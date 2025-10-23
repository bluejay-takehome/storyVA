#!/usr/bin/env python3
"""
StoryVA Voice Director Agent - Main Entry Point

LiveKit agent that helps writers add Fish Audio emotion markup to stories.
Agent personality: Lelouch - brilliant strategist turned voice director.
"""
import os
import sys

# Filter warnings BEFORE any imports that might trigger them
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", module="pydantic")

import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Disable LiveKit's JSON logging - use plain text only
os.environ["LIVEKIT_LOG_LEVEL"] = "WARN"

# Configure logging BEFORE importing livekit
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    force=True
)

# Silence noisy loggers
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("openai._base_client").setLevel(logging.WARNING)
logging.getLogger("asyncio").setLevel(logging.WARNING)
logging.getLogger("livekit").setLevel(logging.ERROR)  # Only show errors, not warnings
logging.getLogger("livekit.agents").setLevel(logging.ERROR)

# NOW import livekit after logging is configured
from livekit.agents import cli, WorkerOptions
from agent.lelouch import entrypoint, prewarm

logger = logging.getLogger("storyva")


def verify_environment():
    """Verify all required environment variables are present."""
    logger.info("=" * 60)
    logger.info("  StoryVA - Voice Director Agent")
    logger.info("=" * 60)
    logger.info("")

    # Verify environment variables
    required_vars = [
        "LIVEKIT_URL",
        "LIVEKIT_API_KEY",
        "LIVEKIT_API_SECRET",
        "DEEPGRAM_API_KEY",
        "FISH_AUDIO_API_KEY",
        "FISH_LELOUCH_VOICE_ID",
        "PINECONE_API_KEY",
    ]

    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        logger.error("Please check backend/.env file")
        return False

    # Check for OpenAI API key (can be in system env or .env)
    if not os.getenv("OPENAI_API_KEY"):
        logger.warning("OPENAI_API_KEY not found in environment")
        logger.warning("Make sure it's available in system environment variables")

    logger.info("✅ Environment configuration verified")
    logger.info("")
    logger.info("Starting LiveKit agent worker...")
    logger.info("=" * 60)
    logger.info("")

    return True


if __name__ == "__main__":
    # Verify environment before starting
    if not verify_environment():
        exit(1)

    # Remove LiveKit's JSON handler to prevent duplicate logs
    root_logger = logging.getLogger()
    # Keep only our BasicConfig handler (first one), remove others
    if len(root_logger.handlers) > 1:
        root_logger.handlers = root_logger.handlers[:1]

    # Start LiveKit agent worker with agent name matching frontend configuration
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            prewarm_fnc=prewarm,
            agent_name="storyva-voice-director",  # Must match agentName in frontend/app-config.ts
        )
    )
