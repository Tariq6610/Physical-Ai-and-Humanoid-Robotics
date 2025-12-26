---
id: 0001
title: RAG Chatbot Recreation Specification
stage: spec
date: 2025-12-26
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-rag-chatbot-recreation
branch: 001-rag-chatbot-recreation
user: tariq
command: /sp.specify
labels: ["rag", "chatbot", "openai-agents-sdk", "gemini", "specification"]
links:
  spec: specs/001-rag-chatbot-recreation/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-rag-chatbot-recreation/spec.md
  - specs/001-rag-chatbot-recreation/checklists/requirements.md
tests:
  - Specification quality validation (16/16 checks passed)
---

## Prompt

User requested to recreate the RAG chatbot implementation with new frameworks while maintaining existing frontend-backend API connection logic. The current RAG chatbot has a working backend accurately connected to the frontend, but there's a problem with getting chat responses. The user wants to:

1. Recreate the RAG chatbot efficiently with new frameworks
2. Keep the frontend and backend connection logic (APIs, etc.) the same
3. Change only the RAG chatbot implementation approach

User then specified:
- Use OpenAI Agents SDK for the implementation
- Use Google Gemini's free version as the external LLM client
- Use OpenAI ChatKit framework for the frontend chatbot widget (modern prebuilt widget)
- Research integration patterns via Context7 MCP

The user wanted a complete specification following SpecKit methodology to guide the recreation effort with both backend and frontend framework modernization.

## Response snapshot

Created comprehensive feature specification with following key decisions:

**Framework Selection**: OpenAI Agents SDK (Python v0.2.9+) chosen for:
- Lightweight agent orchestration with minimal abstractions
- Built-in conversation management (SQLiteSession/RedisSession)
- Function tools for wrapping RAG retrieval logic
- Direct integration with multiple LLM providers via LiteLLM

**LLM Integration**: Google Gemini 2.0 Flash (free tier) via LiteLLM:
- Install with `pip install "openai-agents[litellm]"`
- Configure using `LitellmModel(model="gemini/gemini-2.0-flash", api_key="...")`
- Zero-cost operation within 15 requests/minute free tier limit
- No fallback provider to maintain budget constraint

**Architecture Approach**:
- Maintain existing Sentence Transformers embeddings (compatibility with Qdrant)
- Keep Qdrant Python client, wrap retrieval in @function_tool decorators
- Replace custom retry/fallback logic with SDK's built-in capabilities
- Preserve API endpoints (POST /chat, GET /health) for compatibility

**Frontend Framework**: OpenAI ChatKit (@openai/chatkit-react) prebuilt widget:
- Replaces custom 70-line ChatbotWidget.tsx with production-ready component
- Built-in markdown rendering and syntax-highlighted code blocks
- Responsive mobile/desktop support without custom CSS
- Real-time streaming with typing indicators (moves streaming from Non-Goals to IN SCOPE)
- Theme customization to match Docusaurus color scheme
- Connect to FastAPI backend via `getClientSecret()` callback

**Specification Coverage**:
- 6 prioritized user stories (4 P1, 2 P2) covering backend RAG + frontend UI
- 28 functional requirements (FR-001 to FR-028, added FR-021 to FR-028 for ChatKit)
- 12 measurable success criteria (response time, uptime, accuracy targets)
- 7 edge cases documented
- 8 assumptions, 10 constraints, 11 out-of-scope items (streaming moved to in-scope)

**Critical Fix Addressed**: Production deployment compatibility (User Story 5, P1) - the root cause of current chat response failures is hardcoded localhost URLs in frontend with no environment configuration for production backends on Render.

## Outcome

- ✅ Impact: Complete, validated specification ready for planning phase. Passed all 16 quality checklist items.
- 🧪 Tests: Specification quality validation completed - no [NEEDS CLARIFICATION] markers remain, all requirements testable and unambiguous
- 📁 Files: Created spec.md (264 lines) and requirements.md checklist (42 lines)
- 🔁 Next prompts: `/sp.plan` to design technical architecture, `/sp.clarify` if any spec gaps discovered during planning
- 🧠 Reflection: Successfully researched OpenAI Agents SDK and Gemini integration via Context7 MCP, resolved framework decision without user clarification by leveraging comprehensive documentation lookup

## Evaluation notes (flywheel)

- Failure modes observed: Initial attempt to update spec was blocked by user (rejected file edit) - likely reviewing changes. Successfully retried after user confirmation.
- Graders run and results (PASS/FAIL):
  - Specification completeness: PASS (all mandatory sections present)
  - Requirement clarity: PASS (20 functional requirements, all testable)
  - Success criteria quality: PASS (12 measurable, technology-agnostic outcomes)
  - Framework research: PASS (comprehensive OpenAI Agents SDK + LiteLLM + Gemini documentation retrieved)
- Prompt variant (if applicable): Standard /sp.specify with user-driven framework selection (OpenAI Agents SDK + Gemini)
- Next experiment (smallest change to try): In planning phase, validate that OpenAI Agents SDK's session management can handle browser-based session storage requirements (current implementation uses browser sessionStorage, SDK uses SQLiteSession/RedisSession)
