import os
import glob
from qdrant_client import QdrantClient, models
from qdrant_client.http import models as qdrant_models
from sentence_transformers import SentenceTransformer
from typing import List, Dict
import markdown
import logging
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

def chunk_text(text: str, source_path: str, chunk_size: int = 1000, overlap: int = 100) -> List[Dict]:
    """
    Parses markdown and chunks text into manageable pieces with overlap.
    Uses a more sophisticated approach than simple paragraph splitting.
    """
    # Parse markdown to extract sections and content
    lines = text.split('\n')
    sections = []
    current_section = {"title": "Introduction", "content": []}

    for line in lines:
        if line.startswith('#'):
            # Save previous section
            if current_section["content"]:
                sections.append(current_section)
            # Start new section
            level = len(line) - len(line.lstrip('#'))
            title = line.lstrip('# ').strip()
            current_section = {"title": title, "content": []}
        else:
            current_section["content"].append(line)

    # Add the last section
    if current_section["content"]:
        sections.append(current_section)

    # Now chunk each section
    processed_chunks = []
    for section in sections:
        section_title = section["title"]
        section_content = '\n'.join(section["content"])

        # Break content into chunks of specified size with overlap
        start = 0
        while start < len(section_content):
            end = start + chunk_size
            if end > len(section_content):
                end = len(section_content)

            chunk_text = section_content[start:end]

            processed_chunks.append({
                "text": chunk_text,
                "source": os.path.basename(source_path),
                "section": section_title,
                "chunk_id": str(uuid.uuid4())
            })

            # Move start forward by chunk_size - overlap
            start = end - overlap if end < len(section_content) else end

            # Break if we've reached the end
            if start >= len(section_content):
                break

    return processed_chunks

def ingest_content():
    # Environment variables for Qdrant connection
    qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
    qdrant_api_key = os.getenv("QDRANT_API_KEY", None)  # Can be None for local
    collection_name = os.getenv("QDRANT_COLLECTION_NAME", "book_content")
    embedding_model_name = os.getenv("EMBEDDING_MODEL_NAME", "all-MiniLM-L6-v2")

    # Initialize Qdrant client with real implementation
    try:
        if qdrant_api_key:
            qdrant_client = QdrantClient(
                url=qdrant_url,
                api_key=qdrant_api_key,
                timeout=30  # 30 second timeout
            )
        else:
            # For local development without API key
            qdrant_client = QdrantClient(
                host="localhost",
                port=6333,
                timeout=30
            )
    except Exception as e:
        logger.error(f"Failed to connect to Qdrant: {str(e)}")
        return

    # Initialize Sentence Transformer model with real implementation
    try:
        logger.info(f"Loading embedding model: {embedding_model_name}")
        embedding_model = SentenceTransformer(embedding_model_name)
        logger.info("Embedding model loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load embedding model: {str(e)}")
        return

    logger.info(f"Starting ingestion process for collection: {collection_name}")
    logger.info(f"Scanning markdown files in: docs/docs/")

    documents = load_markdown_files('docs/docs/')
    logger.info(f"Found {len(documents)} markdown files.")

    # Check if collection exists, create if it doesn't
    try:
        collections = qdrant_client.get_collections()
        collection_exists = any(collection.name == collection_name for collection in collections.collections)

        if not collection_exists:
            # Create collection with appropriate vector size (384 for all-MiniLM-L6-v2)
            vector_size = embedding_model.get_sentence_embedding_dimension()
            logger.info(f"Creating collection '{collection_name}' with vector size {vector_size}")
            qdrant_client.create_collection(
                collection_name=collection_name,
                vectors_config=qdrant_models.VectorParams(
                    size=vector_size,
                    distance=qdrant_models.Distance.COSINE
                )
            )
            logger.info(f"Collection '{collection_name}' created successfully")
        else:
            logger.info(f"Collection '{collection_name}' already exists")
    except Exception as e:
        logger.error(f"Failed to create or check collection: {str(e)}")
        return

    points_to_upsert = []
    total_chunks = 0

    for doc in documents:
        logger.info(f"Processing document: {doc['source_path']}")
        chunks = chunk_text(doc["content"], doc["source_path"])

        for chunk in chunks:
            try:
                # Generate embedding for each chunk
                embedding = embedding_model.encode(chunk["text"]).tolist()

                points_to_upsert.append(qdrant_models.PointStruct(
                    id=chunk["chunk_id"],  # Unique ID for each chunk
                    vector=embedding,
                    payload={
                        "text": chunk["text"],
                        "source": chunk["source"],
                        "section": chunk["section"]
                    }
                ))
                total_chunks += 1

                # Log progress every 10 chunks
                if total_chunks % 10 == 0:
                    logger.info(f"Processed {total_chunks} chunks so far...")

            except Exception as e:
                logger.error(f"Error processing chunk from {doc['source_path']}: {str(e)}")
                continue

    if points_to_upsert:
        logger.info(f"Upserting {len(points_to_upsert)} points into Qdrant collection '{collection_name}'...")
        try:
            qdrant_client.upsert(
                collection_name=collection_name,
                wait=True,  # Wait for the operation to be completed
                points=points_to_upsert
            )
            logger.info(f"Ingestion complete. Successfully ingested {len(points_to_upsert)} chunks.")
        except Exception as e:
            logger.error(f"Error during upsert operation: {str(e)}")
    else:
        logger.info("No content to ingest.")

if __name__ == "__main__":
    ingest_content()