---
id: 0002
title: RAG Chatbot Recreation Planning
stage: plan
date: 2025-12-26
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-rag-chatbot-recreation
branch: 001-rag-chatbot-recreation
user: tariq
command: /sp.plan
labels: ["rag", "chatbot", "planning", "openai-agents-sdk", "chatkit", "architecture"]
links:
  spec: specs/001-rag-chatbot-recreation/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-rag-chatbot-recreation/plan.md
  - specs/001-rag-chatbot-recreation/research.md
  - specs/001-rag-chatbot-recreation/data-model.md
  - specs/001-rag-chatbot-recreation/quickstart.md
  - specs/001-rag-chatbot-recreation/contracts/chat-endpoint.yaml
  - specs/001-rag-chatbot-recreation/contracts/health-endpoint.yaml
  - specs/001-rag-chatbot-recreation/contracts/chatkit-session.yaml
  - CLAUDE.md (agent context updated)
tests:
  - Constitution Check (5/5 principles PASS)
  - Technical Context validation (all fields resolved)
---

## Prompt

User executed `/sp.plan` to design the technical architecture and implementation approach for recreating the RAG chatbot with modern frameworks. The specification mandates using Context7 MCP to query OpenAI Agents SDK (`/openai/openai-agents-python`) and ChatKit (`/openai/chatkit-js`) before making any architectural decisions.

**Context from Previous Session**:
- Specification completed in PHR 0001
- Frameworks chosen: OpenAI Agents SDK (backend), ChatKit (frontend), Gemini (LLM via LiteLLM)
- Critical requirement: Mandatory Context7 usage for framework patterns
- Production bug identified: Hardcoded localhost URLs preventing deployment

**User Expectation**: Complete implementation plan with:
- Technical architecture based on official framework patterns from Context7
- Data model for entities (ChatMessage, ConversationSession, etc.)
- API contracts (OpenAPI specs)
- Developer quickstart guide
- Constitution compliance validation

## Response snapshot

Created comprehensive implementation plan following SpecKit `/sp.plan` workflow:

**Phase 0: Research (research.md)**
- Queried Context7 for OpenAI Agents SDK patterns:
  - Agent with function tools for RAG retrieval
  - SQLiteSession for conversation persistence
  - LiteLLM for Gemini integration
- Queried Context7 for ChatKit patterns:
  - Custom backend integration via getClientSecret()
  - Theme customization for Docusaurus matching
  - Environment-aware URL resolution
- Documented 6 key decisions with rationale and alternatives

**Phase 1: Design Artifacts**

1. **plan.md** (234 lines):
   - Technical Context: Python 3.11+, FastAPI, OpenAI Agents SDK, ChatKit, TypeScript
   - Constitution Check: 5/5 principles PASS (Test-First, Integration Testing, Technical Accuracy, Performance, Tech Stack)
   - Project Structure: Backend (agents/ directory NEW, existing dirs maintained), Frontend (ChatbotWidget/ replaces custom widget)
   - Complexity Tracking: No violations (frameworks simplify, reduce 220 lines to framework-managed)

2. **research.md** (200+ lines):
   - Decision 1: OpenAI Agents SDK (vs LangChain/LlamaIndex/custom)
   - Decision 2: ChatKit (vs custom widget/alternatives)
   - Decision 3: Hybrid session management (SQLiteSession + sessionStorage)
   - Decision 4: Function tools wrapping Qdrant
   - Decision 5: Environment-aware deployment
   - Decision 6: Testing strategy (maintain existing + framework-specific)

3. **data-model.md** (250+ lines):
   - 5 core entities: ChatMessage, ConversationSession, DocumentChunk, RAGContext, ErrorResponse
   - Validation rules mapped to functional requirements (FR-007, FR-018, etc.)
   - State transitions and lifecycle management
   - Storage strategies (SQLiteSession, Qdrant, sessionStorage)
   - Entity relationship diagram

4. **contracts/** (3 OpenAPI specs):
   - `chat-endpoint.yaml`: POST /chat with session support, error handling
   - `health-endpoint.yaml`: GET /health for monitoring dependencies
   - `chatkit-session.yaml`: POST /api/chatkit/session for token generation

5. **quickstart.md** (300+ lines):
   - Backend setup: Dependencies, env vars, agent module structure
   - Frontend setup: ChatKit installation, old widget removal
   - Integration testing steps
   - Common development tasks (Context7 queries, debugging sessions)
   - Deployment guide (Render)
   - Troubleshooting scenarios

**Architecture Highlights**:
- Backend: FastAPI → Agent (OpenAI SDK) → Function Tools (@function_tool for Qdrant retrieval) → LiteLLM → Gemini
- Frontend: ChatKit widget → getClientSecret() → FastAPI /api/chatkit/session → SessionStorage
- Session: SQLiteSession (backend file persistence) + sessionStorage (frontend temporary)
- Deployment: Environment-aware backend URL resolution fixes production bug

**Critical Pattern from Context7**:
```python
# Backend: Agent with RAG function tool
@function_tool
async def retrieve_documentation(query: str) -> str:
    query_vector = embedder.encode(query).tolist()
    results = qdrant_client.search(...)
    return formatted_chunks

agent = Agent(
    name="RAG Assistant",
    model=LitellmModel(model="gemini/gemini-2.0-flash", api_key=...),
    tools=[retrieve_documentation]
)

# Frontend: ChatKit with custom backend
const { control } = useChatKit({
  api: {
    async getClientSecret() {
      const res = await fetch(getBackendURL() + '/api/chatkit/session', {...});
      return (await res.json()).client_secret;
    }
  }
});
```

## Outcome

- ✅ Impact: Complete implementation plan ready for task generation. All architectural decisions validated via Context7 MCP queries. Constitution Check passed (5/5).
- 🧪 Tests: Constitution compliance verified - Test-First Development enforced, integration testing planned, technical accuracy ensured via Context7
- 📁 Files: Created plan.md, research.md, data-model.md, quickstart.md, 3 OpenAPI contracts, updated CLAUDE.md
- 🔁 Next prompts: `/sp.tasks` to generate actionable implementation tasks, `/sp.analyze` to validate cross-artifact consistency
- 🧠 Reflection: Mandatory Context7 usage ensured accurate framework integration patterns. Identified session management as critical architectural decision (SQLiteSession backend + sessionStorage frontend hybrid). Production deployment fix designed (environment-aware URL resolution).

## Evaluation notes (flywheel)

- Failure modes observed: None. Context7 queries successful for both `/openai/openai-agents-python` and `/openai/chatkit-js`.
- Graders run and results (PASS/FAIL):
  - Constitution Check: PASS (5/5 principles satisfied)
  - Context7 Mandate Compliance: PASS (queried both library IDs before architectural decisions)
  - API Compatibility: PASS (POST /chat, GET /health preserved)
  - Data Model Completeness: PASS (5 entities with validation rules)
  - Contract Coverage: PASS (3 OpenAPI specs for all endpoints)
- Prompt variant (if applicable): Standard /sp.plan with mandatory Context7 framework research
- Next experiment (smallest change to try): During task generation, validate that ChatKit's getClientSecret() token format is compatible with FastAPI session extraction. May need custom token encoding/decoding logic.
