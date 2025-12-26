---
id: 0003
title: RAG Chatbot Recreation Tasks Generation
stage: tasks
date: 2025-12-26
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-rag-chatbot-recreation
branch: 001-rag-chatbot-recreation
user: tariq
command: /sp.tasks
labels: ["rag", "chatbot", "tasks", "tdd", "openai-agents-sdk", "chatkit"]
links:
  spec: specs/001-rag-chatbot-recreation/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-rag-chatbot-recreation/tasks.md
tests:
  - Task format validation (55 tasks, all follow checklist format)
  - User story mapping verification (US1-US6 coverage complete)
  - TDD compliance check (tests before implementation)
---

## Prompt

User executed `/sp.tasks` to generate actionable implementation tasks from the planning artifacts. The specification mandates Context7 MCP usage for framework documentation queries, and the constitution requires Test-First Development (Principle III - NON-NEGOTIABLE).

**Context from Previous Sessions**:
- PHR 0001: Specification with mandatory Context7 usage for OpenAI Agents SDK + ChatKit
- PHR 0002: Implementation plan with architecture, research, data model, contracts, quickstart
- Planning artifacts available: spec.md, plan.md, research.md, data-model.md, contracts/, quickstart.md

**User Expectation**: Generate comprehensive tasks.md with:
- Tasks organized by user story priority (P1, P2, P3)
- TDD workflow (tests before implementation)
- Context7 MCP query tasks in Phase 2 (BEFORE framework code)
- Exact file paths for each task
- Dependency graph and parallel execution opportunities
- MVP-first strategy focusing on P1 user stories

## Response snapshot

Generated comprehensive tasks.md (55 tasks across 9 phases):

**Task Organization**:
- Phase 1: Setup & Dependencies (7 tasks) - Install frameworks, create directories
- Phase 2: Context7 MCP Research (2 tasks) - MANDATORY framework documentation queries
- Phase 3: User Story 1 - Basic Q&A (11 tasks: 4 tests + 7 implementation) - Core MVP
- Phase 4: User Story 6 - Production URLs (4 tasks: 2 tests + 2 implementation) - Deployment fix
- Phase 5: User Story 5 - ChatKit UI (8 tasks: 3 tests + 5 implementation) - Frontend MVP
- Phase 6: User Story 3 - Error Handling (6 tasks: 3 tests + 3 implementation) - Robustness
- Phase 7: User Story 2 - Multi-turn Context (5 tasks: 2 tests + 3 implementation) - Enhancement
- Phase 8: User Story 4 - Off-topic Detection (5 tasks: 2 tests + 3 implementation) - Enhancement
- Phase 9: Polish & Cross-Cutting (7 tasks) - Documentation, performance, security

**TDD Compliance** (Constitution Principle III):
- Total test tasks: 16 (29% of tasks)
- All test tasks positioned BEFORE their corresponding implementation tasks
- Test acceptance criteria: "Test fails (feature doesn't exist yet)"
- Workflow enforced: Write test → Verify FAIL → Implement → Verify PASS

**Context7 MCP Integration**:
- Phase 2 dedicated to Context7 queries (T008-T009)
- T008: Query `/openai/openai-agents-python` for backend patterns
- T009: Query `/openai/chatkit-js` for frontend patterns
- BLOCKS all implementation phases (spec constraint #11)

**Critical Tasks**:
- T015: retrieve_documentation @function_tool (core RAG logic)
- T016: RAG agent definition with LiteLLM Gemini
- T017: SQLiteSession wrapper for conversation memory
- T018: Refactor rag_service.py to use Runner.run()
- T028: ChatKit session endpoint (JWT generation)
- T030: ChatKit widget component with getClientSecret()
- T023: getBackendURL() environment utility (fixes production bug)

**Dependency Graph**:
- US1 (Basic Q&A) is foundation for US2, US3, US4
- US6 (Production URLs) is foundation for US5 (ChatKit)
- US5 needs US6 + T028 (session endpoint)
- P2 stories (US2, US4) can run in parallel after US1

**MVP Path** (P1 stories):
```
Phase 1 → Phase 2 →
  ├─→ Phase 3 (US1) → Phase 6 (US3) ─┐
  │                                   ├─→ Phase 9 (Polish)
  └─→ Phase 4 (US6) → Phase 5 (US5) ─┘
```

**Estimated Time**:
- MVP (P1 stories): ~54 hours
- Full feature: ~70 hours

## Outcome

- ✅ Impact: Complete, actionable tasks.md ready for `/sp.implement`. 55 tasks with exact file paths, TDD workflow, Context7 integration, dependency graph.
- 🧪 Tests: TDD enforced - 16 test tasks positioned before implementation. Constitution Principle III compliant.
- 📁 Files: Created tasks.md (300+ lines) with 9 phases, dependency graph, parallel execution guide, MVP strategy
- 🔁 Next prompts: `/sp.implement` to execute tasks in order, `/sp.analyze` to validate cross-artifact consistency
- 🧠 Reflection: Successfully mapped 6 user stories to 55 tasks. Identified critical path (US1→US6→US5→US3) for fastest MVP delivery. Phase 2 (Context7 queries) ensures agents have accurate framework patterns before code generation.

## Evaluation notes (flywheel)

- Failure modes observed: None. All planning artifacts loaded successfully.
- Graders run and results (PASS/FAIL):
  - Task format compliance: PASS (all 55 tasks follow `- [ ] [ID] [P?] [Story] Description with path` format)
  - User story coverage: PASS (all 6 stories from spec.md mapped to phases)
  - TDD compliance: PASS (16 test tasks before implementation, Constitution Principle III satisfied)
  - Context7 mandate: PASS (Phase 2 dedicated to framework research before implementation)
  - Dependency graph: PASS (critical path identified, parallel opportunities marked)
- Prompt variant (if applicable): Standard /sp.tasks with Context7 research phase and TDD enforcement
- Next experiment (smallest change to try): During implementation (/sp.implement), validate that LiteLLM's Gemini integration handles streaming responses correctly for ChatKit's real-time display (FR-025). May need to use Runner.run_streamed() instead of Runner.run().
