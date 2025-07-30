from dataclasses import dataclass
from pathlib import Path

from spacy import Language

from src.models.llm_clients.base import BaseLLMClient


@dataclass
class MainScriptsConfig:
    nlp: Language
    llm: BaseLLMClient
    llm_prompt: str
    text_path: Path | None = None
    text_meta_path: Path | None = None
    text_meta_output_path: Path = Path("outputs")
    enable_timing_logs: bool = False

    def __post_init__(self) -> None:
        if (self.text_path is None) == (self.text_meta_path is None):
            raise ValueError("Provide *either* `text_path` *or* `text_meta_file_path`, but not both.")
