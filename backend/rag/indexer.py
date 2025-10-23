"""
PDF Indexer for Voice Acting Knowledge Base

Loads PDF books (Stanislavski and Linklater) and indexes them
into Pinecone vector store using LlamaIndex.

Features concurrent embedding generation with semaphore-based rate limiting.
"""
import os
import logging
import asyncio
from pathlib import Path
from typing import List, Tuple
from pinecone import Pinecone, ServerlessSpec
from llama_index.core import SimpleDirectoryReader, Settings, VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.vector_stores.pinecone import PineconeVectorStore

logger = logging.getLogger(__name__)


async def generate_embedding_with_retry(
    embed_model: OpenAIEmbedding,
    content: str,
    chunk_id: int,
    semaphore: asyncio.Semaphore,
    max_retries: int = 3,
) -> Tuple[int, List[float] | None]:
    """
    Generate embedding with retry logic and semaphore-based concurrency control.

    Args:
        embed_model: OpenAI embedding model
        content: Text content to embed
        chunk_id: Chunk identifier
        semaphore: Asyncio semaphore for rate limiting
        max_retries: Maximum retry attempts (default: 3)

    Returns:
        Tuple of (chunk_id, embedding_vector) or (chunk_id, None) on failure
    """
    async with semaphore:
        for attempt in range(max_retries):
            try:
                # Get embedding asynchronously
                embedding = await embed_model.aget_text_embedding(content)
                return (chunk_id, embedding)
            except Exception as e:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt  # Exponential backoff: 1s, 2s, 4s
                    logger.warning(
                        f"Embedding failed for chunk {chunk_id} (attempt {attempt + 1}/{max_retries}): {e}. "
                        f"Retrying in {wait_time}s..."
                    )
                    await asyncio.sleep(wait_time)
                else:
                    logger.error(f"Embedding failed for chunk {chunk_id} after {max_retries} attempts: {e}")
                    return (chunk_id, None)

    return (chunk_id, None)


async def _generate_embeddings_concurrent(
    embed_model: OpenAIEmbedding,
    chunks: List[Tuple[int, str, dict]],
    max_concurrent: int = 20,
) -> List[Tuple[int, List[float] | None]]:
    """
    Generate embeddings for all chunks concurrently with semaphore limiting.

    Args:
        embed_model: OpenAI embedding model
        chunks: List of (chunk_id, content, metadata) tuples
        max_concurrent: Maximum concurrent requests (default: 20)

    Returns:
        List of (chunk_id, embedding) tuples
    """
    semaphore = asyncio.Semaphore(max_concurrent)

    # Create tasks for all embeddings
    tasks = [
        generate_embedding_with_retry(embed_model, content, i, semaphore)
        for i, (chunk_id, content, metadata) in enumerate(chunks)
    ]

    # Run all tasks concurrently (semaphore limits actual concurrency)
    logger.info(f"Starting concurrent embedding generation for {len(tasks)} chunks...")
    embeddings = await asyncio.gather(*tasks)

    logger.info(f"✅ Completed {len(embeddings)} embeddings")
    return embeddings


