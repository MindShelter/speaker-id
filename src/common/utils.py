import json
import re
from collections.abc import Iterable
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from spacy.tokens import Doc, SpanGroup
from textacy import preprocessing

from src.preprocess.quote_finder.constants import QUOTE_TRANSLATION_TABLE


def read_file(file_path: Path) -> str:
    return file_path.open(encoding="utf-8").read()


def read_json_file(file_path: Path) -> Any:  # noqa: ANN401
    with file_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_to_file(file_path: Path, content: object) -> None:
    with file_path.open("w", encoding="utf-8") as f:
        json.dump(content, f, indent=4)


def quotation_marks_normalization(text: str) -> str:
    return re.sub(
        r"''|' '",
        '"',
        text.translate(QUOTE_TRANSLATION_TABLE),
    )


preproc = preprocessing.make_pipeline(
    preprocessing.normalize.bullet_points,
    preprocessing.normalize.hyphenated_words,
    preprocessing.normalize.unicode,
    preprocessing.normalize.whitespace,
)


def prep_document_for_quote_detection(text: str) -> str:
    return preproc(text)


def clone_cluster(cluster: SpanGroup, destination_doc: Doc) -> SpanGroup:
    return SpanGroup(
        doc=destination_doc,
        spans=[destination_doc[span.start : span.end] for span in cluster],
    )


def normalize_book_title(title: str) -> str:
    sanitized = re.sub(r'[<>:"/\\|?*]', "_", title)
    return sanitized.replace(" ", "_")


def get_current_date() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M")


def process_book_title(title: str) -> str:
    return f"{normalize_book_title(title)}({get_current_date()})"


def dict_factory_no_none_or_empty(items: Iterable[tuple[str, Any]]) -> dict[str, Any]:
    return {k: v for k, v in items if v is not None and v != ""}
