# Implementation Plan: RAG Chatbot Recreation with Modern Frameworks

**Branch**: `001-rag-chatbot-recreation` | **Date**: 2025-12-26 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-rag-chatbot-recreation/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Recreate the RAG chatbot implementation using modern frameworks while maintaining API compatibility. Replace custom backend orchestration with OpenAI Agents SDK (Python) + Google Gemini via LiteLLM. Replace custom frontend widget (70 lines React) with OpenAI ChatKit prebuilt component. Fix production deployment issues caused by hardcoded localhost URLs. Core RAG pipeline (Qdrant vector DB, Sentence Transformers embeddings, FastAPI) remains unchanged.

**Primary Objectives**:
1. Backend: Implement agent-based RAG using OpenAI Agents SDK with SQLiteSession for conversation memory
2. Frontend: Integrate ChatKit widget with custom backend via `getClientSecret()` callback
3. Production: Environment-aware backend URL configuration for Render deployments
4. Performance: Maintain <3 second response time (95th percentile)

## Technical Context

**Backend Stack**:
- **Language/Version**: Python 3.11+
- **Primary Dependencies**:
  - OpenAI Agents SDK 0.2.9+ (`pip install "openai-agents[litellm]"`)
  - LiteLLM for Gemini integration
  - FastAPI 0.104+ (existing)
  - Sentence Transformers (existing, maintained)
  - Qdrant Client (existing, maintained)
  - Pydantic 2.x for data validation

**Frontend Stack**:
- **Language/Version**: TypeScript 5.x, React 18.x
- **Primary Dependencies**:
  - OpenAI ChatKit React (`@openai/chatkit-react` latest)
  - Docusaurus 3.3.2 (existing)
  - No additional CSS frameworks (ChatKit self-contained)

**Storage**:
- **Backend**: SQLiteSession for conversation history (`conversations.db` file-based storage)
- **Vector DB**: Qdrant Cloud (existing, maintained)
- **Frontend**: Browser sessionStorage for lightweight session persistence

**Testing**:
- **Backend**: pytest with async support, existing test infrastructure maintained
- **Frontend**: Jest + React Testing Library (existing)
- **Integration**: End-to-end tests for RAG pipeline flow

**Target Platform**:
- **Backend**: Linux server (Render web service, Python runtime)
- **Frontend**: Static site hosting (Render static site, Node.js build)
- **Development**: macOS/Linux local environments

**Project Type**: Web application (separate frontend + backend)

**Performance Goals**:
- RAG response latency: <3 seconds p95 (FR-009)
- Concurrent users: 100 without degradation (SC-002)
- Gemini API rate limit: 15 requests/minute (free tier constraint)
- Vector search: <500ms for top-5 retrieval

**Constraints**:
- Zero LLM cost (Gemini free tier only, no fallback)
- API endpoint compatibility (POST /chat, GET /health preserved)
- Qdrant free tier: 1GB storage, 1M vectors
- No breaking changes to Docusaurus configuration
- MANDATORY: All framework decisions must reference Context7 MCP queries

**Scale/Scope**:
- Expected traffic: 10,000 queries/month
- Documentation corpus: ~500 pages indexed in Qdrant
- Conversation history: session-scoped (24-hour expiry)
- Deployment: 2 services (frontend static + backend web)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Test-First Development (Principle III - NON-NEGOTIABLE)

**Status**: ✅ PASS

