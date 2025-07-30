from dataclasses import dataclass, field, fields
from enum import Enum
from typing import Any, Union, get_args


class TextItemEnum(str, Enum):
    QUOTE = "quote"
    NARRATION = "narration"
    NEXT_LINE = "next-line"


@dataclass
class BaseTextItem:
    content: str
    type: TextItemEnum


@dataclass
class QuoteItem(BaseTextItem):
    cue: str | None = None
    speaker: str | None = None
    speaker_id: int | None = None
    already_reviewed: bool | None = None
    type: TextItemEnum = field(default=TextItemEnum.QUOTE, init=False)


@dataclass
class NarrationItem(BaseTextItem):
    switched_to_narration: bool | None = None
    type: TextItemEnum = field(default=TextItemEnum.NARRATION, init=False)


@dataclass
class NextLineItem(BaseTextItem):
    type: TextItemEnum = field(default=TextItemEnum.NEXT_LINE, init=False)
    content: TextItemEnum = field(default="\n", init=False)


TextItemType = Union[QuoteItem, NarrationItem, NextLineItem]

INIT_NAMES = {cls: {f.name for f in fields(cls) if f.init} for cls in get_args(TextItemType)}

CLASS_MAP = {
    TextItemEnum.QUOTE: QuoteItem,
    TextItemEnum.NARRATION: NarrationItem,
    TextItemEnum.NEXT_LINE: NextLineItem,
}


def filtered_kwargs(cls: TextItemType, data: dict) -> dict:
    return {k: v for k, v in data.items() if k in INIT_NAMES[cls]}


def text_item_factory(data: dict[str, Any]) -> TextItemType:
    item_type = data.get("type")
    cls = CLASS_MAP.get(item_type)
    if cls is None:
        raise ValueError(f"Unknown TextItemType: {item_type}")
    return cls(**filtered_kwargs(cls, data))


@dataclass
class Speaker:
    id: int
    name: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Speaker":
        return cls(
            id=data["id"],
            name=data["name"],
        )


@dataclass
class Chapter:
    id: int
    title: str
    items: list[TextItemType]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Chapter":
        return cls(
            id=data["id"],
            title=data["title"],
            items=[text_item_factory(item) for item in data["items"]],
        )


@dataclass
class TextMeta:
    title: str
    chapters: list[Chapter]
    speakers: list[Speaker]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TextMeta":
        return cls(
            title=data["title"],
            chapters=[Chapter.from_dict(chapter) for chapter in data["chapters"]],
            speakers=[Speaker.from_dict(speaker) for speaker in data["speakers"]],
        )


@dataclass
class RawChapter:
    title: str
    text: str


@dataclass
class LLMTextItem:
    id: int
    text: str
    label: str
