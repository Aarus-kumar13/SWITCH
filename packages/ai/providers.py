import os
import json
import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from packages.shared.schemas import ModelCategory

logger = logging.getLogger("switch.ai.providers")

class BaseAIProvider(ABC):
    @abstractmethod
    async def generate_text(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        messages: Optional[List[Dict[str, str]]] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ) -> str:
        pass

    @abstractmethod
    async def generate_structured(
        self,
        prompt: str,
        response_schema: Dict[str, Any],
        system_prompt: Optional[str] = None,
    ) -> Dict[str, Any]:
        pass


class OpenAIProvider(BaseAIProvider):
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.enabled = bool(self.api_key)
        if self.enabled:
            import openai
            self.client = openai.AsyncOpenAI(api_key=self.api_key)
        else:
            self.client = None

    async def generate_text(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        messages: Optional[List[Dict[str, str]]] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        model: str = "gpt-4o",
    ) -> str:
        if not self.enabled:
            raise ValueError("OpenAI API key not configured")
        
        formatted_messages = []
        if system_prompt:
            formatted_messages.append({"role": "system", "content": system_prompt})
        if messages:
            formatted_messages.extend(messages)
        else:
            formatted_messages.append({"role": "user", "content": prompt})

        response = await self.client.chat.completions.create(
            model=model,
            messages=formatted_messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content or ""

    async def generate_structured(
        self,
        prompt: str,
        response_schema: Dict[str, Any],
        system_prompt: Optional[str] = None,
        model: str = "gpt-4o",
    ) -> Dict[str, Any]:
        if not self.enabled:
            raise ValueError("OpenAI API key not configured")
        
        sys_p = (system_prompt or "") + "\nRespond ONLY with valid JSON conforming strictly to the requested structure."
        res_text = await self.generate_text(prompt, system_prompt=sys_p, model=model)
        try:
            cleaned = res_text.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:-3].strip()
            elif cleaned.startswith("```"):
                cleaned = cleaned[3:-3].strip()
            return json.loads(cleaned)
        except Exception as e:
            logger.error(f"Failed to parse structured response from OpenAI: {e}")
            return {}


class AnthropicProvider(BaseAIProvider):
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.enabled = bool(self.api_key)
        if self.enabled:
            import anthropic
            self.client = anthropic.AsyncAnthropic(api_key=self.api_key)
        else:
            self.client = None

    async def generate_text(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        messages: Optional[List[Dict[str, str]]] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        model: str = "claude-3-5-sonnet-20240620",
    ) -> str:
        if not self.enabled:
            raise ValueError("Anthropic API key not configured")

        formatted_messages = []
        if messages:
            formatted_messages.extend(messages)
        else:
            formatted_messages.append({"role": "user", "content": prompt})

        response = await self.client.messages.create(
            model=model,
            system=system_prompt or "",
            messages=formatted_messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.content[0].text if response.content else ""

    async def generate_structured(
        self,
        prompt: str,
        response_schema: Dict[str, Any],
        system_prompt: Optional[str] = None,
    ) -> Dict[str, Any]:
        sys_p = (system_prompt or "") + "\nRespond ONLY with valid JSON conforming to the requested format."
        text = await self.generate_text(prompt, system_prompt=sys_p)
        try:
            cleaned = text.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:-3].strip()
            return json.loads(cleaned)
        except Exception:
            return {}


class GoogleGeminiProvider(BaseAIProvider):
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.enabled = bool(self.api_key)

    async def generate_text(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        messages: Optional[List[Dict[str, str]]] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        model: str = "gemini-1.5-pro",
    ) -> str:
        if not self.enabled:
            raise ValueError("Google Gemini API key not configured")
        import httpx
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={self.api_key}"
        payload = {
            "contents": [{"parts": [{"text": (system_prompt or "") + "\n\n" + prompt}]}]
        }
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, json=payload, timeout=30.0)
            data = resp.json()
            try:
                return data["candidates"][0]["content"]["parts"][0]["text"]
            except KeyError:
                return str(data)

    async def generate_structured(
        self,
        prompt: str,
        response_schema: Dict[str, Any],
        system_prompt: Optional[str] = None,
    ) -> Dict[str, Any]:
        res = await self.generate_text(prompt, system_prompt=(system_prompt or "") + " Return JSON only.")
        try:
            cleaned = res.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:-3].strip()
            return json.loads(cleaned)
        except Exception:
            return {}


class MockLocalProvider(BaseAIProvider):
    """Fallback local intelligent provider for offline/keyless local operation."""
    async def generate_text(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        messages: Optional[List[Dict[str, str]]] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ) -> str:
        logger.info(f"MockLocalProvider handling prompt: {prompt[:60]}...")
        p_lower = prompt.lower()
        if "react" in p_lower or "node" in p_lower or "error" in p_lower or "project" in p_lower:
            return (
                "I analyzed your request regarding the project. "
                "I identified that package dependencies and server states should be verified. "
                "I recommend executing a dependency check and starting the dev server."
            )
        elif "battery" in p_lower or "status" in p_lower:
            return "Your system telemetry is normal. Battery state and system processes are actively monitored."
        else:
            return f"SWITCH Autonomous OS initialized. Request received: '{prompt}'. Ready to assist."

    async def generate_structured(
        self,
        prompt: str,
        response_schema: Dict[str, Any],
        system_prompt: Optional[str] = None,
    ) -> Dict[str, Any]:
        return {
            "intent": "general_assistance",
            "action_plan": ["Analyze request", "Formulate steps", "Execute tools", "Verify output"],
            "requires_approval": False,
            "confidence": 0.95,
        }
