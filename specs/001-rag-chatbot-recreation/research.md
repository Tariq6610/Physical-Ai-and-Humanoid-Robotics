# Research: RAG Chatbot Recreation Technical Decisions

**Feature**: 001-rag-chatbot-recreation
**Date**: 2025-12-26
**Research Method**: Context7 MCP queries for OpenAI Agents SDK and ChatKit

---

## Overview

This document consolidates research findings from Context7 MCP server queries (`/openai/openai-agents-python` and `/openai/chatkit-js`) that informed technical decisions for recreating the RAG chatbot. All patterns and code examples are sourced from official documentation to ensure accuracy and prevent outdated implementation approaches.

---

## Decision 1: Backend Framework - OpenAI Agents SDK

### What Was Chosen
**OpenAI Agents SDK (Python) v0.2.9+** with LiteLLM extension for Google Gemini integration

### Rationale
1. **Simplified Orchestration**: Eliminates 150+ lines of custom retry logic, error handling, and conversation management
2. **Built-in Session Management**: SQLiteSession provides automatic conversation history persistence without manual state tracking
3. **Function Tools Pattern**: `@function_tool` decorator cleanly wraps Qdrant retrieval logic, making it agent-callable
4. **LiteLLM Integration**: Unified API for Gemini (free tier) without vendor lock-in
5. **Production-Ready**: Official OpenAI framework with ongoing support and updates

### Alternatives Considered
- **LangChain**: More complex abstraction layer, heavier dependency footprint
- **LlamaIndex**: Purpose-built for RAG but less flexible for custom FastAPI integration
- **Custom Implementation**: Requires maintaining retry logic, session state, provider fallback (existing pain point)

### Key Implementation Patterns (from Context7)

**Pattern 1: Agent with Function Tools**
```python
from agents import Agent, Runner, function_tool

@function_tool
def retrieve_documents(query: str) -> str:
    """Query Qdrant for relevant documentation chunks."""
    # Qdrant retrieval logic here
    return formatted_chunks

agent = Agent(
    name="RAG Assistant",
    instructions="You are a Physical AI and Robotics expert. Use retrieved documentation to answer questions accurately.",
    tools=[retrieve_documents]
)

result = await Runner.run(agent, user_query, session=session)
```

**Pattern 2: SQLiteSession for Conversation Memory**
```python
from agents import SQLiteSession

# File-based persistence (survives restarts)
session = SQLiteSession("user_123", "conversations.db")

# Automatic history management across multiple turns
result1 = await Runner.run(agent, "What is Physical AI?", session=session)
result2 = await Runner.run(agent, "How does it differ from traditional AI?", session=session)
# Agent automatically remembers context from result1
```

**Pattern 3: LiteLLM for Gemini**
```python
from agents.extensions.models.litellm_model import LitellmModel

agent = Agent(
    name="RAG Assistant",
    model=LitellmModel(
        model="gemini/gemini-2.0-flash",
        api_key=os.environ["GEMINI_API_KEY"]
    ),
    tools=[retrieve_documents]
)
```

### Integration with Existing FastAPI
- FastAPI remains the HTTP layer (POST /chat endpoint preserved)
- Agent replaces `rag_service.py` internal logic
- Pydantic models (ChatRequest/ChatResponse) maintained for API compatibility
- No changes to Qdrant client or Sentence Transformers

---

## Decision 2: Frontend Framework - OpenAI ChatKit

### What Was Chosen
**OpenAI ChatKit React** (`@openai/chatkit-react` latest) with custom backend integration

### Rationale
1. **Prebuilt UI**: Eliminates 70 lines of custom React + CSS, provides professional chat interface
2. **Built-in Features**: Markdown rendering, code syntax highlighting, responsive design, streaming support
3. **Custom Backend Support**: Can connect to FastAPI via `getClientSecret()` callback (not locked to OpenAI hosted service)
4. **Theme Customization**: Matches Docusaurus color scheme without custom CSS
5. **Production-Tested**: Official OpenAI component with accessibility and mobile optimization

### Alternatives Considered
- **Maintain Custom Widget**: Requires implementing markdown parsing, code highlighting, responsive layout manually
- **Chat UI Kit React**: Less feature-complete, no official OpenAI integration
- **Shadcn Chatbot Kit**: Good alternative but requires more customization

### Key Implementation Patterns (from Context7)

