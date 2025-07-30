from pathlib import Path

from src.common.project_types import RawChapter
from src.preprocess.document_reader.base import TextReader
from src.preprocess.document_reader.epub_reader import EPUBReader
from src.preprocess.document_reader.txt_reader import TXTReader

READERS: dict[str, TextReader] = {
    ".epub": EPUBReader(),
    ".txt": TXTReader(),
}


def get_reader_for(path: Path) -> TextReader:
    ext = path.suffix.lower()
    reader = READERS.get(ext)
    if reader is None:
        raise ValueError(f"No reader registered for extension '{ext}'")
    return reader

def read_document(path: Path) -> tuple[str, list[RawChapter]]:
    reader = get_reader_for(path)
    return reader.read(path)
