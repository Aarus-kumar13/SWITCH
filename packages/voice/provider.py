import os
import logging
from abc import ABC, abstractmethod
from typing import AsyncGenerator, Optional

logger = logging.getLogger("switch.voice.provider")

class VoiceProvider(ABC):
    @abstractmethod
    async def speech_to_text(self, audio_bytes: bytes) -> str:
        pass

    @abstractmethod
    async def text_to_speech(self, text: str, voice_id: Optional[str] = None) -> bytes:
        pass


class OpenAIVoiceProvider(VoiceProvider):
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.enabled = bool(self.api_key)

    async def speech_to_text(self, audio_bytes: bytes) -> str:
        if not self.enabled:
            logger.info("Speech-To-Text fallback mock processing.")
            return "SWITCH, start my React project development environment."
        
        import openai
        client = openai.AsyncOpenAI(api_key=self.api_key)
        # Call Whisper API
        response = await client.audio.transcriptions.create(
            model="whisper-1",
            file=("audio.wav", audio_bytes, "audio/wav"),
        )
        return response.text

    async def text_to_speech(self, text: str, voice_id: Optional[str] = "alloy") -> bytes:
        if not self.enabled:
            logger.info("Text-To-Speech fallback mock audio generation.")
            return b"RIFF_MOCK_WAV_HEADER_AUDIO_STREAM"
        
        import openai
        client = openai.AsyncOpenAI(api_key=self.api_key)
        response = await client.audio.speech.create(
            model="tts-1",
            voice=voice_id or "alloy",
            input=text,
        )
        return response.content
