"""
Custom Fish Audio TTS integration for LiveKit.

Uses the official Fish Audio SDK for reliable streaming TTS,
supporting 60+ emotion tags for voice direction.
"""
import asyncio
import logging
from typing import Optional, Callable, Awaitable
from fish_audio_sdk import Session, TTSRequest
from livekit.agents import tts, APIConnectOptions
from livekit.agents.types import DEFAULT_API_CONNECT_OPTIONS

logger = logging.getLogger(__name__)

SAMPLE_RATE = 24000
NUM_CHANNELS = 1


class FishAudioTTS(tts.TTS):
    """
    Custom TTS implementation for Fish Audio with LiveKit.

    Uses the official Fish Audio SDK for streaming synthesis
    with emotion markup tags.
    """

    def __init__(
        self,
        *,
        api_key: str,
        reference_id: str,  # Voice model ID
        model: str = "s1",  # Latest Fish Audio model
        latency: str = "normal",
        format: str = "mp3",  # SDK supports: mp3, wav, pcm
        on_text_synthesizing: Optional[Callable[[str], Awaitable[None]]] = None,  # Callback when synthesis starts
    ):
        super().__init__(
            capabilities=tts.TTSCapabilities(streaming=False),  # Using ChunkedStream
            sample_rate=SAMPLE_RATE,
            num_channels=NUM_CHANNELS,
        )
        self._api_key = api_key
        self._reference_id = reference_id
        self._model = model
        self._latency = latency
        self._format = format
        self._on_text_synthesizing = on_text_synthesizing

        # Initialize Fish Audio SDK session
        self._session = Session(api_key)

        logger.info(
            f"Initialized FishAudioTTS (voice={reference_id[:8]}..., "
            f"model={model}, format={format}, latency={latency})"
        )

    @property
    def model(self) -> str:
        return self._model

    @property
    def provider(self) -> str:
        return "fish.audio"

    def synthesize(
        self, text: str, *, conn_options: APIConnectOptions = DEFAULT_API_CONNECT_OPTIONS
    ) -> "ChunkedStream":
        """Synthesize text using Fish Audio SDK."""
        return ChunkedStream(tts=self, input_text=text, conn_options=conn_options)


class ChunkedStream(tts.ChunkedStream):
    """
    Streaming TTS using Fish Audio SDK.

    The SDK handles all WebSocket protocol details and returns
    audio chunks that we push to LiveKit's audio emitter.
    """

    def __init__(self, *, tts: FishAudioTTS, input_text: str, conn_options: APIConnectOptions):
        super().__init__(tts=tts, input_text=input_text, conn_options=conn_options)
        self._tts: FishAudioTTS = tts

    async def _run(self, output_emitter: tts.AudioEmitter) -> None:
        """
        Main synthesis loop - uses Fish Audio SDK to stream audio.

        Args:
            output_emitter: LiveKit's audio emitter for sending frames
        """
        try:
            logger.info(f"Synthesizing with Fish Audio: {self.input_text}")

            # Create TTS request
            request = TTSRequest(
                text=self.input_text,
                reference_id=self._tts._reference_id,
                format=self._tts._format,
                latency=self._tts._latency,
                chunk_length=200,  # Default from docs
                normalize=True,  # Default from docs
            )

            # Initialize emitter
            output_emitter.initialize(
                request_id="",  # Fish Audio SDK doesn't expose request IDs
                sample_rate=SAMPLE_RATE,
                num_channels=NUM_CHANNELS,
                mime_type=f"audio/{self._tts._format}",
            )

            # The SDK's tts() method returns an iterator of audio chunks
            # We need to run it in a thread pool since it's synchronous
            loop = asyncio.get_event_loop()

            def _generate_chunks():
                """Synchronous generator wrapper for SDK."""
                chunks = []
                try:
                    for chunk in self._tts._session.tts(request, backend=self._tts._model):
                        chunks.append(chunk)
                    logger.info(f"Fish Audio generated {len(chunks)} audio chunks")
                    return chunks
                except Exception as e:
                    logger.error(f"Fish Audio SDK error: {e}", exc_info=True)
                    raise

            # Run synchronous SDK call in thread pool
            chunks = await loop.run_in_executor(None, _generate_chunks)

            # Push all chunks to emitter
            text_sent = False
            for i, chunk in enumerate(chunks):
                output_emitter.push(chunk)

                # Send text to frontend after first audio chunk is pushed (audio is playing now)
                if i == 0 and not text_sent and self._tts._on_text_synthesizing:
                    text_sent = True
                    try:
                        await self._tts._on_text_synthesizing(self.input_text)
                    except Exception as e:
                        logger.error(f"Error in on_text_synthesizing callback: {e}")

            # Flush remaining audio
            output_emitter.flush()
            logger.info("Fish Audio synthesis complete")

        except Exception as e:
            logger.error(f"Fish Audio synthesis error: {e}", exc_info=True)
            raise
