from __future__ import annotations

import numpy as np

from my_py_music_box.score.model import NOTE_NAMES

SAMPLE_RATE = 44100

# MIDI: A4 = 69 = 440 Hz. Comb runs G4 (67) … F7 (101).
_MIDI = [67, 69, 71, 72, 74, 76, 77, 79, 81, 83, 84, 86, 88, 89, 91, 93, 95, 96, 98, 100, 101]
FREQUENCIES = [440.0 * (2.0 ** ((m - 69) / 12.0)) for m in _MIDI]


def tine_sample(frequency: float) -> np.ndarray:
    """Synthesize one plucked steel tine. Deterministic; no noise source."""
    duration = float(np.clip(1.05 + 1.15 * (392.0 / frequency) ** 0.45, 1.05, 2.5))
    n = int(SAMPLE_RATE * duration)
    t = np.arange(n, dtype=np.float64) / SAMPLE_RATE
    tau = 0.42 * (440.0 / frequency) ** 0.35
    env = np.exp(-t / tau)
    attack = np.minimum(t / 0.0018, 1.0)
    wave = (
        1.00 * np.sin(2 * np.pi * frequency * t)
        + 0.38 * np.sin(2 * np.pi * frequency * 2.012 * t) * np.exp(-t / (tau * 0.55))
        + 0.14 * np.sin(2 * np.pi * frequency * 3.04 * t) * np.exp(-t / (tau * 0.28))
        + 0.07 * np.sin(2 * np.pi * frequency * 4.18 * t) * np.exp(-t / (tau * 0.16))
        + 0.16 * np.sin(2 * np.pi * frequency * 8.0 * t) * np.exp(-t / 0.006)
    )
    wave *= env * attack
    peak = np.max(np.abs(wave))
    if peak > 0:
        wave /= peak
    return (wave * 0.72).astype(np.float32)


def build_bank() -> list[np.ndarray]:
    if len(NOTE_NAMES) != 21:
        raise RuntimeError("comb must have 21 named tines")
    return [tine_sample(freq) for freq in FREQUENCIES]


_BANK: list[np.ndarray] | None = None


def bank() -> list[np.ndarray]:
    global _BANK
    if _BANK is None:
        _BANK = build_bank()
    return _BANK
