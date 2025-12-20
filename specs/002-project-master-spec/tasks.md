# Tasks: Physical AI and Humanoid Robotics Book Project

**Input**: Design documents from `/specs/002-project-master-spec/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which Module this task belongs to (e.g., M1, M2, M3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/` for FastAPI, `docs/` for Docusaurus

---

## Phase 1: Setup (Docusaurus and Project Structure)

**Purpose**: Project initialization and basic structure for the documentation site and repository.

- [X] T001 Initialize git repository and set up `main` branch
- [X] T002 Create initial repository structure: `backend/`, `docs/`, `scripts/`, `specs/`
- [X] T003 [P] Scaffold a new Docusaurus site in `docs/` using the TypeScript template: `npx create-docusaurus@latest docs classic --typescript`
- [X] T004 [P] Install Docusaurus dependencies in `docs/`: `npm install`
- [X] T005 Configure `docs/docusaurus.config.js` with site metadata (title, url, baseUrl), theme, and navigation
- [X] T006 [P] Configure `docs/sidebars.js` to prepare for Module 1 content
- [X] T007 [P] Create custom styling rules in `docs/src/css/custom.css` for the modern, minimal design
- [X] T008 [P] Create placeholder `README.md` and `docs/docs/intro.md`
- [X] T009 Start local dev server (`npm run start` in `docs/`) and verify the site builds and serves correctly
- [X] T010 Configure Render deployment by linking the GitHub repository for CI/CD

---

## Phase 2: Foundational (Backend and RAG Pipeline)

**Purpose**: Core infrastructure for the RAG chatbot. This must be complete before the chatbot can be integrated.

- [X] T011 Initialize Python project in `backend/` with a virtual environment
- [X] T012 [P] Create `backend/requirements.txt` with dependencies: `fastapi`, `uvicorn`, `qdrant-client`, `sentence-transformers`, `pydantic`
- [X] T013 Install Python dependencies: `pip install -r backend/requirements.txt`
- [X] T014 [P] Set up FastAPI app structure in `backend/src/` (api, core, services, models)
- [X] T015 [P] Implement Pydantic models for chat requests in `backend/src/models/chat.py` based on `data-model.md`
- [X] T016 Create the core RAG service in `backend/src/services/rag_service.py` to handle embedding and retrieval logic
- [X] T017 Implement the `/chat` API endpoint in `backend/src/api/chat.py`
- [X] T018 Create the content ingestion script in `scripts/ingest.py` to process markdown from `docs/docs/` and load into Qdrant
- [X] T019 [P] Write unit tests for the RAG service in `backend/tests/`
- [X] T020 Run ingestion script (`scripts/ingest.py`) with placeholder content to verify the pipeline
- [X] T080 [P2] Update RAG service with real Qdrant client implementation in `backend/src/services/rag_service.py` - replace MockQdrantClient with actual QdrantClient
- [X] T081 [P2] Update RAG service with real Sentence Transformer implementation in `backend/src/services/rag_service.py` - replace MockSentenceTransformer with actual SentenceTransformer
- [X] T082 [P2] Update RAG service with real LLM client implementation in `backend/src/services/rag_service.py` - replace MockLLMClient with actual OpenAI or similar client
- [X] T083 [P2] Add proper error handling and retry logic to RAG service in `backend/src/services/rag_service.py`
- [X] T084 [P2] Add proper configuration and environment variable handling to RAG service in `backend/src/services/rag_service.py`
- [X] T085 [P2] Add logging and monitoring capabilities to RAG service in `backend/src/services/rag_service.py`
- [X] T086 [P2] Implement proper context formatting and prompt engineering in RAG service in `backend/src/services/rag_service.py`
- [X] T087 [P2] Add performance optimization including caching to RAG service in `backend/src/services/rag_service.py`
- [X] T088 [P2] Add proper authentication and rate limiting to chat API in `backend/src/api/chat.py`
- [X] T089 [P2] Add comprehensive integration tests for the full RAG pipeline in `backend/tests/test_rag_integration.py`
- [X] T090 [P2] Update ingestion script to properly embed and store content vectors in `scripts/ingest.py`
- [X] T091 [P2] Add validation and quality checks to content ingestion in `scripts/ingest.py`

