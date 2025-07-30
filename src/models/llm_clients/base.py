from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass
class BaseLLMClient(ABC):
    config: dict[str, Any]

    @abstractmethod
    def chat_completion(
        self,
        system_prompt: str,
        user_input: str,
    ) -> str | None:
        pass
