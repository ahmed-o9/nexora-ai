from typing import Any, Optional

from ..core.config import get_settings
from ..core.exceptions import ProviderError
from .base import BaseProvider
from .gemini import GeminiProvider
from .mock import MockProvider


class ProviderRouter(BaseProvider):
    """
    Selects the configured provider.

    Supported:
        mock
        gemini
    """

    name = "router"

    def __init__(self) -> None:
        settings = get_settings()
        provider_name = settings.LLM_PROVIDER.strip().lower()

        self.providers = {
            "mock": MockProvider(),
            "gemini": GeminiProvider(),
        }

        if provider_name not in self.providers:
            raise ProviderError(
                f"Unsupported LLM_PROVIDER: {provider_name}. "
                f"Use one of: {', '.join(self.providers)}"
            )

        self.provider_name = provider_name
        self.provider = self.providers[provider_name]

    async def generate(
        self,
        prompt: str,
        *,
        system_instruction: Optional[str] = None,
        json_mode: bool = False,
        temperature: float = 0.4,
        max_tokens: int = 1500,
        **kwargs: Any,
    ) -> str:

        return await self.provider.generate(
            prompt,
            system_instruction=system_instruction,
            json_mode=json_mode,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs,
        )

    async def health(self):
        return await self.provider.health()