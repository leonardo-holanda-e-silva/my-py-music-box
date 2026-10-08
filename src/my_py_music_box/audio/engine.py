from __future__ import annotations

import contextlib
import os
import tempfile
import wave
from pathlib import Path

import numpy as np

from my_py_music_box.audio.bank import SAMPLE_RATE
from my_py_music_box.audio.mixer import render, samples_per_step
from my_py_music_box.score.model import Score


def write_wav(path: str | Path, buffer: np.ndarray, sample_rate: int = SAMPLE_RATE) -> None:
    """Write mono float32 buffer as 16-bit PCM WAV."""
    clipped = np.clip(buffer, -1.0, 1.0)
    pcm = (clipped * 32767.0).astype(np.int16)
    with wave.open(str(path), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(pcm.tobytes())


class Engine:
    """Render a score to WAV and play it with Kivy SoundLoader."""

    def __init__(self) -> None:
        self._sound = None
        self._wav_path: Path | None = None
        self._volume = 0.7
        self._sps = 1
        self._steps = 0
        self._paused = False
        self._pause_pos = 0.0
        self._duration = 0.0

    @property
    def volume(self) -> float:
        return self._volume

    @volume.setter
    def volume(self, value: float) -> None:
        self._volume = float(np.clip(value, 0.0, 1.0))
        if self._sound is not None:
            self._sound.volume = self._volume

    def is_playing(self) -> bool:
        if self._sound is None or self._paused:
            return False
        return bool(getattr(self._sound, "state", "") == "play")

    def is_paused(self) -> bool:
        return self._paused and self._sound is not None

    def is_active(self) -> bool:
        return self.is_playing() or self.is_paused()

    def current_step(self) -> int | None:
        if not self.is_active() or self._sps <= 0:
            return None
        if self._paused:
            pos = self._pause_pos
        elif self._sound is None:
            return None
        else:
            try:
                pos = float(self._sound.get_pos())
            except Exception:
                return None
        sample = int(pos * SAMPLE_RATE)
        step = sample // self._sps
        if step >= self._steps:
            return self._steps - 1 if self._steps else 0
        return step

    def play(self, score: Score, device: str | None = None) -> str | None:
        del device  # system output only on mobile
        from kivy.core.audio import SoundLoader

        self.stop()
        buffer = render(score)
        self._sps = samples_per_step(score)
        self._steps = score.steps
        self._duration = len(buffer) / float(SAMPLE_RATE)
        self._paused = False
        self._pause_pos = 0.0

        fd, name = tempfile.mkstemp(suffix=".wav", prefix="mpmb_")
        os.close(fd)
        path = Path(name)
        write_wav(path, buffer)
        self._wav_path = path

        sound = SoundLoader.load(str(path))
        if sound is None:
            self.stop()
            raise RuntimeError("Could not load rendered audio (SoundLoader).")
        sound.volume = self._volume
        sound.play()
        self._sound = sound
        return None

    def pause(self) -> None:
        if self._sound is None or self._paused:
            return
        try:
            self._pause_pos = float(self._sound.get_pos())
        except Exception:
            self._pause_pos = 0.0
        if getattr(self._sound, "state", "") == "play":
            self._sound.stop()
        self._paused = True

    def resume(self) -> None:
        if self._sound is None or not self._paused:
            return
        self._paused = False
        # SoundLoader seek support varies; restart if seek unavailable.
        with contextlib.suppress(Exception):
            if hasattr(self._sound, "seek"):
                self._sound.seek(self._pause_pos)
        self._sound.play()

    def stop(self) -> None:
        sound = self._sound
        self._sound = None
        self._paused = False
        self._pause_pos = 0.0
        self._steps = 0
        self._duration = 0.0
        if sound is not None:
            with contextlib.suppress(Exception):
                sound.stop()
            with contextlib.suppress(Exception):
                sound.unload()
        if self._wav_path is not None:
            with contextlib.suppress(OSError):
                self._wav_path.unlink()
            self._wav_path = None

    def finished(self) -> bool:
        if self._paused or self._sound is None:
            return False
        state = getattr(self._sound, "state", "")
        return state == "stop" and self._duration > 0
