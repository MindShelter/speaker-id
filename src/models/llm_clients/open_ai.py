from dataclasses import dataclass, field

try:
    from openai import OpenAI
except ModuleNotFoundError:
    OpenAI = None

from openai.types.chat import (
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
)

from src.models.llm_clients.base import BaseLLMClient
from src.models.llm_clients.configs.open_ai import OpenAIConfig


@dataclass
class OpenAILLMClient(BaseLLMClient):
    config: OpenAIConfig
    client: OpenAI = field(init=False)

    def __post_init__(self):
        if OpenAI is None:
            raise RuntimeError("openai is required to use OpenAILLMClient.Install it or pick another client.")
        self.client = OpenAI(api_key=self.config.api_key)

    def chat_completion(
        self,
        system_prompt: str,
        user_input: str,
    ) -> str | None:
        try:
            resp = self.client.chat.completions.create(
                model=self.config.model,
                top_p=self.config.top_p,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
                messages=[
                    ChatCompletionSystemMessageParam(role="system", content=system_prompt),
                    ChatCompletionUserMessageParam(role="user", content=user_input),
                ],
            )
            return resp.choices[0].message.content
        except Exception:  # noqa: BLE001
            return None