---

## Phase 2.5: RAG Chatbot Full Implementation

**Purpose**: Complete the RAG chatbot implementation by replacing mock services with real implementations and adding production-ready features.

- [X] T092 [P2.5] Install required dependencies for real implementations in `backend/requirements.txt` (openai, python-dotenv, tenacity for retries)
- [X] T093 [P2.5] Create configuration management system in `backend/src/core/config.py` for environment variables and settings
- [X] T094 [P2.5] Implement real Qdrant client integration in `backend/src/services/rag_service.py`
- [X] T095 [P2.5] Implement real Sentence Transformer for embeddings in `backend/src/services/rag_service.py`
- [X] T096 [P2.5] Implement real OpenAI client for LLM responses in `backend/src/services/rag_service.py`
- [X] T097 [P2.5] Add comprehensive error handling and retry logic to RAG service in `backend/src/services/rag_service.py`
- [X] T098 [P2.5] Add detailed logging to RAG service in `backend/src/services/rag_service.py` per spec requirements
- [X] T099 [P2.5] Implement proper prompt engineering and context formatting in `backend/src/services/rag_service.py`
- [X] T100 [P2.5] Add caching mechanism to RAG service in `backend/src/services/rag_service.py` for performance
- [X] T101 [P2.5] Add rate limiting and authentication to chat API in `backend/src/api/chat.py`
- [X] T102 [P2.5] Add comprehensive integration tests for full RAG pipeline in `backend/tests/test_rag_integration.py`
- [X] T103 [P2.5] Update content ingestion script with proper embedding logic in `scripts/ingest.py`
- [X] T104 [P2.5] Add health check endpoint to FastAPI app in `backend/src/main.py`
- [X] T105 [P2.5] Create environment variable documentation in `backend/README.md`
- [X] T106 [P2.5] Add performance monitoring and metrics collection to RAG service
- [X] T107 [P2.5] Implement comprehensive error responses per OpenAPI spec in `backend/src/api/chat.py`
- [X] T108 [P2.5] Add input validation and sanitization to chat request model in `backend/src/models/chat.py`
- [X] T109 [P2.5] Create comprehensive test suite for error scenarios in `backend/tests/test_error_scenarios.py`
- [X] T110 [P2.5] Add documentation for RAG service API endpoints and usage

---

## Phase 3: User Story - Module 1 (Core Robotics Foundations)

**Goal**: Create the content skeletons for all chapters in Module 1.

**Independent Test**: The site's sidebar should show all four chapters of Module 1, and each page should render with the correct placeholder headings.

- [X] T021 [M1] Create folder `docs/docs/module1-core-robotics`
- [X] T022 [P] [M1] Create chapter skeleton `docs/docs/module1-core-robotics/ch1-intro-ros.md` with front matter and placeholder headings
- [X] T023 [P] [M1] Create chapter skeleton `docs/docs/module1-core-robotics/ch2-ros-nodes-topics.md` with front matter and placeholder headings
- [X] T024 [P] [M1] Create chapter skeleton `docs/docs/module1-core-robotics/ch3-ros-services-actions.md` with front matter and placeholder headings
- [X] T025 [P] [M1] Create chapter skeleton `docs/docs/module1-core-robotics/ch4-urdf-modeling.md` with front matter and placeholder headings
- [X] T026 [M1] Update `docs/sidebars.js` to include all Module 1 chapters
- [X] T027 [M1] Write Lesson 1.1: What is Modern Robotics? (Focus on AI impact) in `docs/docs/module1-core-robotics/ch1-intro-ros.md`
- [X] T027.1 [M1] Write Lesson 1.2: Understanding the ROS 2 Ecosystem in `docs/docs/module1-core-robotics/ch1-intro-ros.md`
- [X] T027.2 [M1] Write Lesson 1.3: The Philosophy and Advantages of ROS 2 in `docs/docs/module1-core-robotics/ch1-intro-ros.md`
- [ ] T068 [M1] Write Lesson 2.1: Creating Nodes and Publishing Topics in `docs/docs/module1-core-robotics/ch2-ros-nodes-topics.md`
- [ ] T068.1 [M1] Write Lesson 2.2: Subscribing to Topics and Message Handling in `docs/docs/module1-core-robotics/ch2-ros-nodes-topics.md`
- [ ] T068.2 [M1] Write Lesson 2.3: Practical Implementation of Custom Message Types in `docs/docs/module1-core-robotics/ch2-ros-nodes-topics.md`
- [ ] T068.3 [M1] Write Lesson 2.4: Testing and Debugging Node Communication in `docs/docs/module1-core-robotics/ch2-ros-nodes-topics.md`

