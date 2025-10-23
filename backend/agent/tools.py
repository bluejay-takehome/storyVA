"""
Function tools for Lelouch voice director agent.

Provides RAG search and emotion markup capabilities for the agent.
"""
import logging
from livekit.agents.llm import function_tool
from tools.emotion_validator import validate_emotion_markup
from tools.diff_generator import generate_emotion_diff, parse_unified_diff

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


@function_tool()
async def apply_emotion_diff(
    diff_patch: str,
    explanation: str,
) -> str:
    """
    Apply emotion control changes using unified diff format.

    Use this when you want to apply Fish Audio emotion tags to text.
    Provide a git-style unified diff showing exact text changes.

    Args:
        diff_patch: Unified diff string showing original (-) and proposed (+) text.
                   Must use exact text from the story for original lines.
                   Format:
                   @@ -1 +1 @@
                   -(old text with tags)
                   +(new text with tags)
        explanation: Brief explanation of why these changes were made (1-2 sentences)

    Returns:
        JSON string with diff and validation results for frontend display

    Example:
        User: "Remove the nervous tag from Miku's line"
        diff_patch: '''@@ -1 +1 @@
        -(nervous) (resigned) Miku: "Hello"
        +(resigned) Miku: "Hello"
        '''
        explanation: "Remove nervous to simplify emotional state"
    """
    try:
        logger.info("Parsing emotion markup diff...")

        # Parse unified diff to extract original and proposed text
        try:
            original_text, proposed_text = parse_unified_diff(diff_patch)
        except ValueError as e:
            logger.error(f"Invalid diff format: {e}")
            return f"ERROR: {str(e)}"

        logger.info(f"Diff parsed - original: '{original_text[:50]}...', proposed: '{proposed_text[:50]}...'")

        # Note: This standalone tool doesn't have access to story state for validation
        # The agent's version in lelouch.py does validate against current story

        # Validate the proposed markup has valid Fish Audio tags
        validation = validate_emotion_markup(proposed_text)

        if not validation.is_valid:
            logger.warning(f"Validation errors: {validation.errors}")
            return f"ERROR: Invalid emotion markup. {'; '.join(validation.errors)}"

        # Generate diff for frontend display
        diff = generate_emotion_diff(
            original_text=original_text,
            proposed_text=proposed_text,
            explanation=explanation
        )

        logger.info(f"✅ Emotion markup suggested: {diff.summary}")

        # Return structured result
        return diff.to_json()

    except Exception as e:
        logger.error(f"Failed to suggest emotion markup: {e}", exc_info=True)
        return f"Error suggesting markup: {str(e)}"


