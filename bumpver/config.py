"""Configuration Methods and Objects."""

from pathlib import Path

from igittigitt import IgnoreParser


class Config:
    """Program Configuration."""

    def __init__(self) -> None:
        self._working_directory = Path.cwd()

        self._path_filter = IgnoreParser()
        self._path_filter.parse_rule_files(base_dir=self.cwd)
        self._path_filter.add_rule(".git/", base_path=self.cwd)

    def ignore_path(self, path: Path) -> bool:
        """Is path matched by the configured ignore rules."""
        return self._path_filter.match(path)

    @property
    def cwd(self) -> Path:
        """The project working directory."""
        return self._working_directory

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__qualname__}("
            f"{', '.join(f'{k!s}={v!r}' for k,v in self.__dict__.items())})"
        )