- [ ] T069 [M1] Write Lesson 3.1: Understanding ROS 2 Services in `docs/docs/module1-core-robotics/ch3-ros-services-actions.md`
- [ ] T069.1 [M1] Write Lesson 3.2: Implementing ROS 2 Actions for Long-Running Tasks in `docs/docs/module1-core-robotics/ch3-ros-services-actions.md`
- [ ] T069.2 [M1] Write Lesson 3.3: Best Practices for Service and Action Design in `docs/docs/module1-core-robotics/ch3-ros-services-actions.md`

- [ ] T070 [M1] Write Lesson 4.1: Understanding URDF Structure and Links in `docs/docs/module1-core-robotics/ch4-urdf-modeling.md`
- [ ] T070.1 [M1] Write Lesson 4.2: Defining Joints and Kinematics in URDF in `docs/docs/module1-core-robotics/ch4-urdf-modeling.md`
- [ ] T070.2 [M1] Write Lesson 4.3: Validating and Visualizing URDF Models in `docs/docs/module1-core-robotics/ch4-urdf-modeling.md`

---

## Phase 4: User Story - Module 2 (Simulation & Digital Twin)

**Goal**: Create the content skeletons for all chapters in Module 2.

**Independent Test**: The site's sidebar should show all three chapters of Module 2.

- [X] T028 [M2] Create folder `docs/docs/module2-simulation`
- [X] T029 [P] [M2] Create chapter skeleton `docs/docs/module2-simulation/ch5-gazebo-worlds.md`
- [X] T030 [P] [M2] Create chapter skeleton `docs/docs/module2-simulation/ch6-advanced-sensors.md`
- [X] T031 [P] [M2] Create chapter skeleton `docs/docs/module2-simulation/ch7-photorealistic-sim.md`
- [X] T032 [M2] Update `docs/sidebars.js` to include all Module 2 chapters
- [X] T033 [M2] Write Lesson 2.1: Getting Started with Gazebo Simulator in `docs/docs/module2-simulation/ch5-gazebo-worlds.md`
- [X] T033.1 [M2] Write Lesson 2.2: Creating Custom Gazebo Worlds and Importing URDF Models in `docs/docs/module2-simulation/ch5-gazebo-worlds.md`
- [X] T033.2 [M2] Write Lesson 2.3: Interacting with the Simulated Robot - Physics and Controls in `docs/docs/module2-simulation/ch5-gazebo-worlds.md`
- [ ] T071 [M2] Write Lesson 5.1: Sensor Integration in Gazebo Simulation in `docs/docs/module2-simulation/ch6-advanced-sensors.md`
- [ ] T071.1 [M2] Write Lesson 5.2: Configuring LiDAR Simulation Parameters in `docs/docs/module2-simulation/ch6-advanced-sensors.md`
- [ ] T071.2 [M2] Write Lesson 5.3: Depth Camera and IMU Simulation in `docs/docs/module2-simulation/ch6-advanced-sensors.md`
- [ ] T071.3 [M2] Write Lesson 5.4: Sensor Data Processing and Validation in `docs/docs/module2-simulation/ch6-advanced-sensors.md`

