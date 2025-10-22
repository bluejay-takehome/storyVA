#!/usr/bin/env python3
"""
Setup script for Pinecone vector database index.

Creates the Pinecone index for StoryVA voice acting reference RAG system.
Based on TDD Section 4.3 specifications.
"""
import os
import sys
from pathlib import Path

# Add parent directory to path to import from backend
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec

# Load environment variables
load_dotenv()

# Configuration from TDD
INDEX_NAME = "storyva-voice-acting"
DIMENSION = 1536  # OpenAI text-embedding-3-small
METRIC = "cosine"
CLOUD = "aws"
REGION = "us-east-1"


def create_pinecone_index():
    """Create Pinecone index for voice acting reference documents."""

    # Initialize Pinecone
    api_key = os.getenv("PINECONE_API_KEY")
    if not api_key:
        print("❌ Error: PINECONE_API_KEY not found in environment variables")
        print("Please add it to backend/.env file")
        sys.exit(1)

    print(f"🔧 Initializing Pinecone client...")
    pc = Pinecone(api_key=api_key)

    # Check if index already exists
    existing_indexes = pc.list_indexes()
    index_names = [idx.name for idx in existing_indexes]

    if INDEX_NAME in index_names:
        print(f"✅ Index '{INDEX_NAME}' already exists!")

        # Get index info
        index = pc.Index(INDEX_NAME)
        stats = index.describe_index_stats()
        print(f"\n📊 Index Stats:")
        print(f"   - Dimension: {stats.get('dimension', 'N/A')}")
        print(f"   - Total vectors: {stats.get('total_vector_count', 0)}")
        print(f"   - Namespaces: {list(stats.get('namespaces', {}).keys()) or ['default']}")

        return

    # Create new index
    print(f"🚀 Creating Pinecone index '{INDEX_NAME}'...")
    print(f"   - Dimension: {DIMENSION}")
    print(f"   - Metric: {METRIC}")
    print(f"   - Cloud: {CLOUD}")
    print(f"   - Region: {REGION}")

    pc.create_index(
        name=INDEX_NAME,
        dimension=DIMENSION,
        metric=METRIC,
        spec=ServerlessSpec(
            cloud=CLOUD,
            region=REGION
        )
    )

    print(f"✅ Successfully created index '{INDEX_NAME}'!")
    print(f"\n📝 Next steps:")
    print(f"   1. Run the ingestion script to populate the index")
    print(f"   2. Test RAG retrieval with sample queries")


if __name__ == "__main__":
    print("=" * 60)
    print("  StoryVA - Pinecone Index Setup")
    print("=" * 60)
    print()

    try:
        create_pinecone_index()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("  Setup Complete!")
    print("=" * 60)
