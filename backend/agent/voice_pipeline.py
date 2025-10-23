"""
Voice pipeline configuration for LiveKit agent.

Sets up the STT → LLM → TTS → VAD pipeline for real-time conversation.
"""
import os
from livekit.agents import AgentSession
from livekit.plugins import deepgram, openai, silero
from agent.state import StoryState
from tts.fish_audio import FishAudioTTS


async def create_agent_session(user_data: StoryState) -> AgentSession:
    """
    Create LiveKit agent session with configured voice pipeline.

    Pipeline components:
    - VAD: Silero for voice activity detection
    - STT: Deepgram Nova-3 for speech-to-text
    - LLM: OpenAI GPT-5 for conversation
    - TTS: Fish Audio S1 with Lelouch voice (supports 60+ emotion tags)
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
        ),

        # Large Language Model (GPT-5)
        # Note: gpt-5 with reasoning_effort doesn't support custom temperature
        llm=openai.LLM(
            model="gpt-5",
        ),

        # Text-to-Speech (Fish Audio with Lelouch voice)
        tts=FishAudioTTS(
            api_key=os.getenv("FISH_AUDIO_API_KEY"),
            reference_id=os.getenv("FISH_LELOUCH_VOICE_ID"),
            latency="normal",
            format="mp3",  # SDK supports: mp3, wav, pcm
        ),

        # Turn Detection (auto-selected: will use vad → stt → manual fallback)
        # Can explicitly set to "vad", "stt", "realtime_llm", or "manual"
        # Leaving as NOT_GIVEN for automatic selection

        # Interruption Settings
        allow_interruptions=True,
        min_endpointing_delay=0.5,

        # User Data
        userdata=user_data,
    )

    return session
