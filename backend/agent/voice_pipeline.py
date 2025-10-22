"""
Voice pipeline configuration for LiveKit agent.

Sets up the STT → LLM → TTS → VAD pipeline for real-time conversation.
"""
import os
from agent.state import StoryState


# TODO: Phase 2 - Implement actual voice pipeline
# from livekit.agents import AgentSession
# from livekit.plugins import deepgram, openai, silero
# from livekit.plugins.turn_detector.multilingual import MultilingualModel
# from tts.fish_audio import FishAudioTTS


async def create_agent_session(user_data: StoryState):
    """
    Create LiveKit agent session with configured voice pipeline.

    Pipeline components:
    - VAD: Silero for voice activity detection
    - STT: Deepgram Nova-3 for speech-to-text
    - LLM: OpenAI GPT-5 for conversation
    - TTS: Fish Audio (custom implementation) for text-to-speech
    - Turn Detection: Multilingual model for interruption handling

    Args:
        user_data: StoryState instance tracking story text and edits

    Returns:
        Configured AgentSession ready for LiveKit room connection
    """
    # TODO: Phase 2 implementation
    # session = AgentSession[StoryState](
    #     vad=silero.VAD.load(),
    #     stt=deepgram.STT(
    #         model="nova-3",
    #         language="en-US",
    #         interim_results=True,
    #         punctuate=True,
    #         smart_format=True,
    #         endpointing_ms=300,
    #     ),
    #     llm=openai.LLM(
    #         model="gpt-5",
    #         temperature=0.7,
    #     ),
    #     tts=FishAudioTTS(
    #         api_key=os.getenv("FISH_AUDIO_API_KEY"),
    #         reference_id=os.getenv("FISH_LELOUCH_VOICE_ID"),
    #         latency="normal",
    #         format="opus",
    #     ),
    #     turn_detection=MultilingualModel(),
    #     allow_interruptions=True,
    #     min_interruption_duration=0.5,
    #     userdata=user_data,
    # )
    # return session

    raise NotImplementedError("Voice pipeline implementation pending (Phase 2)")
