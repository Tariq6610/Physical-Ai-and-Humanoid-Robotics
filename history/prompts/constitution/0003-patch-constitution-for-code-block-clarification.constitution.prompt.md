---
id: 0003
title: Patch Constitution for Code Block Clarification
stage: constitution
date: 2025-12-07
surface: agent
model: Gemini
feature: none
branch: master
user: tariq
command: /sp.constitution
labels: [constitution, patch, formatting, code-block]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - null
---

## Prompt

/sp.constitution also add if adding code in the book the code sould be in a code block

## Response snapshot

I have patched the constitution to version 1.1.1, adding a rule to the 'Structure and Formatting' section that all code examples must be placed within formatted markdown code blocks. The updated constitution is at `.specify/memory/constitution.md`.

## Outcome

- ✅ Impact: Patched the project constitution to clarify a formatting rule for code blocks. Version was incremented from 1.1.0 to 1.1.1.
- 🧪 Tests: N/A
- 📁 Files: Modified `.specify/memory/constitution.md`.
- 🔁 Next prompts: N/A
- 🧠 Reflection: A small, targeted clarification was added to the constitution based on user input. This was correctly identified as a patch-level change.

## Evaluation notes (flywheel)

- Failure modes observed: N/A
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A