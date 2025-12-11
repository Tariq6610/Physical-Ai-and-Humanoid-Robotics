import os
import glob
from qdrant_client import QdrantClient, models # Will need to install this
from sentence_transformers import SentenceTransformer # Will need to install this
from typing import List, Dict
import markdown

# Mock external dependencies for now
class MockQdrantClient:
    def __init__(self, url: str, api_key: str):
        print(f"MockQdrantClient initialized with url: {url}")
        print("NOTE: This is a mock Qdrant client. No actual data will be stored.")

    def upsert(self, collection_name: str, points: List[models.PointStruct], wait: bool = False):
        print(f"MockQdrantClient upserting {len(points)} points into collection: {collection_name}")
        for point in points:
            print(f"  Mock Upserted Point ID: {point.id}, Payload: {point.payload.get('source')}")

class MockSentenceTransformer:
    def __init__(self, model_name: str):
        print(f"MockSentenceTransformer initialized with model: {model_name}")
        print("NOTE: This is a mock Sentence Transformer. No actual embeddings will be generated.")

    def encode(self, text: str, convert_to_tensor: bool = False) -> List[float]:
        print(f"MockSentenceTransformer encoding text (first 50 chars): '{text[:50]}...'")
        # Return a mock embedding (e.g., a list of zeros)
        return [0.1] * 384 # common dimension for all-MiniLM-L6-v2

def load_markdown_files(directory: str) -> List[Dict]:
    """
    Scans the directory for markdown files and loads their content.
    """
    documents = []
    for filepath in glob.glob(os.path.join(directory, '**/*.md'), recursive=True):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        documents.append({
            "content": content,
            "source_path": filepath
        })
    return documents

def chunk_text(text: str, source_path: str) -> List[Dict]:
    """
    Parses markdown and chunks text into manageable pieces.
    For simplicity, this mock implementation will treat each paragraph as a chunk.
    In a real scenario, more sophisticated chunking would be used (e.g., based on headings, token limits).
    """
    html = markdown.markdown(text)
    # Simple chunking by paragraphs (can be improved)
    chunks = html.split('<p>')
    processed_chunks = []
    for i, chunk in enumerate(chunks):
        clean_text = chunk.strip().replace('</p>', '').replace('\n', ' ')
        if clean_text:
            # Attempt to extract a simple section/heading from the markdown.
            # This is a very naive approach and should be improved for real use.
            section = "Unknown Section"
            if '#' in text:
                first_heading_match = text.split('\n')[0]
                if first_heading_match.startswith('#'):
                    section = first_heading_match.lstrip('# ').strip()

            processed_chunks.append({
                "text": clean_text,
                "source": os.path.basename(source_path),
                "section": section,
                "chunk_id": f"{os.path.basename(source_path)}_{i}"
            })
    return processed_chunks

def ingest_content():
    # Environment variables for Qdrant connection
    qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
    qdrant_api_key = os.getenv("QDRANT_API_KEY", None) # Can be None for local
    collection_name = os.getenv("QDRANT_COLLECTION_NAME", "book_content")
    
    # Initialize Qdrant client (using mock for now)
    # For real usage: qdrant_client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
    qdrant_client = MockQdrantClient(url=qdrant_url, api_key=qdrant_api_key)

    # Initialize Sentence Transformer model (using mock for now)
    # For real usage: embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    embedding_model = MockSentenceTransformer('all-MiniLM-L6-v2')

    print(f"Starting ingestion process for collection: {collection_name}")
    print(f"Scanning markdown files in: docs/docs/")

    documents = load_markdown_files('docs/docs/')
    print(f"Found {len(documents)} markdown files.")

    points_to_upsert = []
    for doc in documents:
        print(f"Processing document: {doc['source_path']}")
        chunks = chunk_text(doc["content"], doc["source_path"])
        
        for chunk in chunks:
            # Generate embedding for each chunk
            embedding = embedding_model.encode(chunk["text"])
            
            points_to_upsert.append(models.PointStruct(
                id=chunk["chunk_id"], # Unique ID for each chunk
                vector=embedding,
                payload={
                    "text": chunk["text"],
                    "source": chunk["source"],
                    "section": chunk["section"]
                }
            ))
    
    if points_to_upsert:
        print(f"Upserting {len(points_to_upsert)} points into Qdrant collection '{collection_name}'...")
        qdrant_client.upsert(
            collection_name=collection_name,
            wait=True, # Wait for the operation to be completed
            points=points_to_upsert
        )
        print("Ingestion complete.")
    else:
        print("No content to ingest.")

if __name__ == "__main__":
    ingest_content()