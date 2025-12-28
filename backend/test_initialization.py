"""
Test backend initialization to identify 500 error cause
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("="*60)
print("Testing Backend Initialization")
print("="*60 + "\n")

# Test 1: Environment variables
print("1. Checking Environment Variables...")
required_vars = [
    "GEMINI_API_KEY",
    "QDRANT_URL",
    "QDRANT_API_KEY",
    "QDRANT_COLLECTION_NAME",
    "EMBEDDING_MODEL_NAME"
]

all_vars_present = True
for var in required_vars:
    value = os.getenv(var)
    if value:
        # Mask sensitive values
        if "KEY" in var or "SECRET" in var:
            display_value = value[:10] + "..." if len(value) > 10 else "***"
        else:
            display_value = value
        print(f"   ✅ {var}: {display_value}")
    else:
        print(f"   ❌ {var}: NOT SET")
        all_vars_present = False

if not all_vars_present:
    print("\n❌ Missing required environment variables!")
    sys.exit(1)

print("\n✅ All environment variables present\n")

# Test 2: Import core config
print("2. Testing Core Config Import...")
try:
    from src.core.config import get_settings
    settings = get_settings()
    print(f"   ✅ Config loaded successfully")
    print(f"   Model: {settings.llm_model}")
    print(f"   Collection: {settings.qdrant_collection_name}")
except Exception as e:
    print(f"   ❌ Config import failed: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 3: Qdrant connection
print("\n3. Testing Qdrant Connection...")
try:
    from qdrant_client import QdrantClient
    client = QdrantClient(
        url=settings.qdrant_url,
        api_key=settings.qdrant_api_key,
        timeout=10
    )
    collections = client.get_collections()
    print(f"   ✅ Connected to Qdrant")
    print(f"   Collections: {[c.name for c in collections.collections]}")

    # Check if our collection exists
    if settings.qdrant_collection_name in [c.name for c in collections.collections]:
        info = client.get_collection(settings.qdrant_collection_name)
        print(f"   ✅ Collection '{settings.qdrant_collection_name}' found")
        print(f"   Points: {info.points_count}")
    else:
        print(f"   ❌ Collection '{settings.qdrant_collection_name}' NOT FOUND!")
except Exception as e:
    print(f"   ❌ Qdrant connection failed: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Embedding service
print("\n4. Testing Embedding Service...")
try:
    from src.services.embeddings import get_embedding_service
    embedding_service = get_embedding_service()
    print(f"   ✅ Embedding service initialized")

    # Test encoding
    test_text = "What is Physical AI?"
    embedding = embedding_service.encode(test_text)
    print(f"   ✅ Test encoding successful (dim: {len(embedding)})")
except Exception as e:
    print(f"   ❌ Embedding service failed: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 5: Agent creation
print("\n5. Testing RAG Agent Creation...")
try:
    from src.agents import create_rag_agent
    agent = create_rag_agent()
    print(f"   ✅ RAG agent created successfully")
    print(f"   Agent name: {agent.name}")
    print(f"   Tools: {len(agent.tools)}")
except Exception as e:
    print(f"   ❌ Agent creation failed: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 6: RAG Service initialization
print("\n6. Testing RAG Service...")
try:
    from src.services.rag_service import RAGService
    rag_service = RAGService()
    print(f"   ✅ RAG service initialized")
except Exception as e:
    print(f"   ❌ RAG service failed: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 7: Session manager
print("\n7. Testing Session Manager...")
try:
    from src.agents import get_session_manager
    session_manager = get_session_manager()
    print(f"   ✅ Session manager initialized")
except Exception as e:
    print(f"   ❌ Session manager failed: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "="*60)
print("✅ ALL TESTS PASSED!")
print("Backend should be able to start successfully.")
print("="*60)
