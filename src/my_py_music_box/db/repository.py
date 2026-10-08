from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from my_py_music_box.paths import scores_assets_dir
from my_py_music_box.score.model import MAX_STEPS, MIN_BPM, MIN_STEPS, Pin, Score
from my_py_music_box.score.store import load as load_json_score

_SCHEMA = """
CREATE TABLE IF NOT EXISTS scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    steps INTEGER NOT NULL,
    bpm INTEGER NOT NULL,
    steps_per_beat INTEGER NOT NULL,
    pins_json TEXT NOT NULL,
    source TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS prefs (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
"""


@dataclass
class ScoreRecord:
    id: int
    title: str
    score: Score
    source: str
    created_at: str
    updated_at: str


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _pins_to_json(score: Score) -> str:
    return json.dumps(
        [{"step": p.step, "tooth": p.tooth, "note": p.note} for p in score.pins]
    )


def _pins_from_json(raw: str) -> list[Pin]:
    items = json.loads(raw)
    return [Pin(int(item["step"]), int(item["tooth"])) for item in items]


def _row_to_record(row: sqlite3.Row) -> ScoreRecord:
    score = Score(
        steps=int(row["steps"]),
        bpm=int(row["bpm"]),
        steps_per_beat=int(row["steps_per_beat"]),
        pins=_pins_from_json(row["pins_json"]),
    )
    score.validate()
    return ScoreRecord(
        id=int(row["id"]),
        title=str(row["title"]),
        score=score,
        source=str(row["source"]),
        created_at=str(row["created_at"]),
        updated_at=str(row["updated_at"]),
    )


class Repository:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(str(self.path))
        self._conn.row_factory = sqlite3.Row
        self._conn.executescript(_SCHEMA)
        self._conn.commit()

    def close(self) -> None:
        self._conn.close()

    def seed_builtins(self) -> None:
        existing = self._conn.execute(
            "SELECT COUNT(*) AS n FROM scores WHERE source = 'builtin'"
        ).fetchone()["n"]
        if existing:
            return
        folder = scores_assets_dir()
        if not folder.is_dir():
            return
        paths = sorted({*folder.glob("*.json"), *folder.glob("*.caixa.json")})
        for path in paths:
            try:
                score = load_json_score(path)
            except (OSError, ValueError, json.JSONDecodeError, KeyError):
                continue
            title = path.stem.replace("-", " ").replace("_", " ").title()
            if path.name.startswith("example"):
                title = "Example"
            elif "how-deep" in path.name.lower():
                title = "How Deep Is Your Love"
            self.insert_score(title, score, source="builtin")

    def list_scores(self) -> list[ScoreRecord]:
        rows = self._conn.execute(
            "SELECT * FROM scores ORDER BY source = 'builtin' DESC, title COLLATE NOCASE"
        ).fetchall()
        return [_row_to_record(row) for row in rows]

    def get_score(self, score_id: int) -> ScoreRecord | None:
        row = self._conn.execute(
            "SELECT * FROM scores WHERE id = ?", (score_id,)
        ).fetchone()
        return _row_to_record(row) if row else None

    def insert_score(self, title: str, score: Score, source: str = "user") -> int:
        score.validate()
        stamp = _now()
        cur = self._conn.execute(
            """
            INSERT INTO scores (title, steps, bpm, steps_per_beat, pins_json, source, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                title,
                score.steps,
                score.bpm,
                score.steps_per_beat,
                _pins_to_json(score),
                source,
                stamp,
                stamp,
            ),
        )
        self._conn.commit()
        return int(cur.lastrowid)

    def update_score(self, score_id: int, title: str, score: Score) -> None:
        score.validate()
        self._conn.execute(
            """
            UPDATE scores
            SET title = ?, steps = ?, bpm = ?, steps_per_beat = ?, pins_json = ?, updated_at = ?
            WHERE id = ?
            """,
            (
                title,
                score.steps,
                score.bpm,
                score.steps_per_beat,
                _pins_to_json(score),
                _now(),
                score_id,
            ),
        )
        self._conn.commit()

    def delete_score(self, score_id: int) -> bool:
        row = self.get_score(score_id)
        if row is None or row.source == "builtin":
            return False
        self._conn.execute("DELETE FROM scores WHERE id = ?", (score_id,))
        self._conn.commit()
        return True

    def import_json(self, path: str | Path, title: str | None = None) -> int:
        score = load_json_score(path)
        name = title or Path(path).stem
        return self.insert_score(name, score, source="imported")

    def export_json(self, score_id: int, path: str | Path) -> None:
        from my_py_music_box.score.store import save as save_json_score

        record = self.get_score(score_id)
        if record is None:
            raise ValueError("score not found")
        save_json_score(record.score, path)

    def get_pref(self, key: str, default: str | None = None) -> str | None:
        row = self._conn.execute(
            "SELECT value FROM prefs WHERE key = ?", (key,)
        ).fetchone()
        return str(row["value"]) if row else default

    def set_pref(self, key: str, value: str) -> None:
        self._conn.execute(
            """
            INSERT INTO prefs (key, value) VALUES (?, ?)
            ON CONFLICT(key) DO UPDATE SET value = excluded.value
            """,
            (key, value),
        )
        self._conn.commit()

    def get_volume(self) -> int:
        raw = self.get_pref("volume", "70")
        try:
            return max(0, min(100, int(raw or 70)))
        except ValueError:
            return 70

    def set_volume(self, volume: int) -> None:
        self.set_pref("volume", str(max(0, min(100, int(volume)))))

    def get_default_bpm(self) -> int:
        raw = self.get_pref("default_bpm", "72")
        try:
            return max(MIN_BPM, min(180, int(raw or 72)))
        except ValueError:
            return 72

    def set_default_bpm(self, bpm: int) -> None:
        self.set_pref("default_bpm", str(max(MIN_BPM, min(180, int(bpm)))))

    def get_default_steps(self) -> int:
        raw = self.get_pref("default_steps", "32")
        try:
            return max(MIN_STEPS, min(MAX_STEPS, int(raw or 32)))
        except ValueError:
            return 32

    def set_default_steps(self, steps: int) -> None:
        self.set_pref("default_steps", str(max(MIN_STEPS, min(MAX_STEPS, int(steps)))))

    def get_last_score_id(self) -> int | None:
        raw = self.get_pref("last_score_id")
        if not raw:
            return None
        try:
            return int(raw)
        except ValueError:
            return None

    def set_last_score_id(self, score_id: int | None) -> None:
        if score_id is None:
            self._conn.execute("DELETE FROM prefs WHERE key = 'last_score_id'")
            self._conn.commit()
            return
        self.set_pref("last_score_id", str(score_id))
