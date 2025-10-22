"""
Custom Fish Audio TTS integration for LiveKit.

Implements WebSocket streaming TTS with Fish Audio's API,
supporting 60+ emotion tags for voice direction.
"""
import os
import asyncio
import logging
from typing import Optional
import ormsgpack
import websockets
from livekit.agents import tts, APIConnectOptions
from livekit.agents.types import DEFAULT_API_CONNECT_OPTIONS

logger = logging.getLogger(__name__)

SAMPLE_RATE = 24000
NUM_CHANNELS = 1


class FishAudioTTS(tts.TTS):
    """
    Custom TTS implementation for Fish Audio with LiveKit.

    Supports WebSocket streaming for low-latency synthesis
    with emotion markup tags.
    """

    def __init__(
        self,
        *,
        api_key: str,
        reference_id: str,  # Voice model ID
        model: str = "speech-1.6",
        latency: str = "normal",
        format: str = "opus",
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

        logger.info(
            f"Initialized FishAudioTTS (voice={reference_id[:8]}..., "
            f"format={format}, latency={latency})"
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
        """Synthesize text using Fish Audio WebSocket API."""
        return ChunkedStream(tts=self, input_text=text, conn_options=conn_options)


class ChunkedStream(tts.ChunkedStream):
    """
    Streaming TTS using Fish Audio WebSocket API.

    Connects to wss://api.fish.audio/v1/tts/live
    and streams audio chunks.
    """

    def __init__(self, *, tts: FishAudioTTS, input_text: str, conn_options: APIConnectOptions):
        super().__init__(tts=tts, input_text=input_text, conn_options=conn_options)
        self._tts: FishAudioTTS = tts

    async def _run(self, output_emitter: tts.AudioEmitter) -> None:
        """
        Main synthesis loop - connects to Fish Audio and streams audio.

        Args:
            output_emitter: LiveKit's audio emitter for sending frames
        """
        ws_uri = "wss://api.fish.audio/v1/tts/live"
        headers = {"Authorization": f"Bearer {self._tts._api_key}"}

        logger.debug(f"Connecting to Fish Audio: {ws_uri}")

        try:
            async with websockets.connect(ws_uri, additional_headers=headers) as ws:
                # Send initial configuration
                config_msg = ormsgpack.packb({
                    "event": "start",
                    "request": {
                        "text": self.input_text,  # Send all text at once
                        "reference_id": self._tts._reference_id,
                        "latency": self._tts._latency,
                        "format": self._tts._format,
                    },
                })
                await ws.send(config_msg)
                logger.debug(f"Sent synthesis request for text: {self.input_text[:50]}...")

                # Initialize emitter
                output_emitter.initialize(
                    request_id="",  # Fish Audio doesn't provide request IDs
                    sample_rate=SAMPLE_RATE,
                    num_channels=NUM_CHANNELS,
                    mime_type=f"audio/{self._tts._format}",
                )

                # Receive audio frames with timeout for completion detection
                # Fish Audio may not send explicit "finish" event - use timeout
                receive_timeout = 5.0  # seconds to wait for next message

                while True:
                    try:
                        # Wait for next message with timeout
                        message = await asyncio.wait_for(ws.recv(), timeout=receive_timeout)
                        data = ormsgpack.unpackb(message)
                        event = data.get("event")

                        logger.debug(f"Received event: {event}")

                        if event == "audio":
                            # Push audio data to emitter
                            audio_bytes = data.get("audio")
                            if audio_bytes:
                                output_emitter.push(audio_bytes)
                                logger.debug(f"Pushed {len(audio_bytes)} bytes of audio")

                        elif event == "finish":
                            logger.debug("Fish Audio synthesis complete (finish event)")
                            break

                        elif event == "done" or event == "end":
                            logger.debug(f"Fish Audio synthesis complete ({event} event)")
                            break

                        elif event == "error":
                            error_msg = data.get("message", "Unknown error")
                            logger.error(f"Fish Audio error: {error_msg}")
                            raise Exception(f"Fish Audio API error: {error_msg}")

                    except asyncio.TimeoutError:
                        # No message received within timeout - assume synthesis complete
                        logger.debug("No messages received for 5s, synthesis assumed complete")
                        break

                    except websockets.exceptions.ConnectionClosed:
                        # WebSocket closed by server
                        logger.debug("Fish Audio WebSocket closed by server")
                        break

                # Synthesis complete
                logger.debug("Fish Audio synthesis complete")

                # Flush remaining audio
                output_emitter.flush()

        except websockets.exceptions.WebSocketException as e:
            logger.error(f"WebSocket error: {e}")
            raise
        except Exception as e:
            logger.error(f"Fish Audio synthesis error: {e}")
            raise