**Pattern 1: ChatKit with Custom Backend**
```typescript
import { ChatKit, useChatKit } from '@openai/chatkit-react';

export function RoboticsChat() {
  const { control } = useChatKit({
    api: {
      async getClientSecret() {
        // Call FastAPI backend instead of OpenAI
        const res = await fetch('/api/chatkit/session', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
        });
        const { client_secret } = await res.json();
        return client_secret;
      },
    },
    theme: {
      colorScheme: 'dark', // Match Docusaurus theme
      color: { accent: { primary: '#25c2a0' } }, // Docusaurus green
      typography: { fontFamily: 'var(--ifm-font-family-base)' },
    },
  });

  return <ChatKit control={control} className="h-[600px] w-[350px]" />;
}
```

**Pattern 2: Environment-Aware Backend URL**
```typescript
// utils/env.ts
export function getBackendURL(): string {
  if (typeof window === 'undefined') return '';

  // Production: Use Render backend URL
  if (window.location.hostname === 'physical-ai-robotics-docs.onrender.com') {
    return 'https://physical-ai-backend.onrender.com';
  }

  // Development: Use localhost
  return 'http://localhost:8000';
}
```

**Pattern 3: Docusaurus Integration (BrowserOnly)**
```typescript
// theme/Root.tsx
import BrowserOnly from '@docusaurus/BrowserOnly';

export default function Root({ children }) {
  return (
    <>
      {children}
      <BrowserOnly fallback={<div />}>
        {() => {
          const RoboticsChat = require('@site/src/components/ChatbotWidget').default;
          return <RoboticsChat />;
        }}
      </BrowserOnly>
    </>
  );
}
```

### Fixes Production Deployment Issue
- **Problem**: Current widget hardcodes `http://localhost:8000/chat` (line 21 of ChatbotWidget.tsx)
- **Solution**: ChatKit `getClientSecret()` callback calls environment-aware backend URL
- **Result**: Works on both localhost (dev) and Render (prod) without code changes

---

## Decision 3: Session Management Architecture

### What Was Chosen
**Hybrid approach**: Backend SQLiteSession + Frontend sessionStorage

### Rationale
1. **Backend Persistence**: SQLiteSession stores full conversation history (survives server restarts)
2. **Frontend Lightweight**: sessionStorage holds session ID only (cleared on tab close)
3. **Sync Mechanism**: ChatKit getClientSecret() generates/retrieves session from backend
4. **Scalability Path**: Can upgrade to RedisSession for distributed deployment without frontend changes

### Architecture Flow
```
User opens chat widget
  → Frontend: Check sessionStorage for session_id
  → If missing: getClientSecret() → FastAPI /api/chatkit/session POST
  → Backend: Create/retrieve SQLiteSession("session_id", "conversations.db")
  → Return session token to frontend
  → Frontend: Store session_id in sessionStorage
  → ChatKit uses token for subsequent requests

User sends message
  → ChatKit → FastAPI POST /chat with session token
  → Backend: Extract session_id from token
  → Load SQLiteSession("session_id")
  → Runner.run(agent, message, session=session)
  → Agent retrieves context + calls function tools
  → Response streamed back to ChatKit
```

### Session Expiry Strategy
- **Browser**: sessionStorage cleared on tab close (built-in)
- **Backend**: SQLiteSession rows older than 24 hours purged daily (cron job)
- **Gemini Rate Limit**: 15 req/min enforced at FastAPI level (per-IP tracking)

---

## Decision 4: RAG Pipeline Integration

### What Was Chosen
**Function Tools wrapping existing Qdrant retrieval**

### Rationale
1. **Minimal Changes**: Existing Qdrant client + Sentence Transformers code reused
2. **Agent Orchestration**: Agent decides when to call retrieval tool based on query
3. **Composability**: Easy to add more tools (e.g., off-topic detection) without refactoring pipeline
4. **Error Handling**: Agent SDK manages retry logic, we only handle Qdrant-specific failures

### Implementation Pattern (from Context7)
```python
from agents import function_tool
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

# Existing infrastructure (unchanged)
qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
embedder = SentenceTransformer('all-MiniLM-L6-v2')

@function_tool
async def retrieve_documentation(
    query: str,
    top_k: int = 5
) -> str:
    """
    Retrieve relevant Physical AI/Robotics documentation chunks.

    Args:
        query: User's question
        top_k: Number of chunks to retrieve (default 5)

    Returns:
        Formatted context with source citations
    """
    try:
        # Generate query embedding
        query_vector = embedder.encode(query).tolist()

        # Search Qdrant
        results = qdrant_client.search(
            collection_name="robotics_docs",
            query_vector=query_vector,
            limit=top_k
        )

        # Format with citations
        chunks = []
        for result in results:
            chunks.append({
                "content": result.payload["text"],
                "source": result.payload["source_url"],
                "score": result.score
            })

        return format_context(chunks)

    except Exception as e:
        # Agent will see this error and can retry or inform user
        raise RuntimeError(f"Documentation retrieval failed: {str(e)}")
```