**Evidence**:
- Existing test infrastructure (pytest backend, Jest frontend) will be maintained (constraint #4)
- Plan includes test coverage for: Agent function tools, ChatKit integration, FastAPI endpoints
- TDD cycle enforced: Tests written → Fail → Implement → Pass

**Action**: Tests must be written for new components (Agent setup, function tools, ChatKit integration) before implementation in Phase 2

### Integration Testing (Principle IV)

**Status**: ✅ PASS

**Evidence**:
- RAG pipeline end-to-end testing explicitly covered
- Focus areas: OpenAI Agents SDK session management, ChatKit-backend connection, Qdrant retrieval
- Existing integration test structure maintained

**Action**: Add integration tests for Agent-to-Qdrant flow and ChatKit-to-FastAPI session establishment

### Technical Accuracy (Principle II)

**Status**: ✅ PASS

**Evidence**:
- All framework integrations verified via Context7 MCP queries (mandatory per spec)
- Code patterns sourced from official OpenAI Agents SDK and ChatKit documentation
- Existing Qdrant + Sentence Transformers setup proven working

**Action**: Validate all code examples against actual implementations before tasks generation

### Performance Standards (Section: Performance Standards)

**Status**: ✅ PASS

**Evidence**:
- RAG chatbot <3s target aligns with FR-009 and constitution requirement
- Gemini 2.0 Flash model selected for low-latency (free tier)
- SQLiteSession file-based storage has negligible overhead (<10ms)

**Action**: Performance testing must validate p95 latency <3s under load

### Technology Stack Requirements (Section: Technology Stack Requirements)

**Status**: ✅ PASS (with additions)

**Evidence**:
- Docusaurus v3: Maintained (no breaking changes, constraint #10)
- FastAPI: Maintained (existing endpoints preserved, constraint #1)
- Qdrant: Maintained (existing vector DB + embeddings)
- **NEW**: OpenAI Agents SDK (Python backend framework)
- **NEW**: OpenAI ChatKit (React frontend component)
- **NEW**: LiteLLM (Gemini integration layer)

**Justification for New Dependencies**:
- OpenAI Agents SDK replaces custom orchestration (150+ lines → ~50 lines with framework)
- ChatKit replaces custom widget (70 lines → framework-managed UI)
- LiteLLM enables Gemini free tier (zero-cost constraint)

**Action**: Document new dependencies in requirements.txt and package.json

## Project Structure

### Documentation (this feature)

```text
specs/001-rag-chatbot-recreation/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
│   ├── chat-endpoint.yaml         # POST /chat OpenAPI spec
│   ├── health-endpoint.yaml       # GET /health OpenAPI spec
│   └── chatkit-session.yaml       # POST /api/chatkit/session spec
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
# Backend (Python/FastAPI)
backend/
├── src/
│   ├── agents/                    # NEW: OpenAI Agents SDK integration
│   │   ├── __init__.py
│   │   ├── rag_agent.py          # Agent definition with function tools
│   │   ├── tools.py              # @function_tool decorators for Qdrant retrieval
│   │   └── session_manager.py   # SQLiteSession wrapper
│   ├── models/                    # EXISTING: Pydantic models (maintained)
│   │   ├── __init__.py
│   │   └── chat.py               # ChatRequest, ChatResponse models
│   ├── services/                  # EXISTING: Business logic
│   │   ├── __init__.py
│   │   ├── rag_service.py        # REFACTOR: Use agent.run() instead of custom logic
│   │   └── embeddings.py         # MAINTAINED: Sentence Transformers (unchanged)
│   ├── api/                       # EXISTING: FastAPI routes
│   │   ├── __init__.py
│   │   └── chat.py               # UPDATED: POST /chat now calls Agent
│   ├── core/                      # EXISTING: Configuration
│   │   ├── __init__.py
│   │   └── config.py             # ADD: GEMINI_API_KEY, SESSION_DB_PATH
│   └── main.py                    # EXISTING: FastAPI app entry (minimal changes)
├── tests/                         # EXISTING: Test infrastructure
│   ├── unit/
│   │   ├── test_agents.py        # NEW: Agent tool execution tests
│   │   └── test_rag_service.py   # UPDATED: Test agent integration
│   ├── integration/
│   │   └── test_rag_pipeline.py  # UPDATED: End-to-end with Agent
│   └── conftest.py                # MAINTAINED: Fixtures
├── conversations.db               # NEW: SQLiteSession storage (gitignored)
├── requirements.txt               # UPDATED: Add openai-agents[litellm]
└── .env                           # UPDATED: Add GEMINI_API_KEY

# Frontend (React/TypeScript/Docusaurus)
docs/
├── src/
│   ├── components/
│   │   ├── ChatbotWidget/        # NEW: ChatKit integration (replaces old widget)
│   │   │   ├── index.tsx         # ChatKit wrapper component
│   │   │   └── config.ts         # Theme + backend URL configuration
│   │   └── [OLD] ChatbotWidget.tsx           # REMOVE
│   │   └── [OLD] ChatbotWidget.module.css    # REMOVE
│   ├── theme/
│   │   └── Root.tsx              # UPDATED: Import new ChatKit component
│   └── utils/
│       └── env.ts                 # NEW: Environment-aware backend URL resolution
├── package.json                   # UPDATED: Add @openai/chatkit-react
├── tsconfig.json                  # MAINTAINED
└── docusaurus.config.js           # MAINTAINED: No breaking changes

# Shared
.specify/
└── memory/
    └── agent-context.claude.md    # UPDATED: Add OpenAI Agents SDK + ChatKit to tech stack
```

**Structure Decision**: Maintains existing web application structure (separate backend/frontend). Backend adds new `agents/` directory for OpenAI Agents SDK code. Frontend replaces custom widget with ChatKit integration in dedicated subdirectory. Preserves all existing API routes and Docusaurus configuration for backwards compatibility.

**Key Architectural Decisions**:
1. **Backend**: Agent wraps Qdrant retrieval as @function_tool, maintains FastAPI as HTTP layer
2. **Frontend**: ChatKit connects to custom backend (not OpenAI hosted) via getClientSecret() callback
3. **Session Management**: Backend SQLiteSession (file-based) syncs with ChatKit frontend sessions
4. **Deployment**: Environment variables determine backend URL (dev: localhost, prod: Render URL)

## Complexity Tracking

> **No violations of Constitution principles. This table remains empty.**

All new dependencies (OpenAI Agents SDK, ChatKit, LiteLLM) are justified simplifications that reduce code complexity:
- **OpenAI Agents SDK**: Eliminates 150+ lines of custom retry/fallback logic
- **ChatKit**: Eliminates 70 lines of custom React UI + CSS
- **LiteLLM**: Unified API for Gemini (simpler than direct Google AI SDK integration)

No new projects added (backend/frontend already exist). No architectural patterns introduced beyond framework-standard practices (Agent + function tools, ChatKit hooks).
