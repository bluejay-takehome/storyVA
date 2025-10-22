#!/usr/bin/env python3
"""
Test script for Fish Audio TTS integration.

Tests WebSocket connection and emotion markup support.
"""
import os
import sys
import asyncio
import logging
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from tts.fish_audio import FishAudioTTS

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


async def test_fish_audio():
    """Test Fish Audio TTS with various inputs."""
    logger.info("=" * 60)
    logger.info("  Fish Audio TTS Test")
    logger.info("=" * 60)

    # Verify API key
    api_key = os.getenv("FISH_AUDIO_API_KEY")
    voice_id = os.getenv("FISH_LELOUCH_VOICE_ID")

    if not api_key:
        logger.error("FISH_AUDIO_API_KEY not found in environment")
        return False

    if not voice_id:
        logger.error("FISH_LELOUCH_VOICE_ID not found in environment")
        return False

    logger.info(f"API Key: {api_key[:8]}...")
    logger.info(f"Voice ID: {voice_id}")

    # Initialize Fish Audio TTS
    logger.info("\n1. Initializing Fish Audio TTS...")
    fish_tts = FishAudioTTS(
        api_key=api_key,
        reference_id=voice_id,
        latency="normal",
        format="opus",
    )

    # Test cases
    test_cases = [
        {
            "name": "Plain Text",
            "text": "Hello, I am Lelouch. This is a test of the Fish Audio system.",
        },
        {
            "name": "Confident Emotion",
            "text": "(confident) I will change the world through strategic brilliance.",
        },
        {
            "name": "Multiple Tags",
            "text": "(excited)(laughing) Victory is ours! The plan succeeded perfectly.",
        },
        {
            "name": "Mixed Emotions",
            "text": "(sad) I regret what must be done. (pause) (determined) But I will not waver.",
        },
    ]

    for i, test_case in enumerate(test_cases, 1):
        logger.info(f"\n{i}. Testing: {test_case['name']}")
        logger.info(f"   Text: {test_case['text']}")

        try:
            # Synthesize text
            stream = fish_tts.synthesize(test_case["text"])

            # Collect audio chunks
            audio_chunks = []
            total_bytes = 0

            # Iterate over audio chunks
            async for event in stream:
                if isinstance(event, Exception):
                    logger.error(f"   ❌ Error: {event}")
                    break

                # ChunkedStream yields SynthesizedAudio events
                audio_chunks.append(event)
                if hasattr(event, 'data'):
                    total_bytes += len(event.data)

            if total_bytes > 0:
                logger.info(f"   ✅ Received {len(audio_chunks)} chunks, {total_bytes} bytes total")

                # Estimate duration (rough calculation for opus)
                # Opus is variable bitrate, but roughly 16kbps for speech
                duration_estimate = (total_bytes * 8) / 16000
                logger.info(f"   Estimated duration: ~{duration_estimate:.2f}s")
            elif len(audio_chunks) > 0:
                logger.info(f"   ✅ Received {len(audio_chunks)} audio events")
            else:
                logger.warning(f"   ⚠️  No audio data received")

        except Exception as e:
            logger.error(f"   ❌ Test failed: {e}", exc_info=True)
            return False

    logger.info("\n" + "=" * 60)
    logger.info("  All tests completed!")
    logger.info("=" * 60)
    return True


if __name__ == "__main__":
    success = asyncio.run(test_fish_audio())
    sys.exit(0 if success else 1)
