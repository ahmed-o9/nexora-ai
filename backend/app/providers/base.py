from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class BaseProvider(ABC):
    """Common interface for all LLM providers."""

    name: str = "base"

    @abstractmethod
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
        """Generate a response from the provider."""
        raise NotImplementedError

    async def health(self) -> Dict[str, Any]:
        return {
            "provider": self.name,
            "status": "available",
        }