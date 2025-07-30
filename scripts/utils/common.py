import copy
from dataclasses import asdict, replace
from pathlib import Path
from typing import Any

from scripts.types.config_types import MainScriptsConfig
from scripts.types.statistic_types import Statistics
from src.common.project_types import (
    QuoteItem,
    Speaker,
    TextItemType,
)
from src.common.utils import dict_factory_no_none_or_empty, save_to_file
from src.metrics.metric_types import IncorrectPrediction, Metrics


def found_speaker(speaker_name: str, speakers: dict[int, Speaker]) -> Speaker | None:
    for speaker in speakers.values():
        if speaker.name == speaker_name:
            return speaker
    return None


def get_items_without_speaker(items: list[TextItemType]) -> list[TextItemType]:
    modified_items = copy.deepcopy(items)
    for item in modified_items:
        if isinstance(item, QuoteItem):
            item.speaker = None
            item.speaker_id = None

    return modified_items


def is_speaker_presents_in_text(speaker: str, text: str) -> bool:
    return speaker.lower() in text.lower()


def save_object_to_file(
    output_dir: Path,
    file_name: Path,
    obj: Any,  # noqa: ANN401
) -> None:
    file_path = output_dir / file_name
    file_path.parent.mkdir(parents=True, exist_ok=True)
    save_to_file(file_path, asdict(obj, dict_factory=dict_factory_no_none_or_empty))


def generate_statistics(
    metrics: Metrics,
    input_config: MainScriptsConfig,
    incorrect_predictions: list[IncorrectPrediction],
) -> Statistics:
    llm_config = input_config.llm.config
    if hasattr(llm_config, "api_key"):
        llm_config = replace(llm_config, api_key="skipped")

    return Statistics(
        metrics=metrics,
        llm_config=llm_config,
        nlp_name=input_config.nlp.meta["name"],
        incorrect_predictions=incorrect_predictions,
    )
