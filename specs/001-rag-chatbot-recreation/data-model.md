# Data Model: RAG Chatbot Recreation

**Feature**: 001-rag-chatbot-recreation
**Date**: 2025-12-26
**Source**: Extracted from spec.md Key Entities + OpenAI Agents SDK/ChatKit patterns

---

## Core Entities

### 1. ChatMessage

Represents a single message exchange in a conversation.

**Attributes**:
- `id`: Unique identifier (UUID)
- `session_id`: Reference to parent ConversationSession
- `role`: Enum ("user", "assistant", "system")
- `content`: Message text (string, max 2000 chars)
- `timestamp`: ISO 8601 datetime
- `sources`: Optional list of DocumentChunk references (for citations)
- `metadata`: JSON object for extensibility (model used, tokens, latency)

**Validation Rules** (from FR-007, FR-018):
- `content` must be non-empty after trimming
- `content` sanitized for XSS (HTML escaped)
- `role` must be valid enum value
- `sources` limited to max 5 items

**State Transitions**: None (immutable once created)

**Relationships**:
- Belongs to one ConversationSession
- Optionally references multiple DocumentChunks (many-to-many via citations)

**Storage**:
- **Backend**: SQLiteSession managed by OpenAI Agents SDK (conversations.db)
- **Schema**: OpenAI Agents SDK internal format (messages table with role, content, timestamp columns)
- **Frontend**: ChatKit manages UI state (no direct storage)

---

### 2. ConversationSession

Represents a complete chat interaction lifecycle.

**Attributes**:
- `session_id`: Unique identifier (UUID, primary key)
- `user_identifier`: Anonymous user ID (IP hash or browser fingerprint)
- `messages`: Ordered list of ChatMessage objects
- `created_at`: ISO 8601 datetime (first message)
- `last_activity_at`: ISO 8601 datetime (most recent message)
- `status`: Enum ("active", "expired")
- `metadata`: JSON object (user agent, referrer, device type)

**Validation Rules** (from FR-014):
- `session_id` must be unique
- `last_activity_at` updated on every new message
- Sessions marked "expired" if `last_activity_at` > 24 hours ago

**State Transitions**:
```
Created (first message) → Active (ongoing messages) → Expired (24h inactivity)
```

**Relationships**:
- Contains many ChatMessages (one-to-many)
- ChatMessages ordered chronologically

**Storage**:
- **Backend**: SQLiteSession file (`conversations.db`)
  - SQLite table schema managed by OpenAI Agents SDK
  - Auto-creates tables on first use
  - File location: `SESSION_DB_PATH` environment variable
- **Frontend**: `sessionStorage.setItem('chatkit_session_id', session_id)`
  - Cleared on tab/browser close
  - Retrieved on widget initialization

**Lifecycle Management**:
- **Creation**: On first user message (no session_id in request)
- **Retrieval**: Via `SQLiteSession.get_items(session_id)`
- **Expiry**: Daily cleanup job deletes sessions older than 24 hours
- **Clear**: User clicks "New Conversation" → `session.clear_session()`

---

### 3. DocumentChunk

Represents a segment of indexed documentation.

**Attributes**:
- `chunk_id`: Unique identifier (UUID)
- `document_id`: Parent document reference
- `text`: Chunk content (string, typically 200-500 words)
- `embedding_vector`: Float array (384 dimensions for all-MiniLM-L6-v2)
- `metadata`: JSON object containing:
  - `title`: Document title
  - `section`: Section heading
  - `source_url`: Link to original documentation page
  - `page_number`: Position in document
- `indexed_at`: ISO 8601 datetime

**Validation Rules** (from FR-019):
- `embedding_vector` must be 384-dimensional
- `text` must be non-empty
- `metadata.source_url` must be valid URL

**State Transitions**: None (read-only for chatbot feature)

**Relationships**:
- Belongs to one Document (parent)
- Referenced by ChatMessages via citations (many-to-many)

