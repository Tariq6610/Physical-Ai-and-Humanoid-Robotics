# Physical AI and Humanoid Robotics Book Project

This repository contains the source code and documentation for the "Physical AI and Humanoid Robotics" book project. It includes a Docusaurus-based documentation site, a FastAPI backend for a RAG-chatbot, and a content ingestion script.

## Project Structure

- `docs/`: Docusaurus documentation site (frontend)
- `backend/`: FastAPI application for the RAG-chatbot API
- `scripts/`: Python scripts, including the content ingestion script (`ingest.py`)
- `specs/`: Project specifications, plans, and tasks

## Local Development

### Prerequisites

- Node.js (v20.x or higher)
- Python (v3.10 or higher)
- Docker (optional, for local Qdrant)

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Backend Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

To run the backend:
```bash
uvicorn src.main:app --reload
```
The API will be available at `http://localhost:8000`, with interactive documentation at `http://localhost:8000/docs`.

### 3. Frontend Setup

```bash
cd docs
npm install
npm run start
```
The Docusaurus site will be running at `http://localhost:3000`.

### 4. Qdrant Setup (Local with Docker)

To run Qdrant locally using Docker:
```bash
docker run -p 6333:6333 -p 6334:6334 \
    -v $(pwd)/qdrant_storage:/qdrant/storage \
    qdrant/qdrant
```

### 5. Content Ingestion

Set up your `.env` file at the root of the repository:
```
QDRANT_URL="http://localhost:6333" # Or your Qdrant Cloud URL
QDRANT_API_KEY="" # Your Qdrant API Key if using Qdrant Cloud
```

Then run the ingestion script:
```bash
python scripts/ingest.py
```

## Deployment

### Render (Recommended)

This project is configured for deployment on Render. The `render.yaml` file defines the service configuration for both frontend and backend.

1. **Prerequisites**:
   - Qdrant Cloud account (or self-hosted Qdrant instance)
   - API keys for any external services (OpenAI, etc.)

2. **Deployment**:
   - Connect your GitHub repository to Render
   - Render will automatically detect the `render.yaml` configuration
   - Set the required environment variables as specified in `DEPLOYMENT.md`

3. **Configuration**:
   - Set `QDRANT_URL`, `QDRANT_API_KEY`, and `QDRANT_COLLECTION_NAME` for the backend
   - Set `BACKEND_URL` for the frontend to point to your deployed backend

For detailed deployment instructions, see `DEPLOYMENT.md`.

### Manual Deployment

For manual deployment options and alternative platforms, see `DEPLOYMENT.md`.

## Contributing

See `CONTRIBUTING.md` for guidelines.

## Release and Versioning Strategy

### Versioning Scheme

This project follows Semantic Versioning (SemVer) with the format MAJOR.MINOR.PATCH:

- **MAJOR** version: Incremented for incompatible API changes or major feature additions
- **MINOR** version: Incremented for backward-compatible feature additions
- **PATCH** version: Incremented for backward-compatible bug fixes

### Release Process

1. **Pre-release Preparation**:
   - All tasks in the current milestone must be completed and tested
   - Documentation must be updated to reflect new features
   - All tests must pass in the CI pipeline

2. **Version Bump**:
   - Update version numbers in relevant configuration files
   - Update any internal references to the version number

3. **Release Tagging**:
   - Create a Git tag with the format `vX.Y.Z`
   - Example: `git tag -a v1.2.3 -m "Release version 1.2.3"`

4. **Release Creation**:
   - Create a GitHub release with release notes
   - Include a summary of changes, new features, and bug fixes
   - Attach any relevant artifacts

### Release Cadence

- **Patch releases**: As needed for critical bug fixes
- **Minor releases**: Every 2-4 weeks for new features and improvements
- **Major releases**: Quarterly for significant architectural changes or major feature additions

### Branch Strategy

- `main` branch: Production-ready code, protected branch
- Feature branches: For development work, named as `feature/description`
- Release branches: For preparing releases, named as `release/vX.Y.Z`

### Quality Gates

All releases must pass:
- Automated tests (unit, integration, and end-to-end)
- Code review by at least one other team member
- Security scanning
- Performance benchmarks (where applicable)
