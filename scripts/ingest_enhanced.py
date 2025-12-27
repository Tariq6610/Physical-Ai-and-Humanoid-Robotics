"""
Enhanced Ingestion Script for Physical AI and Humanoid Robotics Book
Creates contextual embeddings that help the agent understand:
1. The book's overall structure and purpose
2. Chapter-level context for each chunk
3. Semantic relationships between topics
"""

import os
import glob
from qdrant_client import QdrantClient
from qdrant_client.http import models as qdrant_models
from sentence_transformers import SentenceTransformer
from typing import List, Dict
import logging
import uuid
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Book overview - this gives the agent contextual understanding
BOOK_OVERVIEW = """
This is the comprehensive documentation for "Physical AI and Humanoid Robotics: From Code to Consciousness".

ABOUT THIS BOOK:
This book is an expert-level guide to building intelligent humanoid robots using modern AI techniques.
It covers the complete journey from understanding robotics fundamentals to implementing advanced AI systems.

MAIN TOPICS COVERED:
1. Introduction to Physical AI and Modern Robotics
2. Robot Operating System (ROS and ROS2) - The foundation for robot software
3. NVIDIA Isaac Sim and Omniverse - Advanced simulation environments
4. Humanoid Robot Design - Mechanical structure, actuators, sensors
5. Perception Systems - Computer vision, LiDAR, sensor fusion
6. Kinematics and Dynamics - Robot motion mathematics
7. Motion Control and Planning - Trajectory generation, path planning
8. Navigation and SLAM - Mapping and localization
9. Manipulation and Grasping - Robot arms and hands
10. AI Integration - Machine learning for robotics
11. Reinforcement Learning - Training robots through experience
12. RAG Architecture - Retrieval-augmented generation for robotics

TARGET AUDIENCE:
- Robotics engineers and researchers
- AI/ML practitioners interested in physical systems
- Graduate students in robotics and AI
- Developers building autonomous systems

KEY TECHNOLOGIES:
- ROS/ROS2, Gazebo, NVIDIA Isaac Sim, Omniverse
- PyTorch, TensorFlow for AI/ML
- Computer vision (OpenCV, deep learning)
- Motion planning (MoveIt, OMPL)
- SLAM algorithms (gmapping, cartographer)
"""

# Chapter summaries for contextual embedding
CHAPTER_SUMMARIES = {
    "intro.md": "Introduction to the book on Physical AI and Humanoid Robotics, covering the scope and learning objectives.",
    "ch1-intro-ros.md": "Introduction to Robot Operating System (ROS), covering ROS concepts, nodes, topics, and the ROS ecosystem.",
    "ch2-ros2.md": "ROS2 fundamentals including DDS, Quality of Service, and migration from ROS1.",
    "ch3-isaac-sim.md": "NVIDIA Isaac Sim for robot simulation, including Omniverse platform and photorealistic rendering.",
    "ch4-humanoid-design.md": "Humanoid robot mechanical design, joints, actuators, and structural considerations.",
    "ch5-perception.md": "Robot perception systems including cameras, LiDAR, depth sensors, and sensor fusion.",
    "ch6-kinematics.md": "Robot kinematics - forward and inverse kinematics, Denavit-Hartenberg parameters.",
    "ch7-dynamics.md": "Robot dynamics, equations of motion, torque computation, and force control.",
    "ch8-control.md": "Motion control systems, PID control, trajectory tracking, and compliance control.",
    "ch9-navigation.md": "Robot navigation, path planning, obstacle avoidance, and global/local planners.",
    "ch10-slam.md": "Simultaneous Localization and Mapping (SLAM) algorithms and implementations.",
    "ch11-manipulation.md": "Robot manipulation, grasping, pick-and-place operations, and motion planning.",
    "ch12-ai-integration.md": "Integrating AI and machine learning with robotic systems.",
    "ch13-rag-architecture.md": "RAG (Retrieval-Augmented Generation) architecture for robotics applications.",
    "appendix-a-setup.md": "Setup guide for development environment, tools, and dependencies.",
    "appendix-b-glossary.md": "Glossary of robotics and AI terminology.",
}


def get_chapter_context(source_file: str) -> str:
    """Get chapter context for a source file."""
    base_name = os.path.basename(source_file)
    return CHAPTER_SUMMARIES.get(base_name, f"Content from {base_name}")


def create_contextual_chunk(text: str, source: str, section: str, chapter_context: str) -> str:
    """
    Create a contextually enriched version of the chunk for embedding.
    This helps the embedding model understand the context better.
    """
    # Prefix with chapter context to improve semantic matching
    contextual_text = f"""
From the book "Physical AI and Humanoid Robotics":
Chapter context: {chapter_context}
Section: {section}

Content:
{text}
"""
    return contextual_text.strip()


