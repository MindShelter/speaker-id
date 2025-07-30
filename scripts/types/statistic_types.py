from dataclasses import dataclass
from typing import Any

from src.metrics.metric_types import IncorrectPrediction, Metrics


@dataclass
class Statistics:
    metrics: Metrics
    nlp_name: str
    llm_config: dict[str, Any]
    incorrect_predictions: list[IncorrectPrediction]
