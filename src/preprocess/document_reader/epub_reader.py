from dataclasses import dataclass
from pathlib import Path
from typing import Any

from bs4 import BeautifulSoup
from ebooklib import ITEM_DOCUMENT, epub
from ebooklib.epub import EpubBook

from src.common.project_types import RawChapter
from src.preprocess.document_reader.base import TextReader


def _extract_text(chapter: Any, chapter_title: str) -> str:  # noqa: ANN401
    soup = BeautifulSoup(chapter.get_body_content(), "html.parser")
    paras = [p.get_text().strip() for p in soup.find_all("p")]
    paras = [p for p in paras if p]
    if paras and paras[0].lower() == chapter_title.strip().lower():
        paras = paras[1:]
    return "\n".join(paras)


def _normalize_href(href: str) -> str:
    return href.split("#")[0].lstrip("/")


def _build_toc_map(toc: Any, toc_map: dict[str, str]) -> None:  # noqa: ANN401
    for entry in toc:
        if isinstance(entry, epub.Link):
            href = _normalize_href(entry.href)
            toc_map[href] = entry.title
        elif isinstance(entry, tuple):
            link, children = entry
            href = _normalize_href(link.href)
            toc_map[href] = link.title
            _build_toc_map(children, toc_map)


def _get_chapters(book: EpubBook) -> list[RawChapter]:
    toc_map: dict[str, str] = {}
    _build_toc_map(book.toc, toc_map)

    chapters: list[RawChapter] = []
    for idref, _ in book.spine:
        item = book.get_item_with_id(idref)
        if not item or item.get_type() != ITEM_DOCUMENT:
            continue
        href = _normalize_href(item.get_name())
        title = toc_map.get(href)
        if title:
            text = _extract_text(item, title)
            chapters.append(RawChapter(title=title, text=text))
    return chapters


@dataclass
class EPUBReader(TextReader):
    parser: str = "html.parser"

    def read(self, path: Path) -> tuple[str, list[RawChapter]]:
        if not Path.is_file(path):
            raise FileNotFoundError(f"EPUB not found: {path}")
        book = epub.read_epub(path)
        title = getattr(book, "title", path.name)
        chapters = _get_chapters(book)
        return title, chapters
