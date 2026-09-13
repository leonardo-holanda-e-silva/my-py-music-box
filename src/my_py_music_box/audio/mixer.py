from __future__ import annotations

import numpy as np

from my_py_music_box.audio.bank import SAMPLE_RATE, bank
from my_py_music_box.score.model import Score


def samples_per_step(score: Score) -> int:
    steps_per_beat = max(int(score.steps_per_beat), 1)
    seconds = (60.0 / float(score.bpm)) / steps_per_beat
    return max(round(SAMPLE_RATE * seconds), 1)


def render(score: Score) -> np.ndarray:
    """Mix pins into a float32 mono buffer at unity gain (volume applied at output)."""
    score.validate()
    sps = samples_per_step(score)
    tines = bank()
    tail = max(len(sample) for sample in tines)
    n = score.steps * sps + tail
    mix = np.zeros(n, dtype=np.float32)
    for pin in score.pins:
        start = pin.step * sps
        sample = tines[pin.tooth]
        end = min(start + len(sample), n)
        mix[start:end] += sample[: end - start]
    peak = float(np.max(np.abs(mix))) if n else 0.0
    if peak > 1.0:
        mix /= peak
    return mix
