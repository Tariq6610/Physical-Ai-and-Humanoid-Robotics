# Physical AI and Humanoid Robotics Constitution

## Core Principles

### I. Expert-Level Content
All content must be expert-level, technically accurate, and production-ready. Content must be clear and authoritative, yet accessible to the target audience. Every concept should be explained with practical examples and real-world applications.

### II. Technical Accuracy
All code examples, configurations, and procedures must be verified to work in the specified environment. All content must be tested against actual implementations before publication.

### III. Test-First (NON-NEGOTIABLE)
All code implementations (backend services, frontend components, ROS nodes) must have corresponding tests written before implementation. TDD cycle: Tests written → User approved → Tests fail → Then implement; Red-Green-Refactor cycle strictly enforced.

### IV. Integration Testing
Focus areas requiring integration tests: ROS 2 node communications, Docusaurus chatbot integration, RAG pipeline end-to-end flow, simulation-ROS bridge functionality.

### V. Documentation Standards
All content follows Docusaurus-compatible markdown format. Code examples use language-tagged blocks. Visuals use Mermaid for diagrams. All content maintains consistent terminology with the glossary.

### VI. Progressive Learning
Content must be structured to build upon previous concepts. Each chapter must clearly indicate prerequisites and learning outcomes. Complex topics must be broken into digestible lessons.

## Additional Constraints

### Technology Stack Requirements
- ROS 2 Humble Hawksbill (exclusively as specified in clarifications)
- Docusaurus v3 for documentation
- FastAPI for backend services
- Qdrant for vector database
- NVIDIA Isaac for AI/robotics components

### Performance Standards
- RAG chatbot response time: <3 seconds for typical queries
- Page load time: <1 second for Largest Contentful Paint (LCP)
- All code examples must run in reasonable timeframes for learning context

## Development Workflow

### Review Process
Each chapter undergoes three-stage review: 1) Peer Review for clarity and flow, 2) Technical Validation to ensure all code works as described, 3) Final Polish for grammar, style, and formatting consistency.

### Quality Gates
- All code examples must pass automated tests
- All content must pass technical validation
- All links and references must be verified

## Governance

All development must comply with these principles. Any deviation requires explicit approval and documentation of the exception. The constitution supersedes all other practices and must be referenced during all major decisions.

**Version**: 1.0.0 | **Ratified**: 2025-12-11 | **Last Amended**: 2025-12-11
