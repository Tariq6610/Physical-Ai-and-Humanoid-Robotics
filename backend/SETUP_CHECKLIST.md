# Database Setup Checklist for RAG Chatbot

## ✅ Already Done (No Action Needed)

### 1. Qdrant Vector Database
- [x] Qdrant Cloud URL configured in .env
- [x] API key configured
- [x] Collection 'book_content' exists with embeddings
- [x] Qdrant client initialized in code

### 2. SQLite Session Database  
- [x] SESSION_DB_PATH configured in .env
- [x] SQLiteSession will auto-create on first use
- [x] .gitignore includes conversations.db
- [x] Session manager wrapper created

## 🔧 Steps to Verify Everything Works

### Step 1: Check Environment Variables
```bash
cd backend
cat .env | grep -E "QDRANT|SESSION|GEMINI"
```

Expected output:
```
QDRANT_URL=https://47d341c9-5db4-480a-8532-64ef66c0e9c6...
QDRANT_API_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
QDRANT_COLLECTION_NAME=book_content
GEMINI_API_KEY=AIzaSyC1xMDaxhn-pNW4yyPOLPpfnBNOSqXhLYU
SESSION_DB_PATH=./conversations.db
SESSION_EXPIRY_HOURS=24
```

### Step 2: Test Qdrant Connection
```bash
cd backend
source .venv/bin/activate
python << 'PYTEST'
from src.services.embeddings import get_embedding_service
from src.agents.tools import get_qdrant_client

# Test embedding service
embedding_service = get_embedding_service()
test_vector = embedding_service.encode("test query")
print(f"✅ Embedding service works! Vector length: {len(test_vector)}")

# Test Qdrant connection
client = get_qdrant_client()
collections = client.get_collections()
print(f"✅ Qdrant connected! Collections: {[c.name for c in collections.collections]}")
PYTEST
```

### Step 3: Test Agent & Session Creation
```bash
cd backend
source .venv/bin/activate
python << 'PYTEST'
import asyncio
from src.agents import get_rag_agent, get_session_manager

# Test agent creation
agent = get_rag_agent()
print(f"✅ Agent created: {agent.name}")
print(f"   Tools: {[tool.name for tool in agent.tools]}")

# Test session manager
session_manager = get_session_manager()
session = session_manager.get_or_create_session("test_session_123")
print(f"✅ Session created/retrieved: test_session_123")

# Check if conversations.db was created
import os
db_exists = os.path.exists("./conversations.db")
print(f"✅ Database file exists: {db_exists}")
PYTEST
```

### Step 4: Test Full RAG Pipeline
```bash
cd backend
source .venv/bin/activate
python << 'PYTEST'
import asyncio
from src.services.rag_service import RAGService

async def test_rag():
    service = RAGService()
    
    # Test query without session
    response = await service.chat_async("What is Physical AI?")
    print(f"✅ RAG Response (no session):\n{response[:200]}...\n")
    
    # Test query with session
    response2 = await service.chat_async(
        "What is a humanoid robot?", 
        session_id="test_user_456"
    )
    print(f"✅ RAG Response (with session):\n{response2[:200]}...\n")
    
    # Test follow-up (should use session context)
    response3 = await service.chat_async(
        "What sensors does it use?", 
        session_id="test_user_456"
    )
    print(f"✅ Follow-up Response:\n{response3[:200]}...\n")

asyncio.run(test_rag())
PYTEST
```

### Step 5: Start Backend Server
```bash
cd backend
source .venv/bin/activate
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Step 6: Test API Endpoint
```bash
# In another terminal
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is Physical AI?"}'
```

Expected response:
```json
{
  "response": "Physical AI refers to...",
  "request_id": "uuid-here",
  "session_id": "uuid-here"
}
```

## 🗄️ Database File Locations

After first run, you'll see:

```
backend/
├── conversations.db          # ← Created automatically by SQLiteSession
├── conversations.db-journal  # ← SQLite transaction log (temporary)
└── .env                      # ← Your configuration
```

## 📊 Inspect Session Database (Optional)

```bash
cd backend
sqlite3 conversations.db

# View tables
.tables

# View sessions
SELECT * FROM sessions;

# View messages for a session
SELECT role, content, timestamp 
FROM messages 
WHERE session_id = 'test_user_456'
ORDER BY timestamp;

# Exit
.quit
```

## 🧹 Cleanup (If Needed)

To reset conversation history:
```bash
cd backend
rm conversations.db conversations.db-journal
# Will be recreated on next chat
```

## ❌ No External Database Setup Required

You do NOT need to:
- ❌ Install PostgreSQL/MySQL
- ❌ Run database migrations
- ❌ Create database schemas manually
- ❌ Set up Qdrant locally (using cloud)
- ❌ Install Redis or other cache

Everything is file-based (SQLite) or cloud-hosted (Qdrant)!
