from pathlib import Path

from my_py_music_box.paths import scores_assets_dir
from my_py_music_box.score.model import Pin, Score
from my_py_music_box.score.store import load


def test_round_trip():
    score = Score(steps=16, bpm=60, pins=[Pin(0, 3), Pin(0, 3), Pin(4, 7)])
    data = score.to_dict()
    again = Score.from_dict(data)
    assert again.steps == 16
    assert again.bpm == 60
    assert [(p.step, p.tooth) for p in again.pins] == [(0, 3), (4, 7)]


def test_rejects_mismatched_note():
    try:
        Score.from_dict(
            {
                "format": "caixa-musica-v1",
                "steps": 8,
                "pins": [{"step": 0, "tooth": 3, "note": "G4"}],
            }
        )
    except ValueError:
        return
    raise AssertionError("should reject mismatched note")


def test_accepts_large_steps():
    score = Score.from_dict(
        {
            "format": "caixa-musica-v1",
            "steps": 545,
            "bpm": 100,
            "pins": [{"step": 2, "tooth": 7}],
        }
    )
    assert score.steps == 545


def test_rejects_bad_format():
    try:
        Score.from_dict({"format": "nope", "pins": []})
    except ValueError:
        return
    raise AssertionError("should reject format")


def test_builtin_assets_load():
    folder = scores_assets_dir()
    files = list(folder.glob("*.json"))
    assert files, f"no builtin scores in {folder}"
    for path in files:
        score = load(path)
        assert score.steps >= 8
        assert isinstance(path, Path)