- [ ] T072 [M2] Write Lesson 6.1: Setting up NVIDIA Isaac Sim Environment in `docs/docs/module2-simulation/ch7-photorealistic-sim.md`
- [ ] T072.1 [M2] Write Lesson 6.2: Unity Integration for Photorealistic Rendering in `docs/docs/module2-simulation/ch7-photorealistic-sim.md`
- [ ] T072.2 [M2] Write Lesson 6.3: Synthetic Data Generation Techniques in `docs/docs/module2-simulation/ch7-photorealistic-sim.md`

---

## Phase 5: User Story - Module 3 (The AI-Robot Brain)

**Goal**: Create the content skeletons for all chapters in Module 3.

**Independent Test**: The site's sidebar should show both chapters of Module 3.

- [X] T034 [M3] Create folder `docs/docs/module3-ai-brain`
- [X] T035 [P] [M3] Create chapter skeleton `docs/docs/module3-ai-brain/ch8-isaac-ros-perception.md`
- [X] T036 [P] [M3] Create chapter skeleton `docs/docs/module3-ai-brain/ch9-bipedal-locomotion.md`
- [X] T037 [M3] Update `docs/sidebars.js` to include all Module 3 chapters
- [X] T038 [M3] Write Lesson 3.1: Introduction to NVIDIA Isaac ROS and Perception Pipelines in `docs/docs/module3-ai-brain/ch8-isaac-ros-perception.md`
- [X] T038.1 [M3] Write Lesson 3.2: Visual SLAM (VSLAM) Fundamentals and Isaac ROS Implementation in `docs/docs/module3-ai-brain/ch8-isaac-ros-perception.md`
- [X] T038.2 [M3] Write Lesson 3.3: Deep Dive into Isaac ROS Gems for Perception in `docs/docs/module3-ai-brain/ch8-isaac-ros-perception.md`
- [X] T038.3 [M3] Write Lesson 3.4: Optimizing Perception Performance and Data Management in `docs/docs/module3-ai-brain/ch8-isaac-ros-perception.md`

- [ ] T073 [M3] Write Lesson 7.1: Nav2 Navigation Stack Configuration for Bipedal Robots in `docs/docs/module3-ai-brain/ch9-bipedal-locomotion.md`
- [ ] T073.1 [M3] Write Lesson 7.2: Costmap and Path Planning for Humanoid Locomotion in `docs/docs/module3-ai-brain/ch9-bipedal-locomotion.md`
- [ ] T073.2 [M3] Write Lesson 7.3: Controller Tuning for Stable Bipedal Walking in `docs/docs/module3-ai-brain/ch9-bipedal-locomotion.md`
- [ ] T073.3 [M3] Write Lesson 7.4: Obstacle Avoidance and Dynamic Navigation in `docs/docs/module3-ai-brain/ch9-bipedal-locomotion.md`

---

## Phase 6: User Story - Module 4 (Vision-Language-Action)

**Goal**: Create the content skeletons for all chapters in Module 4.

**Independent Test**: The site's sidebar should show all three chapters of Module 4.

- [X] T039 [M4] Create folder `docs/docs/module4-vla`
- [X] T040 [P] [M4] Create chapter skeleton `docs/docs/module4-vla/ch10-voice-to-action.md`
- [X] T041 [P] [M4] Create chapter skeleton `docs/docs/module4-vla/ch11-cognitive-planning.md`
- [X] T042 [P] [M4] Create chapter skeleton `docs/docs/module4-vla/ch12-capstone-project.md`
- [X] T043 [M4] Update `docs/sidebars.js` to include all Module 4 chapters
- [X] T044 [M4] Write Lesson 4.1: Speech-to-Text Fundamentals and Whisper Integration in `docs/docs/module4-vla/ch10-voice-to-action.md`
- [X] T044.1 [M4] Write Lesson 4.2: Parsing Natural Language Commands for Robot Control in `docs/docs/module4-vla/ch10-voice-to-action.md`
- [X] T044.2 [M4] Write Lesson 4.3: Mapping Parsed Commands to ROS 2 Actions in `docs/docs/module4-vla/ch10-voice-to-action.md`

