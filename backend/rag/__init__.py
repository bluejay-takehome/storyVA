"""
RAG (Retrieval-Augmented Generation) system for voice acting knowledge.

This package provides indexing and retrieval of voice acting techniques
from Stanislavski and Linklater books using Pinecone vector database.
"""

from rag.indexer import index_voice_acting_books
from rag.retriever import VoiceActingRetriever

__all__ = ["index_voice_acting_books", "VoiceActingRetriever"]
