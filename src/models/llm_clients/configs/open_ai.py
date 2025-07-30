import os
from typing import Any

from pydantic import BaseModel, Field, ValidationError


class OpenAIConfig(BaseModel):
    model: str = "gpt-4o"
    api_key: str = Field(...)
    top_p: float = 0.1
    temperature: float = 0.75
    max_tokens: int = 120

    @classmethod
    def from_env(cls, **overrides: Any) -> "OpenAIConfig":  # noqa: ANN401
        api_key = overrides.pop("api_key", None) or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("No OpenAI key found.  Set OPENAI_API_KEY or pass api_key=...")
        try:
            return cls(api_key=api_key, **overrides)
        except ValidationError as e:
            raise RuntimeError(f"Invalid OpenAI config: {e}") from e
