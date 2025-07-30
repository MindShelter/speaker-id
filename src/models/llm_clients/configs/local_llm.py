from typing import Any

from pydantic import BaseModel, ValidationError


class LocalLLMConfig(BaseModel):
    model: str = "unsloth/llama-3-8b-Instruct-bnb-4bit"
    dtype: str = None
    max_seq_length: int = 3000
    load_in_4bit: bool = True
    top_p: float = 0.01
    temperature: float = 0.75
    max_tokens: float = 10

    @classmethod
    def from_env(cls, **overrides: Any) -> "LocalLLMConfig":  # noqa: ANN401
        try:
            return cls(**overrides)
        except ValidationError as e:
            raise RuntimeError(f"Invalid LocalLLM config: {e}") from e
