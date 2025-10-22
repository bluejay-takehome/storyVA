"""
Function tools for Lelouch voice director agent.

Provides RAG search, emotion markup, and audio preview capabilities for the agent.
"""
import logging
from typing import List
from livekit.agents.llm import function_tool
from agent.state import StoryState
from tools.emotion_validator import validate_emotion_markup, ValidationResult
from tools.diff_generator import generate_emotion_diff, EmotionDiff
from tools.fish_audio_preview import FishAudioPreview, infer_character_gender

logger = logging.getLogger(__name__)

# Global RAG retriever (initialized in prewarm)
_rag_retriever = None

# Global Fish Audio preview client (initialized on first use)
_fish_audio_preview = None


def set_rag_retriever(retriever):
    """Set the global RAG retriever instance (called from prewarm)."""
    global _rag_retriever
    _rag_retriever = retriever
    logger.info("RAG retriever registered with tools")


def get_fish_audio_preview() -> FishAudioPreview:
    """Get or create Fish Audio preview client."""
    global _fish_audio_preview
    if _fish_audio_preview is None:
        _fish_audio_preview = FishAudioPreview()
        logger.info("Fish Audio preview client initialized")
    return _fish_audio_preview


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
async def suggest_emotion_markup(
    line_text: str,
    emotions: List[str],
    explanation: str,
) -> str:
    """
    Suggest emotion markup for a line of dialogue.

    Use this when you want to apply Fish Audio emotion tags to text.
    The tool validates tags, generates a diff, and returns structured feedback.

    Args:
        line_text: Original line of text/dialogue without markup
        emotions: List of emotion tags to apply (e.g., ["sad", "whispering"])
        explanation: Brief explanation of why these emotions were chosen (1-2 sentences)

    Returns:
        JSON string with diff and validation results for frontend display

    Example:
        User: "Make the breakup scene sadder"
        line_text: "I can't do this anymore, she said."
        emotions: ["sad", "soft tone", "sighing"]
        explanation: "Regret and quiet resignation serve the moment better than anger."
    """
    try:
        logger.info(f"Suggesting emotion markup: {emotions} for '{line_text[:50]}...'")

        # Build proposed text with emotion tags
        # Separate emotions (must be at start) from tone/effects (can go anywhere)
        emotion_tags = []
        tone_effects = []

        for tag in emotions:
            # Simple categorization - could use emotion_validator for better accuracy
            if tag in ["whispering", "soft tone", "shouting", "screaming", "in a hurry tone"]:
                tone_effects.append(tag)
            elif tag in ["laughing", "sighing", "sobbing", "crying loudly", "gasping"]:
                tone_effects.append(tag)
            else:
                emotion_tags.append(tag)

        # Build proposed text
        proposed_parts = []

        # Add emotion tags at start
        if emotion_tags:
            for tag in emotion_tags:
                proposed_parts.append(f"({tag})")

        # Add tone if at start
        if tone_effects and not line_text.strip().startswith('"'):
            proposed_parts.append(f"({tone_effects[0]})")
            tone_effects = tone_effects[1:]

        # Add the text
        proposed_parts.append(line_text)

        # Add remaining effects (e.g., before attribution)
        if tone_effects:
            # Simple heuristic: add before "she/he said" if present
            proposed_text = " ".join(proposed_parts)
            for effect in tone_effects:
                # Insert before common attribution patterns
                if " said" in proposed_text or " whispered" in proposed_text:
                    proposed_text = proposed_text.replace(" said", f" ({effect}) said", 1)
                    proposed_text = proposed_text.replace(" whispered", f" ({effect}) whispered", 1)
                else:
                    proposed_text += f" ({effect})"
        else:
            proposed_text = " ".join(proposed_parts)

        # Validate the proposed markup
        validation = validate_emotion_markup(proposed_text)

        if not validation.is_valid:
            logger.warning(f"Validation errors: {validation.errors}")
            return f"ERROR: Invalid emotion markup. {'; '.join(validation.errors)}"

        # Generate diff
        diff = generate_emotion_diff(
            original_text=line_text,
            proposed_text=proposed_text,
            explanation=explanation
        )

        logger.info(f"✅ Emotion markup suggested: {diff.summary}")

        # Return structured result
        return diff.to_json()

    except Exception as e:
        logger.error(f"Failed to suggest emotion markup: {e}", exc_info=True)
        return f"Error suggesting markup: {str(e)}"


@function_tool()
async def preview_line_audio(
    marked_up_text: str,
    character_gender: str = "neutral",
) -> str:
    """
    Generate audio preview of a line with Fish Audio using character voice.

    Use when user asks "how would this sound?" or wants to hear the emotional delivery.
    IMPORTANT: You MUST infer character_gender automatically from story context.
    Do NOT ask the user for gender - analyze the text yourself.

    Gender inference rules:
    - Pronouns: "she/her" → "female", "he/him" → "male"
    - Character names: Sarah/Emma → "female", Marcus/John → "male"
    - Attribution: "she said" → "female", "he replied" → "male"
    - Default to "neutral" if ambiguous

    Args:
        marked_up_text: Text with emotion tags applied (e.g., "(sad) I'm leaving")
        character_gender: "male", "female", or "neutral" (MUST infer, not ask)

    Returns:
        Status message with audio file path

    Example:
        User: "How would that sound?"
        Context: '"I hate you," she said.'
        → Infer gender="female" from "she"
        marked_up_text: '(sad)(soft tone) "I hate you," (sighing) she said.'
        character_gender: "female"
    """
    try:
        logger.info(
            f"Generating audio preview (gender={character_gender}, "
            f"text='{marked_up_text[:50]}...')"
        )

        # Get Fish Audio preview client
        preview_client = get_fish_audio_preview()

        # Generate audio
        audio_path = await preview_client.generate_preview(
            text=marked_up_text,
            character_gender=character_gender,
        )

        logger.info(f"✅ Audio preview generated: {audio_path}")

        # Return success message with file path
        return (
            f"Audio preview generated successfully. "
            f"File saved to: {audio_path} "
            f"(Voice: {character_gender})"
        )

    except Exception as e:
        logger.error(f"Failed to generate audio preview: {e}", exc_info=True)
        return f"Error generating audio preview: {str(e)}"
