from __future__ import annotations

import json
from pathlib import Path

from my_py_music_box.score.model import Score


def load(path: str | Path) -> Score:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return Score.from_dict(data)


def save(score: Score, path: str | Path) -> None:
    Path(path).write_text(
        json.dumps(score.to_dict(), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
