# Quickstart Guide for Contributors

This guide provides instructions for setting up the local development environment for the "Physical AI and Humanoid Robotics" book project.

## Prerequisites

- **Node.js**: Version 20.x or higher.
- **Python**: Version 3.10 or higher.
- **Git**: For version control.

## 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-name>
```

## 2. Docusaurus Frontend Setup

The frontend is the Docusaurus site where the book content is written and displayed.

```bash
# Navigate to the docs directory
cd docs

# Install dependencies
npm install

# Run the local development server
npm run start
```

The Docusaurus site will now be running at `http://localhost:3000`. Changes to Markdown files in `docs/docs` will be reflected live.

## 3. Backend Chatbot Setup

The backend is a FastAPI application that powers the RAG chatbot.

```bash
# Navigate to the backend directory from the root
cd backend

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`

# Install Python dependencies
pip install -r requirements.txt
```

*(A `requirements.txt` file will be created containing all necessary dependencies like `fastapi`, `uvicorn`, `qdrant-client`, `sentence-transformers`, etc.)*

To run the backend server:

```bash
# Run the FastAPI development server
uvicorn src.main:app --reload
```

The backend API will be available at `http://localhost:8000`, with interactive documentation at `http://localhost:8000/docs`.

## 4. Content Ingestion

To populate the Qdrant vector database with the book's content, you need to run the ingestion script.

First, ensure you have a Qdrant instance running. You can use the free cloud tier from [Qdrant Cloud](https://cloud.qdrant.io/) or run it locally via Docker.

Set up the required environment variables. Create a `.env` file in the root of the repository:

```env
QDRANT_URL="your-qdrant-url"
QDRANT_API_KEY="your-qdrant-api-key"
```

Then run the ingestion script:

```bash
# From the root of the repository
cd scripts
python ingest.py
```

This will process all Markdown files and load them into your Qdrant collection.

## Contribution Workflow

1.  Create a new feature branch from `main`.
2.  Make your changes (e.g., write or edit a chapter, improve the chatbot).
3.  Commit your changes with a clear commit message.
4.  Push your branch to the remote repository.
5.  Open a Pull Request against the `main` branch.
6.  The PR will be reviewed, and once approved, merged into `main`, triggering a new deployment on Vercel.
