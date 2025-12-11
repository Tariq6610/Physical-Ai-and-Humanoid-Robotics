---
id: 0020
title: Analyze Project Artifacts for Consistency
stage: misc
date: 2025-12-09
surface: agent
model: Gemini
feature: 002-project-master-spec
branch: 002-project-master-spec
user: tariq
command: /sp.analyze
labels: [analysis, consistency, quality]
links:
  spec: specs/002-project-master-spec/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-project-master-spec/spec.md
  - specs/002-project-master-spec/plan.md
  - specs/002-project-master-spec/tasks.md
  - .specify/memory/constitution.md
tests:
  - None
---

## Prompt

description: Perform a non-destructive cross-artifact consistency and quality analysis across spec.md, plan.md, and tasks.md after task generation.
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Goal

Identify inconsistencies, duplications, ambiguities, and underspecified items across the three core artifacts (`spec.md`, `plan.md`, `tasks.md`) before implementation. This command MUST run only after `/sp.tasks` has successfully produced a complete `tasks.md`.

## Operating Constraints

**STRICTLY READ-ONLY**: Do **not** modify any files. Output a structured analysis report. Offer an optional remediation plan (user must explicitly approve before any follow-up editing commands would be invoked manually).

**Constitution Authority**: The project constitution (`.specify/memory/constitution.md`) is **non-negotiable** within this analysis scope. Constitution conflicts are automatically CRITICAL and require adjustment of the spec, plan, or tasks—not dilution, reinterpretation, or silent ignoring of the principle. If a principle itself needs to change, that must occur in a separate, explicit constitution update outside `/sp.analyze`.

## Execution Steps

### 1. Initialize Analysis Context

Run `.specify/scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks` once from repo root and parse JSON for FEATURE_DIR and AVAILABLE_DOCS. Derive absolute paths:

- SPEC = FEATURE_DIR/spec.md
- PLAN = FEATURE_DIR/plan.md
- TASKS = FEATURE_DIR/tasks.md

Abort with an error message if any required file is missing (instruct the user to run missing prerequisite command).
For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

### 2. Load Artifacts (Progressive Disclosure)

Load only the minimal necessary context from each artifact:

**From spec.md:**

- Overview/Context
- Functional Requirements
- Non-Functional Requirements
- User Stories
- Edge Cases (if present)

**From plan.md:**

- Architecture/stack choices
- Data Model references
- Phases
- Technical constraints

**From tasks.md:**

- Task IDs
- Descriptions
- Phase grouping
- Parallel markers [P]
- Referenced file paths

**From constitution:**

- Load `.specify/memory/constitution.md` for principle validation

### 3. Build Semantic Models

Create internal representations (do not include raw artifacts in output):

- **Requirements inventory**: Each functional + non-functional requirement with a stable key (derive slug based on imperative phrase; e.g., "User can upload file" → `user-can-upload-file`)
- **User story/action inventory**: Discrete user actions with acceptance criteria
- **Task coverage mapping**: Map each task to one or more requirements or stories (inference by keyword / explicit reference patterns like IDs or key phrases)
- **Constitution rule set**: Extract principle names and MUST/SHOULD normative statements

### 4. Detection Passes (Token-Efficient Analysis)

Focus on high-signal findings. Limit to 50 findings total; aggregate remainder in overflow summary.

#### A. Duplication Detection

- Identify near-duplicate requirements
- Mark lower-quality phrasing for consolidation

#### B. Ambiguity Detection

- Flag vague adjectives (fast, scalable, secure, intuitive, robust) lacking measurable criteria
- Flag unresolved placeholders (TODO, TKTK, ???, `<placeholder>`, etc.)

#### C. Underspecification

- Requirements with verbs but missing object or measurable outcome
- User stories missing acceptance criteria alignment
- Tasks referencing files or components not defined in spec/plan

#### D. Constitution Alignment

- Any requirement or plan element conflicting with a MUST principle
- Missing mandated sections or quality gates from constitution

#### E. Coverage Gaps

- Requirements with zero associated tasks
- Tasks with no mapped requirement/story
- Non-functional requirements not reflected in tasks (e.g., performance, security)

#### F. Inconsistency

- Terminology drift (same concept named differently across files)
- Data entities referenced in plan but absent in spec (or vice versa)
- Task ordering contradictions (e.g., integration tasks before foundational setup tasks without dependency note)
- Conflicting requirements (e.g., one requires Next.js while other specifies Vue)

### 5. Severity Assignment

