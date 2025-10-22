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
3. Retrieve technique if relevant (use RAG tool - coming in Phase 3)
4. Suggest specific markup changes
5. Present diff visually (don't speak tags)
6. Wait for user approval

PREVIEW TOOL USAGE (coming in Phase 4):
- When user asks "how would this sound?", call preview_line_audio
- Automatically infer character gender from context (pronouns, names, attribution)
- Example: "she said" → gender="female", "Marcus replied" → gender="male"
- NEVER ask user for gender - infer it silently

STYLE EXAMPLES:
- "I see. Given the context, regret serves better than sadness here."
- "Stanislavski's emotion memory - we apply it by... Observe."
- "Too vague. Specify the emotion's purpose."
- "Applied. The subtlety serves the moment better."

CURRENT PHASE:
You are in Phase 2 (Backend Core). RAG tools and emotion markup tools are not yet available.
Focus on conversational interaction and demonstrating your personality.
When users ask about voice direction, provide general guidance using your knowledge.
"""


async def prewarm(proc: JobProcess):
    """
    Preload heavy resources once per worker.

    This function runs once when the worker starts, before any rooms are joined.
    Use for loading models, initializing databases, etc.
    """
    logger.info("Prewarming agent resources...")

    # TODO: Phase 3 - Initialize RAG retriever
    # global rag_retriever
    # rag_retriever = VoiceActingRetriever()

    logger.info("Prewarm complete (Phase 2: No RAG yet)")


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
    await session.start(
        room=ctx.room,
        instructions=LELOUCH_INSTRUCTIONS,
    )
    logger.info("Agent session started")

    # Generate initial greeting
    await session.agent.say(
        "Ah, you've come seeking my expertise. I am Lelouch. "
        "Tell me about your story - let us transform it into something extraordinary.",
        allow_interruptions=True,
    )
    logger.info("Initial greeting delivered")
