"""
Fish Audio Preview Client

Generates audio previews using Fish Audio HTTP API with character voices.
Different voices for male/female characters (distinct from agent's Lelouch voice).
"""
import os
import hashlib
import logging
from pathlib import Path
from typing import Optional, Literal
import httpx


logger = logging.getLogger(__name__)


class FishAudioPreview:
    """
    Client for Fish Audio HTTP API to generate preview audio.

    Uses character voices (male/female) different from the agent's Lelouch voice
    for distinguishing between director (agent) and character (preview).
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        male_voice_id: Optional[str] = None,
        female_voice_id: Optional[str] = None,
    ):
        """
        Initialize Fish Audio preview client.

        Args:
            api_key: Fish Audio API key (defaults to FISH_AUDIO_API_KEY env var)
            male_voice_id: Voice ID for male characters (defaults to FISH_MALE_VOICE_ID)
            female_voice_id: Voice ID for female characters (defaults to FISH_FEMALE_VOICE_ID)
        """
        self.api_key = api_key or os.getenv("FISH_AUDIO_API_KEY")
        self.male_voice_id = male_voice_id or os.getenv("FISH_MALE_VOICE_ID")
        self.female_voice_id = female_voice_id or os.getenv("FISH_FEMALE_VOICE_ID")

        self.base_url = "https://api.fish.audio/v1/tts"

        # Validate configuration
        if not self.api_key:
            raise ValueError("Fish Audio API key not configured")

        if not self.male_voice_id or not self.female_voice_id:
            logger.warning("Character voice IDs not configured - using defaults")

        logger.info(
            f"FishAudioPreview initialized (male_voice={self.male_voice_id[:8]}..., "
            f"female_voice={self.female_voice_id[:8]}...)"
        )

    async def generate_preview(
        self,
        text: str,
        character_gender: Literal["male", "female", "neutral"] = "neutral",
        format: str = "mp3",
        latency: str = "balanced",
    ) -> Path:
        """
        Generate audio preview with Fish Audio using character voice.

        Args:
            text: Text with emotion markup tags (e.g., "(sad) Hello")
            character_gender: Character gender for voice selection
            format: Audio format (mp3, wav, opus)
            latency: Latency mode (normal, balanced, aggressive)

        Returns:
            Path to saved audio file

        Raises:
            httpx.HTTPError: If API request fails

        Example:
            >>> preview = FishAudioPreview()
            >>> audio_path = await preview.generate_preview(
            ...     "(sad)(whispering) I'm leaving",
            ...     character_gender="female"
            ... )
            >>> print(audio_path)
            PosixPath('/tmp/fish_preview_abc123.mp3')
        """
        # Select appropriate character voice
        reference_id = self._select_voice(character_gender)

        # Prepare request
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "text": text,
            "reference_id": reference_id,
            "format": format,
            "latency": latency,
        }

        logger.info(
            f"Generating Fish Audio preview (gender={character_gender}, "
            f"voice={reference_id[:8]}..., text='{text[:50]}...')"
        )

        # Make HTTP request
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                self.base_url,
                headers=headers,
                json=payload,
            )

            if response.status_code == 200:
                # Save audio to temp file
                audio_data = response.content
                output_path = self._generate_output_path(text, format)

                with open(output_path, "wb") as f:
                    f.write(audio_data)

                logger.info(
                    f"✅ Fish Audio preview generated: {output_path} "
                    f"({len(audio_data)} bytes)"
                )

                return output_path

            else:
                error_msg = (
                    f"Fish Audio API error: {response.status_code} - {response.text}"
                )
                logger.error(error_msg)
                raise httpx.HTTPError(error_msg)

    def _select_voice(self, gender: str) -> str:
        """
        Select appropriate character voice based on gender.

        Args:
            gender: "male", "female", or "neutral"

        Returns:
            Fish Audio voice reference ID
        """
        voice_map = {
            "male": self.male_voice_id,
            "female": self.female_voice_id,
            "neutral": self.male_voice_id,  # Default to male for neutral/unknown
        }

        voice_id = voice_map.get(gender, self.male_voice_id)

        logger.debug(f"Selected voice for gender '{gender}': {voice_id[:8]}...")

        return voice_id

    def _generate_output_path(self, text: str, format: str) -> Path:
        """
        Generate unique output path for audio file.

        Args:
            text: Input text (for generating unique hash)
            format: Audio format extension

        Returns:
            Path to output file in /tmp directory
        """
        # Generate unique hash from text
        text_hash = hashlib.md5(text.encode()).hexdigest()[:8]

        # Create filename
        filename = f"fish_preview_{text_hash}.{format}"
        output_path = Path("/tmp") / filename

        return output_path


# Helper function for gender inference from text
def infer_character_gender(text: str, context: str = "") -> Literal["male", "female", "neutral"]:
    """
    Infer character gender from text and context.

    Uses simple heuristics:
    - Pronouns: he/him/his → male, she/her/hers → female
    - Common names: Marcus/John → male, Sarah/Emma → female
    - Dialogue attribution: "she said" → female, "he replied" → male

    Args:
        text: The dialogue line or marked-up text
        context: Additional context (surrounding text, character names, etc.)

    Returns:
        "male", "female", or "neutral"

    Example:
        >>> infer_character_gender('"I\'m leaving," she said.')
        "female"

        >>> infer_character_gender('"Hello," Marcus replied.')
        "male"
    """
    import re

    # Combine text and context for analysis
    full_text = (text + " " + context).lower()

    # Female pronouns/indicators
    female_indicators = [
        r'\bshe\b', r'\bher\b', r'\bhers\b', r'\bherself\b',
        r'\bshe said\b', r'\bshe replied\b', r'\bshe whispered\b',
        # Common female names
        r'\bsarah\b', r'\bemma\b', r'\bmary\b', r'\bjane\b', r'\blisa\b',
    ]

    # Male pronouns/indicators
    male_indicators = [
        r'\bhe\b', r'\bhim\b', r'\bhis\b', r'\bhimself\b',
        r'\bhe said\b', r'\bhe replied\b', r'\bhe whispered\b',
        # Common male names
        r'\bmarcus\b', r'\bjohn\b', r'\bdavid\b', r'\bmichael\b', r'\bjames\b',
    ]

    # Count matches
    female_matches = sum(1 for pattern in female_indicators if re.search(pattern, full_text))
    male_matches = sum(1 for pattern in male_indicators if re.search(pattern, full_text))

    # Determine gender based on matches
    if female_matches > male_matches:
        return "female"
    elif male_matches > female_matches:
        return "male"
    else:
        return "neutral"


# Convenience function for quick preview generation
async def quick_preview(
    text: str,
    character_gender: Optional[str] = None,
    context: str = ""
) -> Path:
    """
    Quick audio preview generation with automatic gender inference.

    Args:
        text: Marked-up text to preview
        character_gender: Override gender (if None, will infer from text)
        context: Additional context for gender inference

    Returns:
        Path to generated audio file

    Example:
        >>> audio_path = await quick_preview('(sad) "I\'m leaving," she said.')
        >>> # Automatically infers female gender from "she said"
    """
    # Infer gender if not provided
    if character_gender is None:
        character_gender = infer_character_gender(text, context)

    # Generate preview
    preview_client = FishAudioPreview()
    return await preview_client.generate_preview(text, character_gender)
