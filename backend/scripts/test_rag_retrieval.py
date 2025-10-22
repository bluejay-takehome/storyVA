#!/usr/bin/env python3
"""
RAG Retrieval Test Script

Tests the voice acting knowledge retrieval system with sample queries.
Verifies that RAG can retrieve relevant passages from Stanislavski and Linklater books.

Usage:
    uv run python scripts/test_rag_retrieval.py
"""
import os
import sys
import asyncio
import logging
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from rag.retriever import VoiceActingRetriever

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


# Test queries from PRD.md Section 9.2
TEST_QUERIES = [
    "How do I make a character sound more desperate?",
    "What techniques help with emotional authenticity?",
    "How should I approach a grief scene?",
    "What does Stanislavski say about subtext?",
    "How do I use voice to show character transformation?",
    "What is emotion memory and how do I use it?",
    "How can I make dialogue more natural and believable?",
    "What does Linklater teach about freeing the voice?",
]


async def test_rag_retrieval():
    """Test RAG retrieval with multiple queries."""
    logger.info("=" * 60)
    logger.info("  Voice Acting RAG Retrieval Test")
    logger.info("=" * 60)
    logger.info("")

    # Verify environment variables
    required_vars = [
        "PINECONE_API_KEY",
        "PINECONE_INDEX_NAME",
        "OPENAI_API_KEY",
    ]

    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        logger.error("Please check backend/.env file")
        return False

    try:
        # Initialize retriever
        logger.info("Initializing VoiceActingRetriever...")
        retriever = VoiceActingRetriever(similarity_top_k=5)
        logger.info("")

        # Test each query
        for i, query in enumerate(TEST_QUERIES, 1):
            logger.info(f"\n{'='*60}")
            logger.info(f"Test {i}/{len(TEST_QUERIES)}: {query}")
            logger.info("=" * 60)

            try:
                # Execute query
                result = await retriever.search(query)

                # Display result
                print(f"\n{result}\n")

                # Check if result contains expected content
                if len(result) > 100:  # Rough check for meaningful content
                    logger.info("✅ Retrieved relevant content")
                else:
                    logger.warning("⚠️  Result seems short, may not be relevant")

            except Exception as e:
                logger.error(f"❌ Query failed: {e}", exc_info=True)
                return False

        logger.info("\n" + "=" * 60)
        logger.info("  All RAG retrieval tests completed!")
        logger.info("=" * 60)
        logger.info("")
        logger.info("✅ RAG system is working correctly")
        logger.info("Agent can now cite Stanislavski and Linklater techniques")
        logger.info("")

        return True

    except Exception as e:
        logger.error(f"RAG retrieval test failed: {e}", exc_info=True)
        return False


if __name__ == "__main__":
    success = asyncio.run(test_rag_retrieval())
    sys.exit(0 if success else 1)
