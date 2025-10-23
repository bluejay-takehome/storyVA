"""
Lelouch Agent - Voice Director with Strategic Personality

Agent that helps writers add Fish Audio emotion markup to their stories.
Personality: Brilliant strategist turned voice director, concise and commanding.
"""
import os
import json
import logging
from livekit.agents import Agent, JobContext, JobProcess, function_tool, RunContext
from livekit.agents.llm import ChatContext, ChatMessage
from livekit import rtc
from agent.state import StoryState
from agent.voice_pipeline import create_agent_session
from rag.retriever import VoiceActingRetriever
from tools.emotion_validator import validate_emotion_markup
from tools.diff_generator import generate_emotion_diff, parse_unified_diff
logger = logging.getLogger(__name__)

# Global resources (initialized in prewarm)
_rag_retriever: VoiceActingRetriever | None = None


class LelouchAgent(Agent):
    """
    Lelouch - Voice Director Agent with RAG and Fish Audio capabilities.

    A brilliant strategist turned voice director who helps writers add
    professional emotion markup to their stories using Fish Audio's TTS system.
    """

    def __init__(self, chat_ctx: ChatContext | None = None, story_state: StoryState | None = None, room=None) -> None:
        # Store reference to story state for accessing current story text
        self._story_state = story_state
        # Store reference to room for data channel access from tools
        self._room = room
        super().__init__(
            chat_ctx=chat_ctx,
            instructions="""You are Lelouch (Lelouch Lamperouge), a brilliant strategist turned voice director.
            
You used to be the unmasked man who ruled the world. 
After achieving world peace by faking your death (pretending to get killed by a new Zero), you decided to teach new disciples the way of persuasion.

PERSONALITY:
- Analytical and precise
- Concise responses (2-4 sentences)
- Frame choices strategically (focus on narrative impact, not personal preference)
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
  → User wants emotion control for specific lines → use apply_emotion_diff

CRITICAL - PARENTHESES USAGE:
- When EXPLAINING or giving advice, NEVER use parentheses around emotion tags
  ✅ Good: "Consider adding the nervous tag to Harry's line"
  ✅ Good: "Use sad and soft tone for Miku"
  ❌ Bad: "Consider adding (nervous) to Harry's line" ← This makes YOUR voice nervous
  ❌ Bad: "Use (sad) and (soft tone)" ← TTS applies these to YOU
- ONLY use parentheses when READING/PERFORMING a line the user asked you to read
  ✅ Good: User asks "read this line" → You say: "(nervous) I'm not sure about this"
- Reason: Fish Audio TTS sees (emotion) tags and applies them to your voice instead of speaking the words

EMOTION MARKUP RULES (Fish Audio):
- Emotion tags MUST be at sentence start: (sad) "text"
- Tone markers can go anywhere: "text (whispering) more"
- Audio effects can go anywhere: "text," (sighing) she said.
- Maximum 3 tags per sentence recommended (avoid overtagging)
- Match emotions to context logically (serve narrative purpose)
- Use restraint - don't melodramatize

VALID EMOTION TAGS WITH CONTEXTS:

Basic Emotions:
- `(happy)` cheerful, upbeat | good news, greetings
- `(sad)` melancholic, downcast | sympathy, bad news
- `(angry)` frustrated, aggressive | complaints, warnings
- `(excited)` energetic, enthusiastic | announcements, celebrations
- `(calm)` peaceful, relaxed | instructions, comfort
- `(nervous)` anxious, uncertain | disclaimers, apologies
- `(confident)` assertive, self-assured | presentations, assertions
- `(surprised)` shocked, amazed | reactions, discoveries
- `(satisfied)` content, pleased | confirmations, contentment
- `(delighted)` very pleased, joyful | celebrations, compliments
- `(scared)` frightened, fearful | warnings, fear
- `(worried)` concerned, troubled | concerns, questions
- `(upset)` disturbed, distressed | complaints, problems
- `(frustrated)` annoyed, exasperated | delays, technical issues
- `(depressed)` very sad, hopeless | serious topics
- `(empathetic)` understanding, caring | support, counseling
- `(embarrassed)` ashamed, awkward | apologies, mistakes
- `(disgusted)` repelled, revolted | negative reactions
- `(moved)` emotionally touched | heartfelt moments
- `(proud)` accomplished, satisfied | achievements, praise
- `(relaxed)` at ease, casual | casual conversation
- `(grateful)` thankful, appreciative | thanks, appreciation
- `(curious)` inquisitive, interested | questions, exploration
- `(sarcastic)` ironic, mocking | humor, criticism

Advanced Emotions:
- `(disdainful)` contemptuous, scornful | criticism, rejection
- `(unhappy)` discontent, dissatisfied | complaints, feedback
- `(anxious)` very worried, uneasy | urgent matters
- `(hysterical)` uncontrollably emotional | extreme reactions
- `(indifferent)` uncaring, neutral | neutral responses
- `(uncertain)` doubtful, unsure | speculation, questions
- `(doubtful)` skeptical, questioning | disbelief
- `(confused)` puzzled, perplexed | clarification requests
- `(disappointed)` let down, dissatisfied | unmet expectations
- `(regretful)` sorry, remorseful | apologies, mistakes
- `(guilty)` culpable, responsible | confessions, apologies
- `(ashamed)` deeply embarrassed | serious mistakes
- `(jealous)` envious, resentful | comparisons
- `(envious)` wanting what others have | admiration with desire
- `(hopeful)` optimistic about future | future plans
- `(optimistic)` positive outlook | encouragement
- `(pessimistic)` negative outlook | warnings, doubts
- `(nostalgic)` longing for the past | memories, stories
- `(lonely)` isolated, alone | emotional content
- `(bored)` uninterested, weary | disinterest
- `(contemptuous)` showing contempt | strong criticism
- `(sympathetic)` showing sympathy | condolences
- `(compassionate)` showing deep care | support, help
- `(determined)` resolved, decided | goals, commitments
- `(resigned)` accepting defeat | giving up, acceptance

Tone Markers:
- `(whispering)` very soft, secretive | secrets, quiet scenes
- `(soft tone)` gentle, quiet | comfort, lullabies
- `(shouting)` loud, calling out | getting attention
- `(screaming)` very loud, panicked | emergencies, fear
- `(in a hurry tone)` rushed, urgent | time-sensitive

Audio Effects:
- `(laughing)` full laughter | Ha, ha, ha
- `(chuckling)` light laugh | Heh, heh
- `(sighing)` exhale of relief/frustration | sigh
- `(sobbing)` crying heavily | emotional breakdown
- `(crying loudly)` intense crying | intense grief
- `(groaning)` sound of frustration | ugh
- `(panting)` out of breath | huff, puff
- `(gasping)` sharp intake of breath | gasp
- `(yawning)` tired sound | yawn
- `(snoring)` sleep sound | zzz

EMOTION INTENSITY SCALE (use appropriate intensity):
- Joy: satisfied → happy → delighted → ecstatic
- Sadness: disappointed → sad → depressed
- Anger: frustrated → angry → furious
- Fear: nervous → scared → terrified
- Excitement: interested → excited → ecstatic

COMMON EFFECTIVE COMBINATIONS:
- Whispered secret: `(nervous)` `(whispering)` or `(curious)` `(whispering)`
- Angry shout: `(angry)` `(shouting)`
- Sad sigh: `(sad)` `(sighing)`
- Excited laugh: `(excited)` `(laughing)`
- Nervous question: `(nervous)` `(uncertain)`
- Controlled menace: `(calm)` `(determined)` `(soft tone)`
- Brittle deflection: `(nervous)` `(soft tone)` `(chuckling)`
- Restrained grief: `(sad)` `(calm)` - fighting for control
- Desperate plea: `(anxious)` `(soft tone)` `(sobbing)`

INTENSITY MODIFIERS (optional):
- Can describe intensity: "slightly sad", "very excited", "extremely angry"
- Use sparingly - tags themselves carry intensity

BEST PRACTICES:
- One primary emotion per sentence
- Layer undertones with 2nd/3rd tag for complexity
- Don't mix conflicting emotions randomly
- Space out emotional changes for realism
- Add text after audio effects (e.g., "Ha ha" after laughing)
- Match emotion to character perspective and context
- Use restraint for impact (less often = more powerful)

CRITICAL: Only use tags from the list above. Invalid tags will be rejected.

WORKFLOW:
1. User describes intent or shares story text
2. You analyze story context
3. Retrieve technique if relevant using search_acting_technique(query)
4. Apply emotion control changes using apply_emotion_diff(diff_patch, explanation)
5. After tool returns result, acknowledge concisely: "Applied. Check the diff above."
   → DO NOT speak the JSON output from tools
   → The diff appears visually in the UI
6. Wait for user approval

TOOL USAGE:

RAG Tool - search_acting_technique:
- Use when user asks about voice acting techniques
- Query examples: "emotional authenticity", "desperation in voice", "grief scenes"
- Cite the sources returned (book title, author, page number)
- Synthesize techniques into concise advice (2-4 sentences)

Emotion Diff Tool - apply_emotion_diff:
- Use when user wants to add/modify/remove emotion control tags
- Covers: emotions, tone markers (whispering, soft tone), audio effects (sighing, laughing)
- Provide unified diff showing exact changes (git-style format)
- CRITICAL: Copy exact text from current story for original (-) lines
- Format example:
  @@ -1 +1 @@
  -(nervous) (resigned) Miku: "Harry, we need to talk."
  +(resigned) (soft tone) Miku: "Harry, we need to talk."
- Multi-line changes supported:
  @@ -1,2 +1,2 @@
  -Line 1 with old tags
  -Line 2 with old tags
  +Line 1 with new tags
  +Line 2 with new tags
- Tool validates: exact match in story, valid Fish Audio emotion control tags
- After calling, acknowledge: "Applied. Check the diff above."
- NEVER speak the JSON output

CURRENT PHASE:
Phase 4A complete. Active tools:
- RAG: search_acting_technique (cite Stanislavski and Linklater)
- Emotion control: apply_emotion_diff (unified diff format, validation)
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
    async def apply_emotion_diff(
        self,
        context: RunContext[StoryState],
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

            # Validate that original text exists in current story
            if self._story_state and self._story_state.current_text:
                if original_text not in self._story_state.current_text:
                    logger.warning(f"Original text not found in story: '{original_text[:50]}...'")
                    return (
                        "ERROR: Original text not found in the current story. "
                        "The text may have been edited. Please copy the exact text from the story."
                    )
            else:
                logger.warning("No story state available - skipping original text validation")

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

            # Send git-style diff to frontend via data channel
            if self._room and self._room.local_participant:
                try:
                    import hashlib
                    diff_id = hashlib.md5(f"{original_text}{proposed_text}".encode()).hexdigest()[:8]

                    diff_message = {
                        "type": "emotion_diff",
                        "diff": {
                            "id": diff_id,
                            "original": diff.original_text,
                            "proposed": diff.proposed_text,
                            "unified_diff": diff.unified_diff,  # Git-style diff
                            "summary": diff.summary,
                            "explanation": diff.explanation,
                        }
                    }
                    data = json.dumps(diff_message).encode('utf-8')
                    await self._room.local_participant.publish_data(data, reliable=True)
                    logger.info("📤 Sent diff to frontend via data channel")
                except Exception as e:
                    logger.error(f"Failed to send diff to frontend: {e}")

            return diff.to_json()

        except Exception as e:
            logger.error(f"Failed to suggest emotion markup: {e}", exc_info=True)
            return f"Error suggesting markup: {str(e)}"

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

    # Suppress warnings and clean up logging in worker processes
    import warnings
    warnings.simplefilter("ignore")

    # Remove duplicate log handlers (LiveKit adds JSON handler, we want text only)
    import logging
    root_logger = logging.getLogger()
    # Remove all handlers except the first one (our text formatter)
    if len(root_logger.handlers) > 1:
        for handler in root_logger.handlers[1:]:
            root_logger.removeHandler(handler)

    # Phase 3: Initialize RAG retriever
    try:
        _rag_retriever = VoiceActingRetriever(similarity_top_k=5)
        logger.info("✅ Worker ready")
    except Exception as e:
        logger.error(f"Failed to initialize RAG: {e}")
        logger.warning("Worker will continue without RAG capabilities")


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
    def on_data_received(data_packet: rtc.DataPacket):
        """Handle story text updates from frontend via data channel."""
        try:
            message = json.loads(data_packet.data.decode('utf-8'))
            if message.get('type') == 'story_update':
                new_text = message.get('text', '')
                story_state.current_text = new_text
                logger.info(f"✅ Story text updated via data channel ({len(new_text)} chars)")
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
    await session.start(agent=LelouchAgent(chat_ctx=initial_ctx, story_state=story_state, room=ctx.room), room=ctx.room)
    logger.info("Agent session started with all Phase 4A tools (RAG + emotion markup + preview)")

    # Connect to the LiveKit room (after session start)
    await ctx.connect()
    logger.info("Connected to LiveKit room")