**Storage**:
- **Vector Database**: Qdrant Cloud collection "robotics_docs"
- **Not Created by This Feature**: Assume pre-populated (Assumption #1)
- **Query Pattern**: Similarity search by embedding_vector

---

### 4. RAGContext

Represents assembled information passed to the LLM.

**Attributes**:
- `query`: User's current question (string)
- `retrieved_chunks`: List of DocumentChunk objects (top 5 by similarity)
- `conversation_history`: List of last 5 ChatMessages
- `system_instructions`: Agent instructions (string, from Agent definition)
- `max_tokens`: Response length limit (int, default 500)

**Validation Rules** (from FR-003, FR-005):
- `retrieved_chunks` limited to 5 items max
- `conversation_history` includes last 5 exchanges max (context window management)
- Total token count (query + chunks + history) must not exceed model limit (8K for Gemini 2.0 Flash)

**State Transitions**: Ephemeral (created per request, not persisted)

**Relationships**:
- Aggregates DocumentChunks (from vector search)
- Aggregates ChatMessages (from session history)

**Storage**: In-memory only (constructed during Agent execution)

**Assembly Process** (handled by OpenAI Agents SDK):
```python
# SDK automatically assembles context:
# 1. Loads session history: session.get_items(limit=5)
# 2. Agent calls retrieve_documentation function tool
# 3. SDK combines: system instructions + history + tool results + user query
# 4. Passes to LiteLLM → Gemini API
```

---

### 5. ErrorResponse

Represents structured error information.

**Attributes**:
- `error_type`: Enum ("network", "timeout", "validation", "server", "ratelimit")
- `user_message`: User-friendly description (string)
- `technical_details`: Full error for logging (string, not exposed to frontend)
- `suggested_actions`: List of strings (e.g., "Try rephrasing your question")
- `timestamp`: ISO 8601 datetime

**Validation Rules** (from FR-011):
- `user_message` must NOT contain stack traces or internal error codes
- `technical_details` logged but never sent to frontend
- `suggested_actions` max 3 items

**State Transitions**: None (created on error, logged, then discarded)

**Relationships**: None

**Storage**:
- **Logs Only**: Not persisted to database
- **Frontend**: ChatKit displays `user_message` via `onError` event
- **Backend**: `technical_details` written to application logs

**Error Mapping** (from spec Edge Cases):
```python
# Qdrant unavailable
ErrorResponse(
    error_type="network",
    user_message="Knowledge base temporarily unavailable",
    suggested_actions=["Try again in a moment", "Contact support if persists"]
)

# Gemini API timeout
ErrorResponse(
    error_type="timeout",
    user_message="Response generation is taking longer than expected. Please try rephrasing your question.",
    suggested_actions=["Use simpler phrasing", "Ask about a specific subtopic"]
)

# Zero results from Qdrant
ErrorResponse(
    error_type="validation",
    user_message="I don't have specific information about that topic in the current documentation",
    suggested_actions=["Browse the documentation directly", "Ask about core Physical AI concepts"]
)
```

---

## Entity Relationships Diagram

```
ConversationSession (1) ──────< (many) ChatMessage
                                        │
                                        │ (optional citations)
                                        │
                                        └──────> (many) DocumentChunk

RAGContext (ephemeral)
    ├── References: DocumentChunk (top 5)
    ├── References: ChatMessage (last 5)
    └── Assembled per request, not persisted

ErrorResponse (ephemeral)
    └── Logged but not persisted
```

---

## Data Flow

### Chat Request Flow
```
1. User types message in ChatKit widget
2. ChatKit calls getClientSecret() if no token → FastAPI /api/chatkit/session
3. Backend creates/retrieves SQLiteSession(session_id)
4. ChatKit sends message → FastAPI POST /chat
5. Backend extracts session_id from token
6. SQLiteSession loads conversation history
7. Agent with tools executes:
   a. retrieve_documentation(query) → Qdrant search
   b. check_topic_relevance(query) → Validation
8. Agent combines: system instructions + history + retrieved chunks + query
9. LiteLLM → Gemini API (streaming response)
10. FastAPI streams response back to ChatKit
11. ChatKit renders with markdown/code highlighting
12. Backend appends message to SQLiteSession
```

### Session Management Flow
```
Frontend sessionStorage: { chatkit_session_id: "uuid-123" }
                                  ↓
Backend SQLiteSession: conversations.db
    sessions table:
        session_id | created_at | last_activity_at
    messages table:
        id | session_id | role | content | timestamp | sources
                                  ↓
Cleanup Job (daily cron):
    DELETE FROM sessions WHERE last_activity_at < NOW() - INTERVAL '24 hours'
```

### Embedding & Retrieval Flow (Unchanged)
```
User Query
    → SentenceTransformer.encode(query) → [384-dim vector]
    → Qdrant.search(query_vector, top_k=5)
    → DocumentChunks with scores
    → Format as context string
    → Pass to Agent via function tool return value
```

---

## Schema Compatibility Notes

### Backward Compatibility
- **Pydantic Models**: Existing `ChatRequest`, `ChatResponse` maintained for API compatibility
- **Session Migration**: New SQLiteSession schema does NOT conflict with old sessionStorage approach (different storage backends)
- **Qdrant Schema**: No changes to vector database schema (embedding dimensions same)

### Breaking Changes
- **None**: All API contracts preserved
- **Additive Only**: New `/api/chatkit/session` endpoint added, existing endpoints unchanged

---

## Next Steps

Phase 1 continues with:
1. **contracts/**: OpenAPI specs for endpoints
2. **quickstart.md**: Developer setup guide
3. **Update agent context**: Add frameworks to `.specify/memory/agent-context.claude.md`
