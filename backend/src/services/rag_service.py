import os
from typing import List, Dict

# Mock external dependencies for now
class MockQdrantClient:
    def __init__(self, host: str, api_key: str):
        print(f"MockQdrantClient initialized with host: {host}")

    def search(self, collection_name: str, query_vector: List[float], limit: int) -> List[Dict]:
        print(f"MockQdrantClient searching collection: {collection_name} with query vector (first 5 elements): {query_vector[:5]}")
        # Return mock results
        return [
            {"id": "mock_id_1", "payload": {"text": "Mock context for ROS 2 nodes.", "source": "ch2-ros-nodes-topics.md", "section": "ROS 2 Nodes"}},
            {"id": "mock_id_2", "payload": {"text": "Mock context for communication patterns.", "source": "ch2-ros-nodes-topics.md", "section": "Communication Patterns"}}
        ]

class MockSentenceTransformer:
    def encode(self, text: str, convert_to_tensor: bool = False) -> List[float]:
        print(f"MockSentenceTransformer encoding text: '{text}'")
        # Return a mock embedding (e.g., a list of zeros or simple hash)
        return [0.1] * 384 # common dimension for all-MiniLM-L6-v2

class MockLLMClient:
    def generate_response(self, prompt: str) -> str:
        print(f"MockLLMClient generating response for prompt: '{prompt}'")
        # Return a mock LLM response
        return "This is a mock LLM response based on your query and retrieved context."


class RAGService:
    def __init__(self):
        # Initialize Qdrant client (mocked for now)
        qdrant_host = os.getenv("QDRANT_URL", "http://localhost:6333")
        qdrant_api_key = os.getenv("QDRANT_API_KEY", "mock-api-key")
        self.qdrant_client = MockQdrantClient(host=qdrant_host, api_key=qdrant_api_key)
        self.collection_name = os.getenv("QDRANT_COLLECTION_NAME", "book_content")

        # Initialize Sentence Transformer for embeddings (mocked for now)
        self.embedding_model = MockSentenceTransformer()

        # Initialize LLM client (mocked for now)
        self.llm_client = MockLLMClient()

    def get_query_embedding(self, query: str) -> List[float]:
        return self.embedding_model.encode(query)

    def retrieve_context(self, query_embedding: List[float]) -> List[Dict]:
        # In a real scenario, adjust limit and filtering based on desired context size
        return self.qdrant_client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=5 # Retrieve top 5 relevant chunks
        )

    def generate_answer(self, query: str, context: List[Dict]) -> str:
        context_str = "\n".join([chunk["payload"]["text"] for chunk in context])
        
        # This prompt template should be refined, but serves as a basic example
        prompt = (
            "You are an AI assistant for a book on Physical AI and Humanoid Robotics.\n"
            "Answer the user's question ONLY based on the provided context. "
            "If the answer is not in the context, state that you don't know.\n\n"
            "Context:\n"
            f"{context_str}\n\n"
            f"Question: {query}\n"
            "Answer:"
        )
        return self.llm_client.generate_response(prompt)

    def chat(self, query: str) -> str:
        # 1. Generate query embedding
        query_embedding = self.get_query_embedding(query)

        # 2. Retrieve relevant context from Qdrant
        context = self.retrieve_context(query_embedding)

        # 3. Generate answer using LLM
        answer = self.generate_answer(query, context)
        
        return answer