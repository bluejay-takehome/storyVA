#!/usr/bin/env python3
"""
StoryVA Voice Director Agent - Main Entry Point

LiveKit agent that helps writers add Fish Audio emotion markup to stories.
Agent personality: Lelouch - brilliant strategist turned voice director.
"""
import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("storyva")


def main():
    """Main entry point for StoryVA backend."""
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
        "PINECONE_API_KEY",
    ]

    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        logger.error("Please check backend/.env file")
        return 1

    # Check for OpenAI API key (can be in system env or .env)
    if not os.getenv("OPENAI_API_KEY"):
        logger.warning("OPENAI_API_KEY not found in environment")
        logger.warning("Make sure it's available in system environment variables")

    logger.info("✅ Environment configuration verified")
    logger.info("")

    # TODO: Phase 2 - Implement LiveKit agent worker
    # from livekit.agents import cli, WorkerOptions
    # from agent.lelouch import entrypoint, prewarm
    #
    # cli.run_app(
    #     WorkerOptions(
    #         entrypoint_fnc=entrypoint,
    #         prewarm_fnc=prewarm,
    #     )
    # )

    logger.info("Backend structure ready!")
    logger.info("Next: Implement voice pipeline in Phase 2")
    logger.info("")
    logger.info("=" * 60)

    return 0


if __name__ == "__main__":
    exit(main())
