from dataclasses import replace
from typing import TypedDict

from spacy.tokens import Doc, Span

from src.common.project_types import (
    NarrationItem,
    NextLineItem,
    QuoteItem,
    TextItemType,
)


def split_to_next_line(item: TextItemType) -> list[TextItemType]:
    parts = item.content.split("\n")
    result = []

    for index, part in enumerate(parts):
        content = part.lstrip()

        if content:
            result.append(replace(item, content=content))

        if index < len(parts) - 1:
            result.append(NextLineItem())

    return result


class JoinResult(TypedDict):
    speakers: list[str]
    items: list[TextItemType]


def join_quotes_with_narrative(
    quotes: list[Span],
    doc: Doc,
) -> JoinResult:
    current_pos = 0
    items: list[TextItemType] = []

    for quote in quotes:
        quote_start = quote.start
        quote_end = quote.end

        if current_pos < quote_start:
            items.extend(
                split_to_next_line(NarrationItem(doc[current_pos:quote_start].text))
            )

        quote_dict = QuoteItem(content=doc[quote_start:quote_end].text)
        items.extend(split_to_next_line(quote_dict))

        current_pos = quote_end

    if current_pos < len(doc.text):
        items.extend(split_to_next_line(NarrationItem(doc[current_pos:].text)))

    speakers = list(
        {item.speaker for item in items if isinstance(item, QuoteItem) and item.speaker}
    )

    return JoinResult(
        items=items,
        speakers=speakers,
    )
