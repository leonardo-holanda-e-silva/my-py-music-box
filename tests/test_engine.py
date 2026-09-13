from pathlib import Path

import numpy as np

from my_py_music_box.audio.bank import SAMPLE_RATE, bank
from my_py_music_box.audio.mixer import render, samples_per_step
from my_py_music_box.paths import example_score_path
from my_py_music_box.score.model import Pin, Score
from my_py_music_box.score.store import load


def test_bank_has_21_tines():
    tines = bank()
    assert len(tines) == 21
    assert all(sample.dtype == np.float32 and sample.ndim == 1 and len(sample) > 1000 for sample in tines)


def test_render_covers_steps_plus_tail():
    score = Score(steps=8, bpm=60, steps_per_beat=4, pins=[Pin(0, 3)])
    buf = render(score)
    body = 8 * samples_per_step(score)
    assert buf.dtype == np.float32
    assert len(buf) >= body
    assert np.max(np.abs(buf[: SAMPLE_RATE // 10])) > 0.01


def test_how_deep_example_loads_and_sounds():
    path = example_score_path()
    assert path is not None
    score = load(path)
    assert score.steps == 64
    assert score.pins
    buf = render(score)
    assert np.max(np.abs(buf)) > 0.05
    assert Path(path).name == "How Deep Is Your Music Box.caixa.json"
