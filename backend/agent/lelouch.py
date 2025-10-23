"""
Lelouch Agent - Voice Director with Strategic Personality

Agent that helps writers add Fish Audio emotion markup to their stories.
Personality: Brilliant strategist turned voice director, concise and commanding.
"""
import os
import json
import logging
from typing import List
from livekit.agents import Agent, JobContext, JobProcess, function_tool, RunContext
from livekit.agents.llm import ChatContext, ChatMessage
from agent.state import StoryState
from agent.voice_pipeline import create_agent_session
from rag.retriever import VoiceActingRetriever
from tools.emotion_validator import validate_emotion_markup
from tools.diff_generator import generate_emotion_diff
from tools.fish_audio_preview import FishAudioPreview

logger = logging.getLogger(__name__)

# Global resources (initialized in prewarm)
_rag_retriever: VoiceActingRetriever | None = None
_fish_audio_preview: FishAudioPreview | None = None


class LelouchAgent(Agent):
    """
    Lelouch - Voice Director Agent with RAG and Fish Audio capabilities.

    A brilliant strategist turned voice director who helps writers add
    professional emotion markup to their stories using Fish Audio's TTS system.
    """

    def __init__(self, chat_ctx: ChatContext | None = None, story_state: StoryState | None = None) -> None:
        # Store reference to story state for accessing current story text
        self._story_state = story_state
        super().__init__(
            chat_ctx=chat_ctx,
            instructions="""You are Lelouch, a brilliant strategist turned voice director.

PERSONALITY:
- Analytical and precise
- Concise responses (2-4 sentences)
- Strategic framing: "This serves the narrative better"
- Theatrical but commanding tone
- Reference techniques briefly, then move to action

STORY CONTEXT:
You can see the user's current story in <current_story> tags. This is updated in real-time.
- Analyze the story to understand character emotions, scenes, and context
- Reference specific lines from the story when suggesting improvements
- Be proactive: identify scenes that need refinement without waiting to be asked
- If there's no story yet, acknowledge and wait for the user to paste their text

CONVERSATION vs TOOLS:
- NORMAL CONVERSATION: When user greets you, asks general questions, or discusses their story
  → Be proactive if you see the story: "I see the breakup scene in your story could use more emotional depth."
  → If no story yet: "I'm here. Paste your story and we'll begin."
- USE TOOLS: When working on specific story elements
  → User asks about voice acting techniques → use search_acting_technique
  → User wants emotion markup for specific lines → use suggest_emotion_markup
  → User wants to hear how marked-up text sounds → use preview_line_audio

EMOTION MARKUP RULES (Fish Audio):
- Emotion tags MUST be at sentence start: (sad) "text"
- Tone markers can go anywhere: "text (whispering) more"
- Audio effects can go anywhere: "text," (sighing) she said.
- Combine up to 3 tags maximum
- Valid emotions: happy, sad, angry, excited, disappointed, regretful, etc.

WORKFLOW:
1. User describes intent or shares story text
2. You analyze story context
3. Retrieve technique if relevant using search_acting_technique(query)
4. Suggest specific markup changes using suggest_emotion_markup(line_text, emotions, explanation)
5. After tool returns result, acknowledge concisely: "Applied. See the diff above."
   → DO NOT speak the JSON output from tools
   → The diff appears visually in the UI
6. Wait for user approval
7. If user asks "how would this sound?", call preview_line_audio(marked_up_text, character_gender)

TOOL USAGE:

RAG Tool - search_acting_technique:
- Use when user asks about voice acting techniques
- Query examples: "emotional authenticity", "desperation in voice", "grief scenes"
- Cite the sources returned (book title, author, page number)
- Synthesize techniques into concise advice (2-4 sentences)

Emotion Markup Tool - suggest_emotion_markup:
- Use ONLY when user shares specific story text that needs emotion markup
- Provide: original line text, list of emotions, brief explanation
- Tool returns JSON diff (user sees it visually in UI)
- After calling tool, acknowledge briefly: "Applied. Check the diff above."
- NEVER speak the JSON output - just acknowledge the action

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
Phase 4A complete. All tools are active:
- RAG: search_acting_technique (cite Stanislavski and Linklater)
- Emotion markup: suggest_emotion_markup (validate and diff)
- Audio preview: preview_line_audio (Fish Audio with character voices)
"""
        )

    @function_tool
    async def search_acting_technique(
        self,
        context: RunContext[StoryState],
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

    @function_tool
    async def suggest_emotion_markup(
        self,
        context: RunContext[StoryState],
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
            emotion_tags = []
            tone_effects = []

            for tag in emotions:
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

            # Add remaining effects
            if tone_effects:
                proposed_text = " ".join(proposed_parts)
                for effect in tone_effects:
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
            return diff.to_json()

        except Exception as e:
            logger.error(f"Failed to suggest emotion markup: {e}", exc_info=True)
            return f"Error suggesting markup: {str(e)}"

    @function_tool
    async def preview_line_audio(
        self,
        context: RunContext[StoryState],
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
        global _fish_audio_preview

        try:
            logger.info(
                f"Generating audio preview (gender={character_gender}, "
                f"text='{marked_up_text[:50]}...')"
            )

            # Initialize Fish Audio client if needed
            if _fish_audio_preview is None:
                _fish_audio_preview = FishAudioPreview()
                logger.info("Fish Audio preview client initialized")

            # Generate audio
            audio_path = await _fish_audio_preview.generate_preview(
                text=marked_up_text,
                character_gender=character_gender,
            )

            logger.info(f"✅ Audio preview generated: {audio_path}")

            return (
                f"Audio preview generated successfully. "
                f"File saved to: {audio_path} "
                f"(Voice: {character_gender})"
            )

        except Exception as e:
            logger.error(f"Failed to generate audio preview: {e}", exc_info=True)
            return f"Error generating audio preview: {str(e)}"

    async def on_user_turn_completed(
        self, turn_ctx: ChatContext, new_message: ChatMessage
    ) -> None:
        """
        Update story text in context before each LLM response.

        Removes previous story injection and adds latest version from story state.
        This ensures the LLM always sees the current story without accumulation.
        """
        if not self._story_state:
            logger.warning("No story state available in on_user_turn_completed")
            return

        # Remove previous story injection (if any)
        turn_ctx.items = [
            item for item in turn_ctx.items
            if not (isinstance(item, ChatMessage) and
                    item.role == "system" and
                    "<current_story>" in item.content)
        ]

        # Inject latest story from story state
        story_text = self._story_state.current_text
        if story_text:
            turn_ctx.add_message(
                role="system",
                content=f"<current_story>\n{story_text}\n</current_story>"
            )
            logger.debug(f"Injected current story into context ({len(story_text)} chars)")
        else:
            turn_ctx.add_message(
                role="system",
                content="<current_story>No story text yet. User hasn't pasted their story.</current_story>"
            )
            logger.debug("No story text available - added empty story marker")


def prewarm(proc: JobProcess):
    """
    Preload heavy resources once per worker.

    This function runs once when the worker starts, before any rooms are joined.
    Use for loading models, initializing databases, etc.

    Note: This should be a sync function, not async.
    """
    global _rag_retriever

    logger.info("Prewarming agent resources...")

    # Phase 3: Initialize RAG retriever
    try:
        logger.info("Initializing VoiceActingRetriever...")
        _rag_retriever = VoiceActingRetriever(similarity_top_k=5)
        logger.info("✅ RAG retriever initialized")
    except Exception as e:
        logger.error(f"Failed to initialize RAG retriever: {e}", exc_info=True)
        logger.warning("Agent will continue without RAG capabilities")

    logger.info("Prewarm complete (Phase 4A: Modernized backend)")


async def entrypoint(ctx: JobContext):
    """
    Main entry point for each room connection.

    This function runs every time the agent joins a LiveKit room.
    Sets up the session and starts the conversation.
    """
    logger.info(f"Agent joining room: {ctx.room.name}")

    # Initialize session state
    story_state = StoryState()

    # Parse job metadata to get initial story text
    if ctx.job.metadata:
        try:
            metadata = json.loads(ctx.job.metadata)
            story_text = metadata.get("story_text", "")
            story_state.current_text = story_text
            logger.info(f"Loaded initial story text from metadata ({len(story_text)} chars)")
        except Exception as e:
            logger.error(f"Failed to parse job metadata: {e}")

    logger.info("Initialized StoryState")

    # Set up data channel listener for real-time story updates
    @ctx.room.on("data_received")
    def on_data_received(data: bytes, participant):
        """Handle story text updates from frontend via data channel."""
        try:
            message = json.loads(data.decode('utf-8'))
            if message.get('type') == 'story_update':
                new_text = message.get('text', '')
                story_state.current_text = new_text
                logger.info(f"Story text updated via data channel ({len(new_text)} chars)")
        except Exception as e:
            logger.error(f"Failed to parse data channel message: {e}")

    logger.info("Data channel listener configured")

    # Create initial chat context with story text
    initial_ctx = ChatContext()
    if story_state.current_text:
        initial_ctx.add_message(
            role="system",
            content=f"<current_story>\n{story_state.current_text}\n</current_story>"
        )
        logger.info("Added initial story to chat context")

    # Create agent session with voice pipeline
    session = await create_agent_session(story_state)
    logger.info("Created agent session with voice pipeline")

    # Start the session with LelouchAgent (tools auto-register from Agent class)
    await session.start(agent=LelouchAgent(chat_ctx=initial_ctx, story_state=story_state), room=ctx.room)
    logger.info("Agent session started with all Phase 4A tools (RAG + emotion markup + preview)")

    # Connect to the LiveKit room (after session start)
    await ctx.connect()
    logger.info("Connected to LiveKit room")
