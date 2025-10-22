#!/usr/bin/env python3
"""
PDF Indexing Script

One-time script to index voice acting PDF books into Pinecone.
Run this before starting the agent to populate the knowledge base.

Usage:
    uv run python scripts/index_pdfs.py
"""
import os
import sys
import logging
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from rag.indexer import index_voice_acting_books

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def main():
    """Run PDF indexing."""
    logger.info("=" * 60)
    logger.info("  Voice Acting Knowledge Base Indexing")
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

    logger.info(f"Pinecone Index: {os.getenv('PINECONE_INDEX_NAME')}")
    logger.info("")

    # Check PDF files exist
    pdf_dir = Path(__file__).parent.parent / "data" / "pdfs"
    pdf_files = list(pdf_dir.glob("*.pdf"))

    if not pdf_files:
        logger.error(f"No PDF files found in: {pdf_dir}")
        return False

    logger.info(f"Found {len(pdf_files)} PDF files:")
    for pdf in pdf_files:
        logger.info(f"  - {pdf.name}")
    logger.info("")

    # Run indexing
    try:
        logger.info("Starting indexing process...")
        logger.info("This may take several minutes depending on PDF size.")
        logger.info("")

        index = index_voice_acting_books()

        logger.info("")
        logger.info("=" * 60)
        logger.info("  ✅ Indexing Complete!")
        logger.info("=" * 60)
        logger.info("")
        logger.info("Your voice acting knowledge base is ready for use.")
        logger.info("Start the agent with: uv run python main.py dev")
        logger.info("")

        return True

    except Exception as e:
        logger.error(f"Indexing failed: {e}", exc_info=True)
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
