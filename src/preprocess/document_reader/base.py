from abc import ABC, abstractmethod
from pathlib import Path

from src.common.project_types import RawChapter


class TextReader(ABC):
    @abstractmethod
    def read(self, path: Path) -> tuple[str, list[RawChapter]]: ...
