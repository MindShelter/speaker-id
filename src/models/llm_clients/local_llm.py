import re
from dataclasses import dataclass, field
from typing import Any

from src.models.llm_clients.base import BaseLLMClient
from src.models.llm_clients.configs.local_llm import LocalLLMConfig


def _import_unsloth():  # noqa: ANN202
    try:
        from unsloth import FastLanguageModel
    except ModuleNotFoundError as exc:
        raise RuntimeError("unsloth is required to use LocalLLMClient.Install it or choose another client.") from exc
    return FastLanguageModel


def _extract_response_regex_single(model_output: str) -> str | None:
    pattern = r"Output:\s*([^\n\r]+)"
    matches = re.findall(pattern, model_output)
    if matches:
        return matches[-1].strip().rstrip("'")
    return None


@dataclass
class LocalLLMClient(BaseLLMClient):
    config: LocalLLMConfig
    llm_model: Any = field(init=False, repr=False)
    tokenizer: Any = field(init=False, repr=False)

    def __post_init__(self):
        FastLanguageModel = _import_unsloth()  # noqa: N806
        model, tokenizer = _import_unsloth().from_pretrained(
            model_name=self.config.model,
            max_seq_length=self.config.max_seq_length,
            dtype=self.config.dtype,
            load_in_4bit=self.config.load_in_4bit,
        )
        self.llm_model = model
        self.tokenizer = tokenizer
        FastLanguageModel.for_inference(self.llm_model)

    def chat_completion(self, system_prompt: str, user_input: str) -> str | None:
        prompt = system_prompt.format(user_input)
        inputs = self.tokenizer([prompt], return_tensors="pt").to("cuda")
        outputs = self.llm_model.generate(
            **inputs,
            max_new_tokens=self.config.max_tokens,
            do_sample=True,
            temperature=self.config.temperature,
            top_p=self.config.top_p,
        )
        decoded = self.tokenizer.batch_decode(
            outputs,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=True,
        )[0]
        return _extract_response_regex_single(decoded)
