# Quickstart: RAG Chatbot Recreation Development

**Feature**: 001-rag-chatbot-recreation
**Date**: 2025-12-26
**For**: Developers implementing the recreated RAG chatbot

---

## Prerequisites

Before starting development, ensure you have:

- **Python 3.11+** installed
- **Node.js 18+** and npm installed
- **Git** repository cloned and on branch `001-rag-chatbot-recreation`
- **API Keys** configured:
  - Google Gemini API key (free tier from https://makersuite.google.com/app/apikey)
  - Qdrant Cloud URL and API key (existing)
- **Context7 MCP** server access (mandatory for framework documentation)

---

## Backend Setup

### 1. Install Dependencies

```bash
cd backend

# Install OpenAI Agents SDK with LiteLLM support
pip install "openai-agents[litellm]"

# Install existing dependencies (FastAPI, Qdrant, etc.)
pip install -r requirements.txt
```

**Updated `requirements.txt`** should include:
```text
openai-agents[litellm]>=0.2.9
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
qdrant-client>=1.7.0
sentence-transformers>=2.2.2
pydantic>=2.5.0
python-jose[cryptography]>=3.3.0
slowapi>=0.1.9
```

### 2. Configure Environment Variables

Create/update `backend/.env`:

```bash
# LLM Configuration
GEMINI_API_KEY=your-gemini-api-key-here
LLM_PROVIDER=gemini
LLM_MODEL=gemini/gemini-2.0-flash

# Vector Database (existing)
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=your-qdrant-key
QDRANT_COLLECTION=robotics_docs

# Session Management (new)
SESSION_DB_PATH=./conversations.db
SESSION_EXPIRY_HOURS=24

# CORS (for production)
FRONTEND_URL_DEV=http://localhost:3000
FRONTEND_URL_PROD=https://physical-ai-robotics-docs.onrender.com

# API Configuration
API_RATE_LIMIT=15  # Gemini free tier limit per minute
```

### 3. Initialize Session Database

```bash
# Create conversations.db (SQLiteSession will auto-initialize schema)
touch conversations.db

# Add to .gitignore
echo "conversations.db" >> .gitignore
```

### 4. Create Agent Module Structure

```bash
mkdir -p src/agents
touch src/agents/__init__.py
touch src/agents/rag_agent.py
touch src/agents/tools.py
touch src/agents/session_manager.py
```

### 5. Verify Qdrant Connection

```bash
# Quick test script
python -c "
from qdrant_client import QdrantClient
import os
from dotenv import load_dotenv

load_dotenv()
client = QdrantClient(url=os.getenv('QDRANT_URL'), api_key=os.getenv('QDRANT_API_KEY'))
collections = client.get_collections()
print(f'Connected! Collections: {[c.name for c in collections.collections]}')
"
```

Expected output: `Connected! Collections: ['robotics_docs']`

### 6. Run Development Server

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

**Verify health endpoint**:
```bash
curl http://localhost:8000/health
```

---

## Frontend Setup

### 1. Install Dependencies

```bash
cd docs

# Install ChatKit
npm install @openai/chatkit-react

# Install existing dependencies
npm install
```

**Updated `package.json`** should include:
```json
{
  "dependencies": {
    "@openai/chatkit-react": "^latest",
    "@docusaurus/core": "3.3.2",
    "@docusaurus/preset-classic": "3.3.2",
    "react": "^18.0.0",
    "react-dom": "^18.0.0"
  }
}
```

### 2. Create ChatKit Component Structure

```bash
mkdir -p src/components/ChatbotWidget
touch src/components/ChatbotWidget/index.tsx
touch src/components/ChatbotWidget/config.ts

# Create utility for backend URL
mkdir -p src/utils
touch src/utils/env.ts
```

### 3. Remove Old Widget

```bash
# Backup first (optional)
mv src/components/ChatbotWidget.tsx src/components/ChatbotWidget.tsx.backup
mv src/components/ChatbotWidget.module.css src/components/ChatbotWidget.module.css.backup

# Or delete directly
rm src/components/ChatbotWidget.tsx
rm src/components/ChatbotWidget.module.css
```

### 4. Run Development Server

```bash
npm start
```

**Verify** at: http://localhost:3000

---

## Integration Testing

### 1. Test Backend Agent

```bash
cd backend

# Run unit tests for Agent setup
pytest tests/unit/test_agents.py -v

# Run integration tests for RAG pipeline
pytest tests/integration/test_rag_pipeline.py -v
```

### 2. Test Frontend ChatKit

```bash
cd docs

# Run component tests
npm test -- ChatbotWidget.test.tsx
```

### 3. Test End-to-End

1. **Start Backend**: `cd backend && uvicorn src.main:app --reload`
2. **Start Frontend**: `cd docs && npm start`
3. **Open Browser**: http://localhost:3000
4. **Click Chat Widget**: Should see ChatKit interface
5. **Send Message**: "What is Physical AI?"
6. **Verify**:
   - Response appears within 3 seconds
   - Markdown rendered correctly
   - Source citations displayed
   - Follow-up question maintains context

---

## Common Development Tasks

### Query Context7 for Framework Help

**During Development**: Use Context7 MCP to get up-to-date code examples

```bash
# Example: Get OpenAI Agents SDK session management docs
# (Use your IDE's MCP integration or Claude Code CLI)

# For Python backend patterns
Context7 Query: /openai/openai-agents-python
Topic: "session management SQLiteSession conversation history"

# For ChatKit React patterns
Context7 Query: /openai/chatkit-js
Topic: "custom backend getClientSecret authentication"
```

### Debug Session Issues

```bash
# View SQLiteSession database
sqlite3 backend/conversations.db

# List all sessions
SELECT session_id, created_at, last_activity_at FROM sessions;

# View messages for a session
SELECT role, content, timestamp FROM messages WHERE session_id = 'your-session-id';

# Clear expired sessions
DELETE FROM sessions WHERE last_activity_at < datetime('now', '-24 hours');
```

### Test Gemini API Connection

```bash
cd backend
python -c "
from agents.extensions.models.litellm_model import LitellmModel
from agents import Agent, Runner
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

agent = Agent(
    name='Test',
    model=LitellmModel(
        model='gemini/gemini-2.0-flash',
        api_key=os.getenv('GEMINI_API_KEY')
    )
)

async def test():
    result = await Runner.run(agent, 'Say hello')
    print(result.final_output)

asyncio.run(test())
"
```

Expected output: Gemini's greeting response

### Check Rate Limits

```bash
# Monitor Gemini API rate limit (15 req/min free tier)
# Watch FastAPI logs for rate limit warnings

tail -f backend/logs/app.log | grep "rate_limit"
```

---

## Deployment to Render

### Backend Deployment

1. **Push to Git**: Ensure branch `001-rag-chatbot-recreation` is pushed
2. **Render Dashboard**: Create new Web Service
3. **Build Command**: `pip install -r requirements.txt`
4. **Start Command**: `uvicorn src.main:app --host 0.0.0.0 --port $PORT`
5. **Environment Variables**: Add all variables from `.env` in Render dashboard
6. **Persistent Disk**: Mount `/conversations.db` for session storage

### Frontend Deployment

1. **Push to Git**: Ensure updated code is pushed
2. **Render Dashboard**: Update Static Site (already exists)
3. **Build Command**: `npm install && npm run build`
4. **Publish Directory**: `build`
5. **Auto-Deploy**: Enable on branch `001-rag-chatbot-recreation`

### Post-Deployment Verification

```bash
# Test production backend health
curl https://physical-ai-backend.onrender.com/health

# Test production frontend
# Open: https://physical-ai-robotics-docs.onrender.com
# Click chat widget, send test message
```

---

## Troubleshooting

### Issue: "ChatKit widget not appearing"

**Solution**:
- Check browser console for JavaScript errors
- Verify `@openai/chatkit-react` installed: `npm list @openai/chatkit-react`
- Ensure BrowserOnly wrapper in Root.tsx
- Check Docusaurus build succeeded without errors

### Issue: "Backend connection failed"

**Solution**:
- Check `getBackendURL()` returns correct URL
- Verify CORS configured in FastAPI main.py
- Check browser Network tab for failed requests
- Confirm backend is running and accessible

### Issue: "No response from Gemini"

**Solution**:
- Verify `GEMINI_API_KEY` set correctly in `.env`
- Check Gemini API quota/rate limits
- Review backend logs for LiteLLM errors
- Test with sample query: `curl -X POST http://localhost:8000/chat -d '{"query":"test"}'`

### Issue: "Session not persisting"

**Solution**:
- Check `conversations.db` file permissions (writeable)
- Verify `SESSION_DB_PATH` environment variable
- Check sessionStorage in browser DevTools (should have `chatkit_session_id`)
- Review SQLiteSession initialization code

---

## Next Steps

After quickstart setup is complete:

1. **Run `/sp.tasks`**: Generate implementation tasks from this plan
2. **Review Tasks**: Ensure task order respects TDD (tests before implementation)
3. **Run `/sp.implement`**: Execute tasks in dependency order
4. **Run `/sp.git.commit_pr`**: Commit changes and create pull request

---

## References

- **OpenAI Agents SDK Docs**: Query Context7 `/openai/openai-agents-python`
- **ChatKit Docs**: Query Context7 `/openai/chatkit-js`
- **Spec**: `specs/001-rag-chatbot-recreation/spec.md`
- **Plan**: `specs/001-rag-chatbot-recreation/plan.md`
- **Data Model**: `specs/001-rag-chatbot-recreation/data-model.md`
- **API Contracts**: `specs/001-rag-chatbot-recreation/contracts/`
