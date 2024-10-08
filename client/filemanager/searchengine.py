from abc import ABC, abstractmethod
from pathlib import Path


class BaseSearchEngine(ABC):
    @abstractmethod
    def _search_for_file(self, base_dir: Path, search_term: str) -> Path:
        pass

    def search_for_file(self, base_dir: Path, search_term: str) -> Path:
        rpath = self._sanitize_path(base_dir, Path(search_term))
        if rpath.is_file():
            return rpath

        return self._search_for_file(base_dir, search_term)

    def _sanitize_path(self, base_dir: Path, path: Path) -> Path:
        return base_dir.joinpath(path).resolve().relative_to(base_dir.resolve())
