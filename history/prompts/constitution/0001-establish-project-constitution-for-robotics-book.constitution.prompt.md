---
id: 0001
title: Establish Project Constitution for Robotics Book
stage: constitution
date: 2025-12-07
surface: agent
model: Gemini
feature: none
branch: master
user: tariq
command: /sp.constitution
labels: [constitution, book, robotics]
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

/sp.constitution Write a complete, professional digital book titled “Physical AI and Humanoid Robotics,” structured around four core modules: (1) The Robotic Nervous System (ROS 2), covering middleware, ROS 2 nodes, topics, services, rclpy integration, and URDF for humanoids; (2) The Digital Twin (Gazebo & Unity), covering physics simulation, gravity, collisions, high-fidelity rendering, human-robot interaction, and sensor simulation including LiDAR, depth cameras, and IMUs; (3) The AI-Robot Brain (NVIDIA Isaac), covering Isaac Sim for photorealistic simulation and synthetic data, Isaac ROS acceleration for VSLAM and navigation, and Nav2 path planning for bipedal locomotion; (4) Vision-Language-Action (VLA), covering voice-to-action using Whisper, cognitive planning using LLMs to convert natural language into ROS 2 actions, and a capstone project where a humanoid robot receives a voice command, plans a path, navigates obstacles, identifies an object, and manipulates it. All chapters must be expert-level, technically accurate, forward-looking, and written in a clear, authoritative tone. Content must use Docusaurus-compatible markdown, open with a short introduction, include 3–6 deep sections with examples, diagrams, and modern references, and close with summaries and takeaways. Maintain consistent terminology across the entire book, avoid filler, and ensure the writing is simultaneously accessible to ambitious learners and rigorous enough for robotics professionals. All generated content must strictly follow this constitution and produce polished, production-ready chapters.

for example:
/sp.constitution

Project: Research paper on AI-native software development

Core principles:
- Accuracy through primary source verification
- Clarity for academic audience (computer science background)
- Reproducibility (all claims cited and traceable)
- Rigor (peer-reviewed sources preferred)

Key standards:
- All factual claims must be traceable to sources
- Citation format: APA style
- Source types: minimum 50% peer-reviewed articles
- Plagiarism check: 0% tolerance before submission
- Writing clarity: Flesch-Kincaid grade 10-12

Constraints:
- Word count: 5,000-7,000 words
- Minimum 15 sources
- Format: PDF with embedded citations

Success criteria:
- All claims verified against sources
- Zero plagiarism detected
- Passes fact-checking review

## Response snapshot

I have updated the project constitution to version 1.0.0, establishing the core principles for the "Physical AI and Humanoid Robotics" book based on your detailed request. The constitution file is located at `.specify/memory/constitution.md`. I also created a Prompt History Record for this action.

## Outcome

- ✅ Impact: Established the project's foundational principles and standards in the constitution file.
- 🧪 Tests: N/A
- 📁 Files: Modified `.specify/memory/constitution.md`.
- 🔁 Next prompts: Potentially updating template files (`plan-template.md`, `spec-template.md`, `tasks-template.md`).
- 🧠 Reflection: The user's prompt was a detailed description of a project, which was interpreted as the constitution. The process involved extracting principles, standards, and structure from this description and mapping them to the constitution template.

## Evaluation notes (flywheel)

- Failure modes observed: N/A
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A