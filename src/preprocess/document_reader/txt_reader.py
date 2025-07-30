from dataclasses import dataclass
from pathlib import Path

from src.common.project_types import RawChapter
from src.preprocess.document_reader.base import TextReader


@dataclass
class TXTReader(TextReader):
    encoding: str = "utf-8"

    def read(self, path: Path) -> tuple[str, list[RawChapter]]:
        if not Path.is_file(path):
            raise FileNotFoundError(f"TXT file not found: {path}")
        with Path.open(path, encoding=self.encoding) as file:
            text = file.read()
        title = path.stem
        return title, [RawChapter(title=title, text=text)]
