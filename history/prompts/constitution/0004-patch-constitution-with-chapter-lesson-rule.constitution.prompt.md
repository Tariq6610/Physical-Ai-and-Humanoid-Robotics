---
id: 0004
title: Patch Constitution with Chapter Lesson Rule
stage: constitution
date: 2025-12-07
surface: agent
model: Gemini
feature: none
branch: master
user: tariq
command: /sp.constitution
labels: [constitution, patch, structure, lessons]
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

also add every chapter will have atleast three lessons

## Response snapshot

I have patched the constitution to version 1.1.2, adding a rule to the 'Structure and Formatting' section that every chapter will have at least three lessons. The updated constitution is at `.specify/memory/constitution.md`.

## Outcome

- ✅ Impact: Patched the project constitution to include a rule about chapter lessons. Version was incremented from 1.1.1 to 1.1.2.
- 🧪 Tests: N/A
- 📁 Files: Modified `.specify/memory/constitution.md`.
- 🔁 Next prompts: N/A
- 🧠 Reflection: A small, targeted rule about chapter structure was added to the constitution based on user input. This was correctly identified as a patch-level change.

## Evaluation notes (flywheel)

- Failure modes observed: N/A
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A