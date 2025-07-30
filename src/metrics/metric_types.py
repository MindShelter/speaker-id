from dataclasses import dataclass


@dataclass
class IncorrectPrediction:
    text: str
    true_label: str
    predicted_label: str
    text_for_llm: str


@dataclass
class Metrics:
    accuracy: float
    precision: float
    recall: float
    f1: float
