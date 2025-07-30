from dataclasses import dataclass

import requests

from src.models.llm_clients.base import BaseLLMClient
from src.models.llm_clients.configs.llama import LlamaConfig


@dataclass
class LlamaLLMClient(BaseLLMClient):
    config: LlamaConfig

    def chat_completion(
        self,
        system_prompt: str,
        user_input: str,
    ) -> str | None:
        payload = {
            "model": self.config.model,
            "top_p": self.config.top_p,
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input},
            ],
        }
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config.api_key}",
        }

        try:
            response = requests.post(self.config.url, headers=headers, json=payload, timeout=10)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception:  # noqa: BLE001
            return None