def chunk_text_enhanced(text: str, source_path: str, chunk_size: int = 800, overlap: int = 150) -> List[Dict]:
    """
    Enhanced chunking with better section detection and context preservation.
    Smaller chunks with more overlap for better retrieval.
    """
    lines = text.split('\n')
    sections = []
    current_section = {"title": "Introduction", "content": [], "level": 0}
    chapter_context = get_chapter_context(source_path)

    for line in lines:
        if line.startswith('#'):
            # Save previous section if it has content
            if current_section["content"]:
                sections.append(current_section)

            # Determine heading level
            level = len(line) - len(line.lstrip('#'))
            title = line.lstrip('# ').strip()
            current_section = {"title": title, "content": [], "level": level}
        else:
            # Skip empty lines at the start of sections
            if current_section["content"] or line.strip():
                current_section["content"].append(line)

    # Add the last section
    if current_section["content"]:
        sections.append(current_section)

    # Process chunks with context
    processed_chunks = []
    source_basename = os.path.basename(source_path)

    for section in sections:
        section_title = section["title"]
        section_content = '\n'.join(current_section["content"]).strip()

        if not section_content:
            continue

        section_text = '\n'.join(section["content"])

        # Break content into chunks
        start = 0
        chunk_index = 0
        while start < len(section_text):
            end = min(start + chunk_size, len(section_text))

            # Try to break at sentence boundary
            if end < len(section_text):
                # Look for sentence endings
                for sep in ['. ', '.\n', '! ', '!\n', '? ', '?\n']:
                    last_sep = section_text[start:end].rfind(sep)
                    if last_sep > chunk_size * 0.5:  # At least half the chunk
                        end = start + last_sep + len(sep)
                        break

            chunk_text_raw = section_text[start:end].strip()

            if chunk_text_raw:  # Only add non-empty chunks
                # Create contextual version for embedding
                contextual_text = create_contextual_chunk(
                    chunk_text_raw,
                    source_basename,
                    section_title,
                    chapter_context
                )

                processed_chunks.append({
                    "text": chunk_text_raw,  # Original text for display
                    "contextual_text": contextual_text,  # Enriched text for embedding
                    "source": source_basename,
                    "section": section_title,
                    "chapter_context": chapter_context,
                    "chunk_id": str(uuid.uuid4()),
                    "chunk_index": chunk_index
                })
                chunk_index += 1

            # Move to next chunk with overlap
            start = end - overlap if end < len(section_text) else end
            if start >= len(section_text):
                break

    return processed_chunks


def create_overview_chunks(embedding_model) -> List[qdrant_models.PointStruct]:
    """
    Create special overview chunks that help the agent understand the book holistically.
    These are embedded with high-level context for general queries.
    """
    overview_chunks = []

    # Main book overview
    overview_texts = [
        {
            "text": BOOK_OVERVIEW,
            "source": "_book_overview",
            "section": "Book Overview",
            "chapter_context": "Complete book overview and table of contents"
        },
        {
            "text": """
What is this book about?
This book, "Physical AI and Humanoid Robotics: From Code to Consciousness", is a comprehensive guide
to building intelligent humanoid robots. It covers everything from ROS basics to advanced AI integration,
including simulation with NVIDIA Isaac Sim, robot perception, kinematics, dynamics, navigation,
manipulation, and machine learning for robotics. Whether you want to learn about robot operating systems,
build simulations, understand robot motion, or integrate AI into physical robots, this book covers it all.
            """,
            "source": "_book_overview",
            "section": "About This Book",
            "chapter_context": "General introduction and book summary"
        },
        {
            "text": """
Table of Contents and Topics:
- Chapter 1: Introduction to ROS (Robot Operating System)
- Chapter 2: ROS2 and Modern Robotics
- Chapter 3: NVIDIA Isaac Sim and Omniverse Simulation
- Chapter 4: Humanoid Robot Design and Mechanics
- Chapter 5: Perception Systems (Vision, LiDAR, Sensors)
- Chapter 6: Kinematics (Robot Motion Mathematics)
- Chapter 7: Dynamics (Forces and Motion)
- Chapter 8: Motion Control Systems
- Chapter 9: Navigation and Path Planning
- Chapter 10: SLAM (Simultaneous Localization and Mapping)
- Chapter 11: Manipulation and Grasping
- Chapter 12: AI and Machine Learning Integration
- Chapter 13: RAG Architecture for Robotics
- Appendix A: Development Environment Setup
- Appendix B: Glossary of Terms
            """,
            "source": "_book_overview",
            "section": "Table of Contents",
            "chapter_context": "Book structure and chapter listing"
        }
    ]

    for item in overview_texts:
        contextual_text = f"""
Book: Physical AI and Humanoid Robotics
Context: {item['chapter_context']}

{item['text']}
        """
        embedding = embedding_model.encode(contextual_text).tolist()

        overview_chunks.append(qdrant_models.PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding,
            payload={
                "text": item["text"].strip(),
                "source": item["source"],
                "section": item["section"],
                "chapter_context": item["chapter_context"],
                "is_overview": True
            }
        ))

    return overview_chunks


