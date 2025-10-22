"""
Lelouch Agent - Voice Director with Strategic Personality

Agent that helps writers add Fish Audio emotion markup to their stories.
Personality: Brilliant strategist turned voice director, concise and commanding.
"""
import os
import logging
from agent.state import StoryState

logger = logging.getLogger(__name__)


# TODO: Phase 2 - Implement actual agent
# from livekit.agents import Agent, function_tool, RunContext, JobContext
# from rag.retriever import VoiceActingRetriever


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
3. Retrieve technique if relevant (use RAG tool)
4. Suggest specific markup changes
5. Present diff visually (don't speak tags)
6. Wait for user approval

PREVIEW TOOL USAGE:
- When user asks "how would this sound?", call preview_line_audio
- Automatically infer character gender from context (pronouns, names, attribution)
- Example: "she said" → gender="female", "Marcus replied" → gender="male"
- NEVER ask user for gender - infer it silently

STYLE EXAMPLES:
- "I see. Given the context, regret serves better than sadness here."
- "Stanislavski's emotion memory - we apply it by... Observe."
- "Too vague. Specify the emotion's purpose."
- "Applied. The subtlety serves the moment better."
"""


# TODO: Phase 2 - Implement LelouchAgent class
# class LelouchAgent(Agent):
#     def __init__(self, rag_retriever: VoiceActingRetriever):
#         super().__init__(instructions=LELOUCH_INSTRUCTIONS)
#         self.rag_retriever = rag_retriever
#
#     @function_tool()
#     async def search_acting_technique(
#         self,
#         context: RunContext[StoryState],
#         query: str,
#     ) -> str:
#         """Search voice acting books for techniques."""
#         result = await self.rag_retriever.search(query)
#         return result
#
#     @function_tool()
#     async def suggest_emotion_markup(
#         self,
#         context: RunContext[StoryState],
#         line_text: str,
#         emotions: list[str],
#         explanation: str,
#     ) -> dict:
#         """Create emotion markup suggestion."""
#         # TODO: Generate diff, store in context.userdata.pending_diff
#         pass
#
#     @function_tool()
#     async def preview_line_audio(
#         self,
#         context: RunContext[StoryState],
#         marked_up_text: str,
#         character_gender: str,
#     ) -> str:
#         """Generate audio preview with Fish Audio using character's voice."""
#         # TODO: Call Fish Audio API with appropriate voice_id
#         pass


async def prewarm(proc):
    """Preload heavy resources once per worker."""
    logger.info("Prewarming agent resources...")
    # TODO: Initialize RAG retriever
    logger.info("Prewarm complete")


async def entrypoint(ctx):
    """Main entry point for each room connection."""
    logger.info(f"Agent joining room: {ctx.room.name}")
    # TODO: Phase 2
    # - Connect to room
    # - Initialize StoryState
    # - Create agent session
    # - Start conversation
    logger.info("Entrypoint stub (Phase 2 implementation pending)")