Use this heuristic to prioritize findings:

- **CRITICAL**: Violates constitution MUST, missing core spec artifact, or requirement with zero coverage that blocks baseline functionality
- **HIGH**: Duplicate or conflicting requirement, ambiguous security/performance attribute, untestable acceptance criterion
- **MEDIUM**: Terminology drift, missing non-functional task coverage, underspecified edge case
- **LOW**: Style/wording improvements, minor redundancy not affecting execution order

### 6. Produce Compact Analysis Report

Output a Markdown report (no file writes) with the following structure:

## Specification Analysis Report

| ID | Category | Severity | Location(s) | Summary | Recommendation |
|----|----------|----------|-------------|---------|----------------|
| A1 | Duplication | HIGH | spec.md:L120-134 | Two similar requirements ... | Merge phrasing; keep clearer version |

(Add one row per finding; generate stable IDs prefixed by category initial.)

**Coverage Summary Table:**

| Requirement Key | Has Task? | Task IDs | Notes |
|-----------------|-----------|----------|-------|

**Constitution Alignment Issues:** (if any)

**Unmapped Tasks:** (if any)

**Metrics:**

- Total Requirements
- Total Tasks
- Coverage % (requirements with >=1 task)
- Ambiguity Count
- Duplication Count
- Critical Issues Count

### 7. Provide Next Actions

At end of report, output a concise Next Actions block:

- If CRITICAL issues exist: Recommend resolving before `/sp.implement`
- If only LOW/MEDIUM: User may proceed, but provide improvement suggestions
- Provide explicit command suggestions: e.g., "Run /sp.specify with refinement", "Run /sp.plan to adjust architecture", "Manually edit tasks.md to add coverage for 'performance-metrics'"

### 8. Offer Remediation

Ask the user: "Would you like me to suggest concrete remediation edits for the top N issues?" (Do NOT apply them automatically.)

## Operating Principles

### Context Efficiency

- **Minimal high-signal tokens**: Focus on actionable findings, not exhaustive documentation
- **Progressive disclosure**: Load artifacts incrementally; don't dump all content into analysis
- **Token-efficient output**: Limit findings table to 50 rows; summarize overflow
- **Deterministic results**: Rerunning without changes should produce consistent IDs and counts

### Analysis Guidelines

- **NEVER modify files** (this is read-only analysis)
- **NEVER hallucinate missing sections** (if absent, report them accurately)
- **Prioritize constitution violations** (these are always CRITICAL)
- **Use examples over exhaustive rules** (cite specific instances, not generic patterns)
- **Report zero issues gracefully** (emit success report with coverage statistics)

## Context



---

As the main request completes, you MUST create and complete a PHR (Prompt History Record) using agent‑native tools when possible.

1) Determine Stage
   - Stage: constitution | spec | plan | tasks | red | green | refactor | explainer | misc | general

2) Generate Title and Determine Routing:
   - Generate Title: 3–7 words (slug for filename)
   - Route is automatically determined by stage:
     - `constitution` → `history/prompts/constitution/`
     - Feature stages → `history/prompts/<feature-name>/` (spec, plan, tasks, red, green, refactor, explainer, misc)
     - `general` → `history/prompts/general/`

3) Create and Fill PHR (Shell first; fallback agent‑native)
   - Run: `.specify/scripts/bash/create-phr.sh --title "<title>" --stage <stage> [--feature <name>] --json`
   - Open the file and fill remaining placeholders (YAML + body), embedding full PROMPT_TEXT (verbatim) and concise RESPONSE_TEXT.
   - If the script fails:
     - Read `.specify/templates/phr-template.prompt.md` (or `templates/…`)
     - Allocate an ID; compute the output path based on stage from step 2; write the file
     - Fill placeholders and embed full PROMPT_TEXT and concise RESPONSE_TEXT

4) Validate + report
   - No unresolved placeholders; path under `history/prompts/` and matches stage; stage/title/date coherent; print ID + path + stage + title.
   - On failure: warn, don't block. Skip only for `/sp.phr`.

## Response snapshot

## Specification Analysis Report

