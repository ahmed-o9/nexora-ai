from typing import Any, Optional

from ..core.config import get_settings
from ..core.exceptions import ProviderError
from .base import BaseProvider


class GeminiProvider(BaseProvider):
    """Google Gemini provider."""

    name = "gemini"

    def __init__(self) -> None:
        self.settings = get_settings()

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

        if not self.settings.GEMINI_API_KEY:
            raise ProviderError(
                "GEMINI_API_KEY is missing. "
                "Add it to .env or use LLM_PROVIDER=mock."
            )

        try:
            from google import genai
            from google.genai import types
        except ImportError as exc:
            raise ProviderError(
                "google-genai is not installed. "
                "Run: pip install google-genai"
            ) from exc

        try:
            client = genai.Client(
                api_key=self.settings.GEMINI_API_KEY
            )

            config_kwargs = {
                "temperature": temperature,
                "max_output_tokens": max_tokens,
            }

            if system_instruction:
                config_kwargs["system_instruction"] = system_instruction

            if json_mode:
                config_kwargs["response_mime_type"] = "application/json"

            response = client.models.generate_content(
                model=self.settings.GEMINI_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(**config_kwargs),
            )

            text = getattr(response, "text", None)

            if not text:
                raise ProviderError(
                    "Gemini returned an empty response."
                )

            return text.strip()

        except ProviderError:
            raise
        except Exception as exc:
            raise ProviderError(
                f"Gemini request failed: {exc}"
            ) from exc