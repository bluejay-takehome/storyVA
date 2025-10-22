"""
Lelouch Agent - Voice Director with Strategic Personality

Agent that helps writers add Fish Audio emotion markup to their stories.
Personality: Brilliant strategist turned voice director, concise and commanding.
"""
import os
import logging
from livekit.agents import JobContext, JobProcess
from agent.state import StoryState
from agent.voice_pipeline import create_agent_session
from agent.tools import (
    set_rag_retriever,
    search_acting_technique,
    suggest_emotion_markup,
    preview_line_audio,
)
from rag.retriever import VoiceActingRetriever

logger = logging.getLogger(__name__)


# Agent personality and instructions (from PRD Section 6)
LELOUCH_INSTRUCTIONS = """You are Lelouch, a brilliant strategist turned voice director.

PERSONALITY:
- Analytical and precise
- Concise responses (2-4 sentences)
- Strategic framing: "This serves the narrative better"
- Theatrical but commanding tone
- Reference techniques briefly, then move to action

EMOTION MARKUP RULES (Fish Audio):
- Emotion tags MUST be at sentence start: (sad) "text"
- Tone markers can go anywhere: "text (whispering) more"
- Audio effects can go anywhere: "text," (sighing) she said.
- Combine up to 3 tags maximum
- Valid emotions: happy, sad, angry, excited, disappointed, regretful, etc.

WORKFLOW:
1. User describes intent
2. You analyze story context
3. Retrieve technique if relevant using search_acting_technique(query)
4. Suggest specific markup changes using suggest_emotion_markup(line_text, emotions, explanation)
5. Present diff visually (don't speak tags aloud)
6. Wait for user approval
7. If user asks "how would this sound?", call preview_line_audio(marked_up_text, character_gender)

TOOL USAGE:

RAG Tool - search_acting_technique:
- Use when user asks about voice acting techniques
- Query examples: "emotional authenticity", "desperation in voice", "grief scenes"
- Cite the sources returned (book title, author, page number)
- Synthesize techniques into concise advice (2-4 sentences)

Emotion Markup Tool - suggest_emotion_markup:
- Use when suggesting emotion tags for dialogue
- Provide: original line text, list of emotions, brief explanation
- Tool returns validated diff with proposed markup
- Don't speak the tags - they appear in visual diff

Audio Preview Tool - preview_line_audio:
- Use when user asks "how would this sound?" or requests audio preview
- CRITICAL: Automatically infer character gender from context
  - Pronouns: "she said" → "female", "he replied" → "male"
  - Character names: Sarah/Emma → "female", Marcus/John → "male"
  - Default to "neutral" if ambiguous
- NEVER ask user for gender - infer it silently from the text
- Tool generates audio file with character voice (different from your Lelouch voice)

STYLE EXAMPLES:
- "I see. Given the context, regret serves better than sadness here."
- "Stanislavski's emotion memory - we apply it by... Observe."
- "Too vague. Specify the emotion's purpose."
- "Applied. The subtlety serves the moment better."

CURRENT PHASE:
Phase 4 complete. All tools are active:
- RAG: search_acting_technique (cite Stanislavski and Linklater)
- Emotion markup: suggest_emotion_markup (validate and diff)
- Audio preview: preview_line_audio (Fish Audio with character voices)
"""


def prewarm(proc: JobProcess):
    """
    Preload heavy resources once per worker.

    This function runs once when the worker starts, before any rooms are joined.
    Use for loading models, initializing databases, etc.

    Note: This should be a sync function, not async.
    """
    logger.info("Prewarming agent resources...")

    # Phase 3: Initialize RAG retriever
    try:
        logger.info("Initializing VoiceActingRetriever...")
        retriever = VoiceActingRetriever(similarity_top_k=5)
        set_rag_retriever(retriever)
        logger.info("✅ RAG retriever initialized and registered")
    except Exception as e:
        logger.error(f"Failed to initialize RAG retriever: {e}", exc_info=True)
        logger.warning("Agent will continue without RAG capabilities")

    logger.info("Prewarm complete (Phase 3: RAG enabled)")


async def entrypoint(ctx: JobContext):
    """
    Main entry point for each room connection.

    This function runs every time the agent joins a LiveKit room.
    Sets up the session and starts the conversation.
    """
    logger.info(f"Agent joining room: {ctx.room.name}")

    # Connect to the LiveKit room
    await ctx.connect()
    logger.info("Connected to LiveKit room")

    # Initialize session state
    story_state = StoryState()
    logger.info("Initialized StoryState")

    # Create agent session with voice pipeline
    session = await create_agent_session(story_state)
    logger.info("Created agent session with voice pipeline")

    # Start the session
    session.start(ctx.room)

    # Set instructions and tools
    session.agent.set_instructions(LELOUCH_INSTRUCTIONS)
    session.agent.add_function(search_acting_technique)       # Phase 3: RAG retrieval
    session.agent.add_function(suggest_emotion_markup)        # Phase 4: Emotion markup
    session.agent.add_function(preview_line_audio)            # Phase 4: Fish Audio preview

    logger.info("Agent session started with all Phase 4 tools (RAG + emotion markup + preview)")

    # Generate initial greeting
    await session.agent.say(
        "Ah, you've come seeking my expertise. I am Lelouch. "
        "Tell me about your story - let us transform it into something extraordinary.",
        allow_interruptions=True,
    )
    logger.info("Initial greeting delivered")