- [ ] T074 [M4] Write Lesson 8.1: LLM Integration for Natural Language Processing in `docs/docs/module4-vla/ch11-cognitive-planning.md`
- [ ] T074.1 [M4] Write Lesson 8.2: Creating Action Sequences from Natural Language Commands in `docs/docs/module4-vla/ch11-cognitive-planning.md`
- [ ] T074.2 [M4] Write Lesson 8.3: Error Handling and Fallback Strategies in VLA Pipeline in `docs/docs/module4-vla/ch11-cognitive-planning.md`
- [ ] T074.3 [M4] Write Lesson 8.4: Performance Optimization for Real-time VLA Processing in `docs/docs/module4-vla/ch11-cognitive-planning.md`

- [ ] T075 [M4] Write Lesson 9.1: Integrating Voice Command Pipeline with Navigation in `docs/docs/module4-vla/ch12-capstone-project.md`
- [ ] T075.1 [M4] Write Lesson 9.2: Testing the Complete VLA System in Simulation in `docs/docs/module4-vla/ch12-capstone-project.md`
- [ ] T075.2 [M4] Write Lesson 9.3: Troubleshooting Common VLA Pipeline Issues in `docs/docs/module4-vla/ch12-capstone-project.md`

---

## Phase 7: User Story - Module 5 (The RAG Chatbot Companion)

**Goal**: Create the content skeletons and integrate the chatbot functionality.

**Independent Test**: The chatbot widget appears on the site and responds to a test query.

- [X] T045 [M5] Create folder `docs/docs/module5-rag-chatbot`
- [X] T046 [P] [M5] Create chapter skeleton `docs/docs/module5-rag-chatbot/ch13-rag-architecture.md`
- [X] T047 [P] [M5] Create chapter skeleton `docs/docs/module5-rag-chatbot/ch14-building-chatbot.md`
- [X] T048 [M5] Update `docs/sidebars.js` to include all Module 5 chapters
- [X] T049 [M5] Implement the chatbot frontend widget in `docs/src/components/ChatbotWidget.tsx`
- [X] T050 [M5] Swizzle the Root component and add the ChatbotWidget to the site layout (`docs/src/theme/Root.tsx`)
- [X] T051 [M5] Configure the widget to communicate with the backend API
- [X] T052 [M5] Test the end-to-end chatbot functionality locally

---

## Final Phase: Polish & Governance

**Purpose**: Finalize the project and set up maintenance workflows.

- [X] T053 [P] Set up GitHub Issues for feedback, bug tracking, and errata with templates in `.github/ISSUE_TEMPLATE/`
- [X] T054 [P] Create `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md`
- [ ] T055 [P] Perform a full content review for all drafted chapters (technical and stylistic)
- [X] T056 [P] Validate all code examples and ensure they run correctly using `scripts/validate_code_examples.py`
- [X] T057 [P] Final QA of the entire site (links, rendering, mobile responsiveness) using `scripts/check_broken_links.py`
- [X] T058 [P] [M6] Create Appendix A: Setup and Installation Guide in `docs/docs/appendix-a-setup.md`
- [X] T059 [P] [M6] Create Appendix B: Glossary of Terms in `docs/docs/appendix-b-glossary.md`
- [X] T060 [P] [M6] Create Appendix C: Common ROS 2 CLI Commands in `docs/docs/appendix-c-commands.md`
- [X] T061 [P] Add performance tests for the backend API to measure response time under load in `backend/tests/test_performance.py`
- [X] T062 [P] Add frontend performance checks to CI/CD to measure LCP and other web vitals in `.github/workflows/frontend-performance.yml`
- [X] T063 Define and document the release and versioning strategy in `README.md`

---

## Dependencies & Execution Order

