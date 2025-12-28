"""
Check if embeddings are properly loaded in Qdrant
"""
import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient

# Load environment variables
load_dotenv()

def check_qdrant_collection():
    """Check the status of the Qdrant collection"""

    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")
    collection_name = os.getenv("QDRANT_COLLECTION_NAME", "book_content")

    print(f"Connecting to Qdrant at: {qdrant_url}")
    print(f"Collection name: {collection_name}\n")

    try:
        # Initialize Qdrant client
        client = QdrantClient(
            url=qdrant_url,
            api_key=qdrant_api_key,
            timeout=10
        )

        # Check if collection exists
        collections = client.get_collections()
        collection_names = [col.name for col in collections.collections]

        print(f"Available collections: {collection_names}")

        if collection_name not in collection_names:
            print(f"\n❌ Collection '{collection_name}' does NOT exist!")
            print("Run the ingestion script to create embeddings.")
            return False

        # Get collection info
        collection_info = client.get_collection(collection_name)
        print(f"\n✅ Collection '{collection_name}' exists!")
        print(f"   Vector size: {collection_info.config.params.vectors.size}")
        print(f"   Distance metric: {collection_info.config.params.vectors.distance}")
        print(f"   Total points (documents): {collection_info.points_count}")
        print(f"   Status: {collection_info.status}")

        if collection_info.points_count == 0:
            print("\n⚠️  WARNING: Collection exists but has 0 documents!")
            print("Run the ingestion script to populate the collection.")
            return False

        # Test a simple query to verify embeddings work
        print("\n🔍 Testing a sample query...")
        from src.services.embeddings import get_embedding_service

        embedding_service = get_embedding_service()
        test_query = "What is Physical AI?"
        query_vector = embedding_service.encode(test_query)

        results = client.query_points(
            collection_name=collection_name,
            query=query_vector,
            limit=3
        ).points

        if results:
            print(f"✅ Query successful! Found {len(results)} results for '{test_query}'")
            print("\nTop result:")
            print(f"   Score: {results[0].score:.4f}")
            print(f"   Source: {results[0].payload.get('source', 'N/A')}")
            print(f"   Text preview: {results[0].payload.get('text', '')[:100]}...")
            return True
        else:
            print("⚠️  No results found for test query")
            return False

    except Exception as e:
        print(f"\n❌ Error checking collection: {str(e)}")
        return False

if __name__ == "__main__":
    print("="*60)
    print("Checking Qdrant Embeddings Status")
    print("="*60 + "\n")

    success = check_qdrant_collection()

    print("\n" + "="*60)
    if success:
        print("✅ EMBEDDINGS ARE READY!")
        print("The chatbot can retrieve documentation successfully.")
    else:
        print("❌ EMBEDDINGS NEED ATTENTION!")
        print("Please run the ingestion script to create/update embeddings.")
    print("="*60)