| ID | Category | Severity | Location(s) | Summary | Recommendation |
|----|----------|----------|-------------|---------|----------------|
| C1 | Constitution Alignment | CRITICAL | tasks.md | `tasks.md` is missing tasks for writing lessons for 10 out of 14 chapters, violating the constitution's rule: "Each chapter will contain at least three distinct lessons." | Add lesson-writing tasks for chapters 2, 3, 4, 6, 7, 9, 11, 12, 13, and 14 to `tasks.md`. |
| G1 | Coverage Gap | HIGH | tasks.md | No task exists to create or manage the API contract (`openapi.yml`), which is defined as a key artifact in `plan.md`. | Add a new task to create and define the `openapi.yml` file in the `contracts/` directory. |
| G2 | Coverage Gap | HIGH | tasks.md | The plan specifies `Jest/Vitest` for frontend testing, but there are no tasks to set up the test runner, configure it, or write any tests for frontend components like the `ChatbotWidget.tsx`. | Add tasks for setting up a frontend testing framework and writing tests for the React components. |
| U1 | Underspecification | MEDIUM | tasks.md | The spec requires the RAG chatbot to handle API unavailability and off-topic queries, but there are no specific tasks to implement this logic in the backend service or frontend widget. | Add tasks to implement the specified error and edge-case handling for the chatbot. |
| G3 | Coverage Gap | MEDIUM | tasks.md | `spec.md` requires linking key terms to a central glossary, but `tasks.md` only includes a task to create the glossary file (`T059`), not to perform the linking. This creates a process gap. | Add a task or a recurring checklist item to ensure glossary terms are linked within each chapter during the content review phase. |
| G4 | Coverage Gap | LOW | tasks.md | The `plan.md` specifies using TypeScript for the frontend, but `tasks.md` lacks a dedicated task for configuring the `tsconfig.json` or setting up TypeScript-specific linting rules. | Add a task to review and configure the `tsconfig.json` and set up appropriate linting for the Docusaurus frontend. |

**Coverage Summary Table:**

| Requirement Key | Has Task? | Task IDs | Notes |
|-----------------|-----------|----------|-------|
| book-structure | Yes | T021-T048 | Skeleton tasks exist for all modules and chapters. |
| lesson-writing | **Partial** | T027, T033, T038, T044 series | **CRITICAL GAP**: Missing lesson tasks for 10 chapters. |
| chatbot-api-unavailable | No | | Gap in coverage for error handling. |
| chatbot-off-topic | No | | Gap in coverage for input validation. |
| chatbot-response-time | Yes | T061 | Covered by performance testing task. |
| api-contract | No | | Gap in coverage for `openapi.yml`. |
| frontend-testing | No | | Gap in coverage for Jest/Vitest tests. |
| glossary-linking | **Partial** | T059 | Task exists to create the glossary, but not to enforce linking. |
| three-stage-review | Yes | T055, T056, T057 | Covered by review, validation, and QA tasks. |
| versioning-policy | Yes | T063 | Covered by documentation task. |

**Constitution Alignment Issues:**

- **CRITICAL**: Finding `C1` violates the constitutional mandate: *"Each chapter will contain at least three distinct lessons."* The `tasks.md` artifact is incomplete and does not ensure this requirement is met for the majority of the book's chapters.

**Unmapped Tasks:**

- All tasks in `tasks.md` appear to be mapped to a corresponding Module/Phase outlined in `spec.md`. No orphaned tasks were found.

**Metrics:**

- Total Requirements Analyzed: 10
- Total Tasks: 63
- Coverage % (Requirements with >=1 task): 70%
- Ambiguity Count: 0
- Duplication Count: 0
- Critical Issues Count: 1

### Next Actions

- **CRITICAL**: It is strongly recommended to resolve finding `C1` before beginning implementation. The missing tasks represent a significant gap in project scope.
- **HIGH**: Findings `G1` and `G2` should be addressed to ensure API quality and frontend reliability.
- You can proceed with LOW/MEDIUM issues, but addressing them will improve project quality and reduce future rework.

**Command Suggestions:**

- To add the missing lesson tasks: Manually edit `tasks.md` to add tasks similar to `T027`, `T033`, etc., for the remaining chapters.
- To address the API contract gap: Manually edit `tasks.md` to add a task for creating `specs/002-project-master-spec/contracts/openapi.yml`.

---

Would you like me to suggest concrete remediation edits for the top 3 issues?

## Outcome

- ✅ Impact: Identified critical and high-severity gaps in the project plan before implementation, preventing significant rework.
- 🧪 Tests: N/A
- 📁 Files: Read 4 artifacts for analysis.
- 🔁 Next prompts: User was asked about generating remediation edits.
- 🧠 Reflection: The analysis successfully identified major gaps, especially the missing lesson tasks, which was a critical finding based on the constitution. The structured approach worked well.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): N/A