def index_voice_acting_books(
    pdf_dir: str | Path = None,
    pinecone_api_key: str = None,
    pinecone_index_name: str = None,
    openai_api_key: str = None,
    chunk_size: int = 512,
    chunk_overlap: int = 50,
) -> VectorStoreIndex:
    """
    Index voice acting PDF books into Pinecone vector store.

    Args:
        pdf_dir: Directory containing PDF files (default: data/pdfs)
        pinecone_api_key: Pinecone API key (default: from env)
        pinecone_index_name: Pinecone index name (default: from env)
        openai_api_key: OpenAI API key (default: from env)
        chunk_size: Chunk size in tokens (default: 512)
        chunk_overlap: Chunk overlap in tokens (default: 50)

    Returns:
        VectorStoreIndex: The created/updated index
    """
    # Get configuration from environment if not provided
    pinecone_api_key = pinecone_api_key or os.getenv("PINECONE_API_KEY")
    pinecone_index_name = pinecone_index_name or os.getenv("PINECONE_INDEX_NAME")
    openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")

    if not all([pinecone_api_key, pinecone_index_name, openai_api_key]):
        raise ValueError("Missing required API keys or index name in environment")

    # Default PDF directory
    if pdf_dir is None:
        pdf_dir = Path(__file__).parent.parent / "data" / "pdfs"
    else:
        pdf_dir = Path(pdf_dir)

    logger.info(f"Loading PDFs from: {pdf_dir}")

    # Initialize Pinecone
    pc = Pinecone(api_key=pinecone_api_key)

    # Create index if doesn't exist
    if pinecone_index_name not in pc.list_indexes().names():
        logger.info(f"Creating Pinecone index: {pinecone_index_name}")
        pc.create_index(
            name=pinecone_index_name,
            dimension=3072,  # OpenAI text-embedding-3-large dimension
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )
        logger.info("Index created successfully")
    else:
        logger.info(f"Using existing Pinecone index: {pinecone_index_name}")

    pinecone_index = pc.Index(pinecone_index_name)

    # Configure LlamaIndex settings
    embed_model = OpenAIEmbedding(
        model="text-embedding-3-large",
        api_key=openai_api_key,
    )
    Settings.embed_model = embed_model
    Settings.chunk_size = chunk_size
    Settings.chunk_overlap = chunk_overlap

    # Load PDFs
    logger.info("Loading PDF documents...")
    documents = SimpleDirectoryReader(
        input_dir=str(pdf_dir),
        required_exts=[".pdf"],
        recursive=False,
    ).load_data()

    logger.info(f"Loaded {len(documents)} document pages")

    # Add metadata to documents
    for doc in documents:
        filename = doc.metadata.get("file_name", "").lower()

        if "handbook" in filename and "volume 1" in filename:
            doc.metadata.update(
                {
                    "author": "AI-Generated",
                    "title": "The Voice Director's Handbook Volume 1",
                    "year": 2025,
                    "book": "Voice Director's Handbook Vol 1",
                }
            )
        elif "handbook" in filename and "volume 2" in filename:
            doc.metadata.update(
                {
                    "author": "AI-Generated",
                    "title": "The Voice Director's Handbook Volume 2",
                    "year": 2025,
                    "book": "Voice Director's Handbook Vol 2",
                }
            )
        elif "actor" in filename or "stanislavski" in filename:
            doc.metadata.update(
                {
                    "author": "Constantin Stanislavski",
                    "title": "An Actor Prepares",
                    "year": 1936,
                    "book": "An Actor Prepares",
                }
            )
        elif "voice" in filename or "linklater" in filename:
            doc.metadata.update(
                {
                    "author": "Kristin Linklater",
                    "title": "Freeing the Natural Voice",
                    "year": 2006,
                    "book": "Freeing the Natural Voice",
                }
            )

    # Create sentence splitter for better chunking
    node_parser = SentenceSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    # Parse documents into nodes/chunks
    logger.info("Chunking documents...")
    nodes = node_parser.get_nodes_from_documents(documents, show_progress=True)
    logger.info(f"Created {len(nodes)} chunks")

    # Generate embeddings concurrently with semaphore (max 20 concurrent)
    logger.info("Generating embeddings concurrently (max 20 at a time)...")

    # Prepare valid chunks
    valid_chunks = []
    skipped_count = 0

    for i, node in enumerate(nodes):
        # Get content and clean it
        content = node.get_content()

        # Skip if empty or too short
        if not content or len(content.strip()) < 10:
            logger.warning(f"Skipping chunk {i}: too short or empty")
            skipped_count += 1
            continue

        # Truncate if too long (OpenAI has 8191 token limit)
        # Roughly 4 chars per token, so limit to ~30k chars to be safe
        if len(content) > 30000:
            logger.warning(f"Truncating chunk {i}: {len(content)} chars")
            content = content[:30000]

        valid_chunks.append((i, content, node.metadata))

    logger.info(f"Processing {len(valid_chunks)} valid chunks...")

    # Run async embedding generation with semaphore
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        embeddings = loop.run_until_complete(
            _generate_embeddings_concurrent(embed_model, valid_chunks)
        )
    finally:
        loop.close()

    # Prepare vectors for upload
    logger.info("Preparing vectors for Pinecone upload...")
    vectors_to_upsert = []

    for chunk_id, embedding in embeddings:
        if embedding is None:
            logger.warning(f"Skipping chunk {chunk_id}: embedding generation failed")
            skipped_count += 1
            continue

        # Get original chunk data
        original_idx, content, metadata_dict = valid_chunks[chunk_id]

        # Prepare metadata (ensure all values are strings/numbers/bools)
        metadata = {"text": content[:1000]}  # Limit metadata text size

        # Add other metadata
        for key, value in metadata_dict.items():
            if isinstance(value, (str, int, float, bool)):
                metadata[key] = value

        # Create vector tuple (id, values, metadata)
        vector_id = f"chunk_{original_idx}"
        vectors_to_upsert.append((vector_id, embedding, metadata))

        # Upload in batches of 100
        if len(vectors_to_upsert) >= 100:
            pinecone_index.upsert(vectors=vectors_to_upsert)
            logger.info(f"Uploaded batch of {len(vectors_to_upsert)} vectors")
            vectors_to_upsert = []

    # Upload remaining vectors
    if vectors_to_upsert:
        pinecone_index.upsert(vectors=vectors_to_upsert)
        logger.info(f"Uploaded final {len(vectors_to_upsert)} vectors")

    if skipped_count > 0:
        logger.warning(f"Skipped {skipped_count} problematic chunks")

    logger.info(f"✅ Successfully indexed {len(documents)} documents into {len(nodes)} chunks")

    # Get index stats
    stats = pinecone_index.describe_index_stats()
    logger.info(f"📊 Index stats: {stats['total_vector_count']} vectors")

    # Create LlamaIndex wrapper for querying
    vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
    vector_index = VectorStoreIndex.from_vector_store(vector_store)

    return vector_index


if __name__ == "__main__":
    # For direct script execution
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    from dotenv import load_dotenv

    load_dotenv()

    logger.info("Starting PDF indexing...")
    index = index_voice_acting_books()
    logger.info("Indexing complete!")