- **Setup (Phase 1)** must be completed before any other phase.
- **Foundational (Phase 2)** depends on Phase 1 and blocks the chatbot integration parts of Module 5 (Phase 7).
- **User Stories (Phases 3-7)** for content skeleton creation can run in parallel after Phase 1.
- **Chatbot integration tasks** (T049-T052) in Phase 7 depend on the completion of Phase 2.
- **Final Phase (Polish)** depends on the completion of all other phases.

### Parallel Opportunities
- Once Phase 1 is done, content skeleton creation (T021-T048) can proceed in parallel for all modules.
- Backend setup (Phase 2) can run in parallel with the content skeleton creation.
- Within each module, creating chapter skeletons (`[P]` tasks) can be done in parallel.

## Implementation Strategy

1.  **MVP Scope**: Complete Phase 1, Phase 2, and the content skeletons for Module 1 (Phase 3). This delivers a functional Docusaurus site with the first module outlined and a working backend ready for integration.
2.  **Incremental Delivery**: After the MVP, complete the content for each Module sequentially or in parallel, followed by the full chatbot integration and polish.
3.  **Team Strategy**:
    - **Frontend/Docs Lead**: Focus on Phase 1 and the content skeleton tasks (Phases 3-7).
    - **Backend Lead**: Focus on Phase 2 (RAG pipeline) and chatbot integration (Phase 7).
    - **Content Writers**: Can begin drafting content for modules as soon as their skeletons are created.

---

## Phase 8: Analysis Remediation

**Purpose**: Address gaps identified in the `/sp.analyze` report to ensure full coverage of the project specification.

- [X] T064 Create API contract specification in `specs/002-project-master-spec/contracts/openapi.yml`
- [X] T065 [P] Set up frontend testing framework (Jest/Vitest) in `docs/`
- [X] T066 [P] Write unit tests for the `ChatbotWidget.tsx` component in `docs/src/components/ChatbotWidget.test.tsx`
- [X] T067 Implement error handling in the backend for unavailable APIs and off-topic queries in `backend/src/api/chat.py`
- [X] T068 [M1] Write 4 lessons for Chapter 2 in `docs/docs/module1-core-robotics/ch2-ros-nodes-topics.md` (See Phase 3 for detailed lesson tasks)
- [X] T069 [M1] Write 3 lessons for Chapter 3 in `docs/docs/module1-core-robotics/ch3-ros-services-actions.md` (See Phase 3 for detailed lesson tasks)
- [X] T070 [M1] Write 3 lessons for Chapter 4 in `docs/docs/module1-core-robotics/ch4-urdf-modeling.md` (See Phase 3 for detailed lesson tasks)
- [X] T071 [M2] Write 4 lessons for Chapter 6 in `docs/docs/module2-simulation/ch6-advanced-sensors.md` (See Phase 4 for detailed lesson tasks)
- [X] T072 [M2] Write 3 lessons for Chapter 7 in `docs/docs/module2-simulation/ch7-photorealistic-sim.md` (See Phase 4 for detailed lesson tasks)
- [X] T073 [M3] Write 4 lessons for Chapter 9 in `docs/docs/module3-ai-brain/ch9-bipedal-locomotion.md` (See Phase 5 for detailed lesson tasks)
- [X] T074 [M4] Write 4 lessons for Chapter 11 in `docs/docs/module4-vla/ch11-cognitive-planning.md` (See Phase 6 for detailed lesson tasks)
- [X] T075 [M4] Write 3 lessons for Chapter 12 in `docs/docs/module4-vla/ch12-capstone-project.md` (See Phase 6 for detailed lesson tasks)
- [X] T076 [M5] Write 3 lessons for Chapter 13 in `docs/docs/module5-rag-chatbot/ch13-rag-architecture.md`
- [X] T077 [M5] Write 4 lessons for Chapter 14 in `docs/docs/module5-rag-chatbot/ch14-building-chatbot.md`
- [X] T078 [P] Add a recurring task to the project checklist for linking glossary terms during content review in `specs/002-project-master-spec/checklists/requirements.md`
- [X] T079 [P] Review and enhance `docs/tsconfig.json` with strict rules and update code to comply.