def load_markdown_files(directory: str) -> List[Dict]:
    """Load all markdown files from directory."""
    documents = []
    for filepath in glob.glob(os.path.join(directory, '**/*.md'), recursive=True):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        documents.append({
            "content": content,
            "source_path": filepath
        })
    return documents


def ingest_content():
    """Main ingestion function with enhanced contextual embeddings."""
    # Environment variables
    qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
    qdrant_api_key = os.getenv("QDRANT_API_KEY", None)
    collection_name = os.getenv("QDRANT_COLLECTION_NAME", "book_content")
    embedding_model_name = os.getenv("EMBEDDING_MODEL_NAME", "all-MiniLM-L6-v2")

    # Initialize Qdrant client
    try:
        if qdrant_api_key:
            qdrant_client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key, timeout=30)
        else:
            qdrant_client = QdrantClient(host="localhost", port=6333, timeout=30)
        logger.info(f"Connected to Qdrant at {qdrant_url}")
    except Exception as e:
        logger.error(f"Failed to connect to Qdrant: {str(e)}")
        return

    # Initialize embedding model
    try:
        logger.info(f"Loading embedding model: {embedding_model_name}")
        embedding_model = SentenceTransformer(embedding_model_name)
        logger.info("Embedding model loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load embedding model: {str(e)}")
        return

    # Delete existing collection and recreate
    try:
        collections = qdrant_client.get_collections()
        if any(c.name == collection_name for c in collections.collections):
            logger.info(f"Deleting existing collection '{collection_name}'...")
            qdrant_client.delete_collection(collection_name)

        # Create new collection
        vector_size = embedding_model.get_sentence_embedding_dimension()
        logger.info(f"Creating collection '{collection_name}' with vector size {vector_size}")
        qdrant_client.create_collection(
            collection_name=collection_name,
            vectors_config=qdrant_models.VectorParams(
                size=vector_size,
                distance=qdrant_models.Distance.COSINE
            )
        )
    except Exception as e:
        logger.error(f"Failed to setup collection: {str(e)}")
        return

    # Load and process documents
    logger.info("Loading markdown files...")
    documents = load_markdown_files('docs/docs/')
    logger.info(f"Found {len(documents)} markdown files")

    points_to_upsert = []

    # Add overview chunks first
    logger.info("Creating book overview embeddings...")
    overview_points = create_overview_chunks(embedding_model)
    points_to_upsert.extend(overview_points)
    logger.info(f"Created {len(overview_points)} overview chunks")

    # Process document chunks
    total_chunks = 0
    for doc in documents:
        logger.info(f"Processing: {doc['source_path']}")
        chunks = chunk_text_enhanced(doc["content"], doc["source_path"])

        for chunk in chunks:
            try:
                # Embed the contextual text (enriched with chapter context)
                embedding = embedding_model.encode(chunk["contextual_text"]).tolist()

                points_to_upsert.append(qdrant_models.PointStruct(
                    id=chunk["chunk_id"],
                    vector=embedding,
                    payload={
                        "text": chunk["text"],  # Original text for display
                        "source": chunk["source"],
                        "section": chunk["section"],
                        "chapter_context": chunk["chapter_context"],
                        "is_overview": False
                    }
                ))
                total_chunks += 1

                if total_chunks % 50 == 0:
                    logger.info(f"Processed {total_chunks} chunks...")

            except Exception as e:
                logger.error(f"Error processing chunk: {str(e)}")
                continue

    # Upsert all points
    if points_to_upsert:
        logger.info(f"Upserting {len(points_to_upsert)} total points...")

        # Batch upsert for large collections
        batch_size = 100
        for i in range(0, len(points_to_upsert), batch_size):
            batch = points_to_upsert[i:i + batch_size]
            try:
                qdrant_client.upsert(
                    collection_name=collection_name,
                    wait=True,
                    points=batch
                )
                logger.info(f"Upserted batch {i//batch_size + 1}/{(len(points_to_upsert) + batch_size - 1)//batch_size}")
            except Exception as e:
                logger.error(f"Error upserting batch: {str(e)}")

        logger.info(f"Ingestion complete! Total: {len(points_to_upsert)} chunks ({len(overview_points)} overview + {total_chunks} content)")
    else:
        logger.info("No content to ingest.")


if __name__ == "__main__":
    ingest_content()
