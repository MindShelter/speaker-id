import time
from collections.abc import Generator
from contextlib import contextmanager
from typing import Any

from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
)

from src.metrics.metric_types import IncorrectPrediction, Metrics


def compute_metrics(
    true_labels: list[str],
    pred_labels: list[str],
) -> Metrics:
    return Metrics(
        accuracy=accuracy_score(true_labels, pred_labels),
        precision=precision_score(true_labels, pred_labels, average="weighted", zero_division=0),
        recall=recall_score(true_labels, pred_labels, average="weighted", zero_division=0),
        f1=f1_score(true_labels, pred_labels, average="weighted", zero_division=0),
    )


def display_metrics(
    metrics: Metrics,
    incorrect_predictions: list[IncorrectPrediction],
) -> None:
    print("Evaluation Metrics:")
    print(f"  Accuracy:  {metrics.accuracy:.4f}")
    print(f"  Precision: {metrics.precision:.4f}")
    print(f"  Recall:    {metrics.recall:.4f}")
    print(f"  F1-Score:  {metrics.f1:.4f}")

    if incorrect_predictions:
        print("\nIncorrect Predictions:")
        for ip in incorrect_predictions:
            print(f"  True: '{ip.true_label}'  Pred: '{ip.predicted_label}'")
            print(f'  Text: "{ip.text}"')
            print("  " + "-" * 30)
    else:
        print("\nAll predictions are correct!")


@contextmanager
def elapsed_time(label: str, *, enabled: bool) -> Generator[None, Any, None]:
    if enabled:
        start = time.perf_counter()
        yield
        elapsed = time.perf_counter() - start
        print(f"{label} processed in {elapsed:.2f} seconds")
    else:
        yield
