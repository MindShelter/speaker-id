import os
from typing import Any

from pydantic import BaseModel, Field, ValidationError


class LlamaConfig(BaseModel):
    model: str = "accounts/fireworks/models/llama-v3p1-405b-instruct"
    url: str = "https://api.fireworks.ai/inference/v1/chat/completions"
    api_key: str = Field(...)
    top_p: float = 0.1
    temperature: float = 0.75
    max_tokens: int = 120

    @classmethod
    def from_env(cls, **overrides: Any) -> "LlamaConfig":  # noqa: ANN401
        api_key = overrides.pop("api_key", None) or os.getenv("LLAMA_API_KEY")
        if not api_key:
            raise RuntimeError("No Llama key found.  Set LLAMA_API_KEY or pass api_key=...")
        try:
            return cls(api_key=api_key, **overrides)
        except ValidationError as e:
            raise RuntimeError(f"Invalid LlamaConfig config: {e}") from e