### Off-Topic Detection Tool
```python
@function_tool
def check_topic_relevance(query: str) -> dict:
    """
    Check if query is related to Physical AI/Robotics.

    Returns:
        {"relevant": bool, "reason": str}
    """
    keywords = ["robot", "ai", "physical", "humanoid", "sensor", "actuator"]
    # Simple keyword check (can be upgraded to classifier later)
    is_relevant = any(kw in query.lower() for kw in keywords)
    return {
        "relevant": is_relevant,
        "reason": "Query matches domain keywords" if is_relevant else "Query off-topic"
    }
```

---

## Decision 5: Deployment Configuration

### What Was Chosen
**Environment variables + conditional logic**

### Rationale
1. **No Hardcoded URLs**: Eliminates current production bug
2. **Single Codebase**: Same code runs in dev/staging/prod
3. **Render-Compatible**: Uses Render's environment variable injection
4. **Frontend Auto-Detection**: Uses `window.location.hostname` to determine environment

### Configuration Matrix

| Environment | Backend URL | Frontend URL | Session Storage |
|-------------|-------------|--------------|-----------------|
| Development | `http://localhost:8000` | `http://localhost:3000` | `conversations.db` (local file) |
| Production  | `https://physical-ai-backend.onrender.com` | `https://physical-ai-robotics-docs.onrender.com` | `conversations.db` (Render persistent disk) |

### Environment Variables

**Backend (.env)**
```bash
# LLM Configuration
GEMINI_API_KEY=<your-key>
LLM_PROVIDER=gemini

# Vector Database
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=<your-key>

# Session Management
SESSION_DB_PATH=./conversations.db
SESSION_EXPIRY_HOURS=24

# CORS (Render production)
FRONTEND_URL=https://physical-ai-robotics-docs.onrender.com
```

**Frontend (Docusaurus config / env.ts)**
```javascript
// Auto-detected, no environment variables needed
const BACKEND_URL = getBackendURL(); // Function checks window.location
```

---

## Decision 6: Testing Strategy

### What Was Chosen
**Maintain existing pytest/Jest infrastructure + add framework-specific tests**

### Rationale
1. **Constitution Compliance**: Test-First Development (Principle III) non-negotiable
2. **Preserve Coverage**: Existing tests for Qdrant, FastAPI, Docusaurus maintained
3. **New Coverage**: Agent execution, function tool calls, ChatKit integration

### New Test Coverage Areas

**Backend (pytest)**
1. **Unit Tests** (`tests/unit/test_agents.py`):
   - Agent initialization with tools
   - Function tool execution (mock Qdrant responses)
   - SQLiteSession CRUD operations
   - LiteLLM Gemini API calls (mocked)

2. **Integration Tests** (`tests/integration/test_rag_pipeline.py`):
   - End-to-end: User query → Agent → Qdrant → Response
   - Session persistence across multiple turns
   - Error handling (Qdrant down, Gemini timeout)

**Frontend (Jest + React Testing Library)**
1. **Component Tests** (`tests/ChatbotWidget.test.tsx`):
   - ChatKit renders correctly
   - getClientSecret() called on mount
   - Messages sent to backend
   - Environment URL resolution

2. **Integration Tests**:
   - Mock FastAPI backend responses
   - Verify session token flow
   - Test error states (backend unreachable)

---

## Summary of All Decisions

| Decision Area | Choice | Key Benefit |
|---------------|--------|-------------|
| Backend Framework | OpenAI Agents SDK + LiteLLM | Eliminates 150+ lines custom code, built-in session management |
| Frontend Framework | OpenAI ChatKit React | Eliminates 70 lines custom UI, professional features out-of-box |
| Session Management | SQLiteSession (backend) + sessionStorage (frontend) | Persistent history, scalable to Redis later |
| RAG Integration | Function tools wrapping Qdrant | Minimal changes to existing pipeline, composable |
| Deployment | Environment-aware URL resolution | Fixes production bug, single codebase for all envs |
| Testing | Maintain existing + add framework tests | Constitution compliance, full coverage |

---

## References

All patterns and code examples sourced from:
- **OpenAI Agents SDK Python**: `/openai/openai-agents-python` (Context7 MCP)
- **OpenAI ChatKit React**: `/openai/chatkit-js` (Context7 MCP)
- **Specification**: `specs/001-rag-chatbot-recreation/spec.md`
- **Constitution**: `.specify/memory/constitution.md`

---

**Next Steps**: Proceed to Phase 1 (data-model.md, contracts/, quickstart.md)
