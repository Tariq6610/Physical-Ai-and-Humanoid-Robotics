# Research & Decisions for Project "Physical AI and Humanoid Robotics"

## 1. Docusaurus Setup

- **Decision**: Use **Docusaurus v3.x** (latest stable version).
- **Rationale**: Provides the best features, performance, and security. It supports MDX v3, which allows for more interactive components.
- **Alternatives Considered**: Docusaurus v2 (older, less feature-rich).

- **Decision**: Hosting will be on **Vercel**.
- **Rationale**: Vercel offers seamless integration with GitHub for CI/CD, automatic deployments on push, preview deployments for pull requests, and a generous free tier suitable for this project. It's optimized for modern static site generators like Docusaurus.
- **Alternatives Considered**:
  - **GitHub Pages**: Free and simple, but less flexible than Vercel for backend integrations (like the chatbot API).
  - **Netlify**: Very similar to Vercel, a solid alternative. Vercel is chosen for its strong focus on Next.js/React frameworks, which Docusaurus is built on.
  - **Self-hosting**: Provides full control but requires significant setup and maintenance overhead.

## 2. Backend and RAG Chatbot

- **Decision**: The backend for the RAG chatbot will be built with **Python and FastAPI**.
- **Rationale**: FastAPI is a modern, high-performance web framework for building APIs with Python. It's extremely fast, has automatic interactive documentation (Swagger UI), and is well-suited for ML/AI-powered applications. Python has a rich ecosystem of libraries for AI and data processing.
- **Alternatives Considered**:
  - **Node.js + Express**: A popular choice, but Python's ecosystem for AI/ML is more mature.

- **Decision**: Use **Qdrant** as the vector database.
- **Rationale**: The project spec explicitly mentions Qdrant. It is a high-performance, open-source vector similarity search engine. It offers a free cloud tier, which is perfect for this project's needs.
- **Alternatives Considered**: Pinecone, Weaviate. Qdrant is a solid choice and aligns with the spec.

- **Decision**: Use the **`all-MiniLM-L6-v2`** model from the Sentence Transformers library for generating embeddings.
- **Rationale**: This model provides a good balance of performance and quality. It's small, fast, and produces high-quality embeddings suitable for semantic search in a RAG system. It is also a widely used and well-documented open-source model.
- **Alternatives Considered**: OpenAI's `text-embedding-ada-002` (requires API calls and cost), larger models (more resource-intensive). `all-MiniLM-L6-v2` is a great starting point.

- **Decision**: Use a **custom-built chatbot widget using React**.
- **Rationale**: While plugins exist, building a custom widget provides maximum flexibility for styling and integration. It allows for a seamless user experience that matches the book's design philosophy. We can use a library like `react-chatbot-kit` as a starting point to accelerate development. The suggestion of `Biel.ai` in the prompt is noted, but a custom solution offers more control over the UX and data flow for a RAG system.
- **Alternatives Considered**:
  - **Biel.ai / Other third-party plugins**: These can be faster to set up but may offer less customization and might not be optimized for a custom RAG backend. A custom widget ensures tight integration with our FastAPI backend.

## 3. Version Control

- **Decision**: A **feature-branching workflow** will be used with a `main` branch for the source of truth and a `gh-pages` branch or Vercel's automated deployment for the built site.
- **Rationale**: This is a standard and effective Git workflow. `main` will contain all the Markdown content, Docusaurus configuration, and source code. Vercel will automatically build and deploy from the `main` branch upon merge. This keeps the development history clean and separates source from production assets.
- **Alternatives Considered**: Single branch (not recommended for collaboration or CI/CD), GitFlow (overly complex for this project).
