from __future__ import annotations

from pathlib import Path

EXAMPLE_SCORE_NAME = "How Deep Is Your Music Box.caixa.json"


def examples_dirs() -> list[Path]:
    here = Path(__file__).resolve()
    pkg = here.parent
    return [
        pkg.parent / "examples",
        here.parents[2] / "examples",
        Path.cwd() / "examples",
    ]


def examples_dir() -> Path | None:
    for path in examples_dirs():
        if path.is_dir():
            return path
    return None


def example_score_path() -> Path | None:
    for folder in examples_dirs():
        candidate = folder / EXAMPLE_SCORE_NAME
        if candidate.is_file():
            return candidate
    return None
