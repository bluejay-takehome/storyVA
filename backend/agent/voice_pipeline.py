"""
Voice pipeline configuration for LiveKit agent.

Sets up the STT → LLM → TTS → VAD pipeline for real-time conversation.
"""
import os
from livekit.agents import AgentSession
from livekit.plugins import deepgram, openai, silero
from livekit.plugins.turn_detector import EOUModel
from agent.state import StoryState


async def create_agent_session(user_data: StoryState) -> AgentSession:
    """
    Create LiveKit agent session with configured voice pipeline.

    Pipeline components:
    - VAD: Silero for voice activity detection
    - STT: Deepgram Nova-3 for speech-to-text
    - LLM: OpenAI GPT-5 for conversation
    - TTS: OpenAI TTS (temporary - will swap to Fish Audio in Phase 2B)
    - Turn Detection: End-of-utterance model for interruption handling

    Args:
        user_data: StoryState instance tracking story text and edits

    Returns:
        Configured AgentSession ready for LiveKit room connection
    """

    # Create agent session with voice pipeline
    session = AgentSession[StoryState](
        # Voice Activity Detection
        vad=silero.VAD.load(),

        # Speech-to-Text (Deepgram Nova-3)
        stt=deepgram.STT(
            model="nova-3",
            language="en-US",
            interim_results=True,
            punctuate=True,
            smart_format=True,
            endpointing=300,  # ms of silence before end of utterance
        ),

        # Large Language Model (GPT-5)
        llm=openai.LLM(
            model="gpt-4o",  # Using gpt-4o as GPT-5 may not be available yet
            temperature=0.7,
        ),

        # Text-to-Speech (OpenAI TTS - temporary)
        # TODO: Phase 2B - Replace with Fish Audio TTS
        tts=openai.TTS(
            voice="onyx",  # Deep, authoritative voice for Lelouch
            speed=1.0,
        ),

        # Turn Detection (End-of-utterance model)
        turn_detection=EOUModel(),

        # Interruption Settings
        allow_interruptions=True,
        min_endpointing_delay=0.5,

        # User Data
        user_data=user_data,
    )

    return session
