"""
Function tools for Lelouch voice director agent.

Provides RAG search and emotion markup capabilities for the agent.
"""
import logging
from livekit.agents.llm import function_tool
from agent.state import StoryState

logger = logging.getLogger(__name__)

# Global RAG retriever (initialized in prewarm)
_rag_retriever = None


def set_rag_retriever(retriever):
    """Set the global RAG retriever instance (called from prewarm)."""
    global _rag_retriever
    _rag_retriever = retriever
    logger.info("RAG retriever registered with tools")


@function_tool()
async def search_acting_technique(
    query: str,
) -> str:
    """
    Search voice acting books (Stanislavski and Linklater) for techniques.

    Use this when the user asks about voice acting techniques, emotional approaches,
    or when you need to cite specific methods from the books to support your advice.

    Args:
        query: Natural language query about voice acting technique

    Returns:
        Relevant passages from the books with citations (author, title, page)

    Example:
        User: "How do I convey desperation?"
        query: "techniques for conveying desperation in voice acting"
    """
    if _rag_retriever is None:
        logger.error("RAG retriever not initialized")
        return "RAG system not available. Please restart the agent."

    try:
        logger.info(f"RAG search: {query}")
        result = await _rag_retriever.search(query)
        logger.info(f"RAG result: {len(result)} chars, citations included")
        return result
    except Exception as e:
        logger.error(f"RAG search failed: {e}", exc_info=True)
        return f"Error retrieving technique: {str(e)}"
