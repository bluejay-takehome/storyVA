#!/usr/bin/env python3
"""Debug script to check Pinecone index status."""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from pinecone import Pinecone

load_dotenv()

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index_name = os.getenv("PINECONE_INDEX_NAME")

print(f"Checking index: {index_name}")
print()

# Get index
index = pc.Index(index_name)

# Get stats
stats = index.describe_index_stats()
print("Index Stats:")
print(f"  Total vectors: {stats.get('total_vector_count', 0)}")
print(f"  Dimension: {stats.get('dimension', 'unknown')}")
print()

# Try a sample query
from llama_index.embeddings.openai import OpenAIEmbedding

embed_model = OpenAIEmbedding(model="text-embedding-3-small")
query_text = "emotion memory"
print(f"Testing query: '{query_text}'")

# Generate embedding
query_embedding = embed_model.get_text_embedding(query_text)
print(f"Generated embedding with {len(query_embedding)} dimensions")

# Query Pinecone directly
results = index.query(
    vector=query_embedding,
    top_k=5,
    include_metadata=True,
)

print(f"\nDirect Pinecone query results:")
print(f"  Matches found: {len(results.matches)}")

for i, match in enumerate(results.matches[:3], 1):
    print(f"\n  Match {i}:")
    print(f"    Score: {match.score:.4f}")
    print(f"    ID: {match.id}")
    if match.metadata:
        print(f"    Metadata keys: {list(match.metadata.keys())}")
        text = match.metadata.get('text', match.metadata.get('_node_content', 'No text found'))
        print(f"    Text preview: {text[:200]}...")
