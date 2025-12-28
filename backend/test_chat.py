"""
Test chat functionality end-to-end
"""
import asyncio
from src.services.rag_service import RAGService

async def test_chat():
    print("="*60)
    print("Testing RAG Chat Functionality")
    print("="*60 + "\n")

    try:
        # Initialize RAG service
        print("1. Initializing RAG service...")
        rag_service = RAGService()
        print("   ✅ RAG service initialized\n")

        # Test query
        test_query = "What is Physical AI?"
        print(f"2. Testing chat with query: '{test_query}'")
        print("   (This may take 10-30 seconds...)\n")

        response = await rag_service.chat_async(test_query)

        print("="*60)
        print("✅ CHAT TEST SUCCESSFUL!")
        print("="*60)
        print(f"\nQuery: {test_query}")
        print(f"\nResponse:\n{response}\n")
        print("="*60)

        return True

    except Exception as e:
        print("="*60)
        print("❌ CHAT TEST FAILED!")
        print("="*60)
        print(f"\nError: {str(e)}\n")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_chat())
    exit(0 if success else 1)
