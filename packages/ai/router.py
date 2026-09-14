import os
import logging
from typing import Any, Dict, List, Optional
from packages.ai.providers import (
    BaseAIProvider,
    OpenAIProvider,
    AnthropicProvider,
    GoogleGeminiProvider,
    MockLocalProvider,
)
from packages.shared.schemas import ModelCategory

logger = logging.getLogger("switch.ai.router")

class AIRouter:
    def __init__(self):
        self.providers: Dict[str, BaseAIProvider] = {}
        self._initialize_providers()

    def _initialize_providers(self):
        # OpenAI
        if os.getenv("OPENAI_API_KEY"):
            try:
                self.providers["openai"] = OpenAIProvider()
                logger.info("OpenAI Provider initialized.")
            except Exception as e:
                logger.warning(f"Failed to initialize OpenAI provider: {e}")

        # Anthropic
        if os.getenv("ANTHROPIC_API_KEY"):
            try:
                self.providers["anthropic"] = AnthropicProvider()
                logger.info("Anthropic Provider initialized.")
            except Exception as e:
                logger.warning(f"Failed to initialize Anthropic provider: {e}")

        # Google Gemini
        if os.getenv("GEMINI_API_KEY"):
            try:
                self.providers["gemini"] = GoogleGeminiProvider()
                logger.info("Google Gemini Provider initialized.")
            except Exception as e:
                logger.warning(f"Failed to initialize Gemini provider: {e}")

        # Fallback Local Mock Provider
        self.providers["local"] = MockLocalProvider()

    def get_provider(self, category: ModelCategory = ModelCategory.REASONING) -> BaseAIProvider:
        """Select appropriate provider based on model category and active API keys."""
        if category == ModelCategory.REASONING:
            if "anthropic" in self.providers:
                return self.providers["anthropic"]
            elif "openai" in self.providers:
                return self.providers["openai"]
        elif category == ModelCategory.FAST:
            if "openai" in self.providers:
                return self.providers["openai"]
            elif "gemini" in self.providers:
                return self.providers["gemini"]
        elif category == ModelCategory.VISION:
            if "openai" in self.providers:
                return self.providers["openai"]
            elif "gemini" in self.providers:
                return self.providers["gemini"]

        # Default fallback to any configured provider or local
        for key in ["openai", "anthropic", "gemini"]:
            if key in self.providers:
                return self.providers[key]

        return self.providers["local"]

    async def route_and_generate(
        self,
        prompt: str,
        category: ModelCategory = ModelCategory.REASONING,
        system_prompt: Optional[str] = None,
        messages: Optional[List[Dict[str, str]]] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ) -> str:
        provider = self.get_provider(category)
        return await provider.generate_text(
            prompt=prompt,
            system_prompt=system_prompt,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )

    async def route_and_generate_structured(
        self,
        prompt: str,
        response_schema: Dict[str, Any],
        category: ModelCategory = ModelCategory.REASONING,
        system_prompt: Optional[str] = None,
    ) -> Dict[str, Any]:
        provider = self.get_provider(category)
        return await provider.generate_structured(
            prompt=prompt,
            response_schema=response_schema,
            system_prompt=system_prompt,
        )
