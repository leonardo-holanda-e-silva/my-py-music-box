from __future__ import annotations

import contextlib

import numpy as np
import sounddevice as sd

from my_py_music_box.audio.bank import SAMPLE_RATE
from my_py_music_box.audio.mixer import render, samples_per_step
from my_py_music_box.score.model import Score


class Engine:
    """Non-blocking playback of a rendered score via sounddevice."""

    def __init__(self) -> None:
        self._stream: sd.OutputStream | None = None
        self._buffer = np.zeros(0, dtype=np.float32)
        self._pos = 0
        self._paused = False
        self._volume = 0.7
        self._sps = 1
        self._steps = 0

    @property
    def volume(self) -> float:
        return self._volume

    @volume.setter
    def volume(self, value: float) -> None:
        self._volume = float(np.clip(value, 0.0, 1.0))

    def is_playing(self) -> bool:
        return self._stream is not None and self._stream.active and not self._paused

    def is_paused(self) -> bool:
        return self._paused and self._stream is not None

    def is_active(self) -> bool:
        return self.is_playing() or self.is_paused()

    def current_step(self) -> int | None:
        if not self.is_active() or self._sps <= 0:
            return None
        step = self._pos // self._sps
        if step >= self._steps:
            return self._steps - 1 if self._steps else 0
        return step

    def play(self, score: Score) -> None:
        self.stop()
        self._buffer = render(score)
        self._sps = samples_per_step(score)
        self._steps = score.steps
        self._pos = 0
        self._paused = False
        try:
            self._stream = sd.OutputStream(
                samplerate=SAMPLE_RATE,
                channels=1,
                dtype="float32",
                callback=self._callback,
            )
            self._stream.start()
        except sd.PortAudioError as exc:
            self.stop()
            raise RuntimeError(str(exc)) from exc

    def pause(self) -> None:
        if self._stream is None or self._paused:
            return
        if self._stream.active:
            self._stream.stop()
        self._paused = True

    def resume(self) -> None:
        if self._stream is None or not self._paused:
            return
        self._paused = False
        if not self._stream.active:
            self._stream.start()

    def stop(self) -> None:
        stream = self._stream
        self._stream = None
        self._paused = False
        self._pos = 0
        self._buffer = np.zeros(0, dtype=np.float32)
        if stream is not None:
            with contextlib.suppress(OSError, sd.PortAudioError):
                stream.abort()
            with contextlib.suppress(OSError, sd.PortAudioError):
                stream.stop()
            with contextlib.suppress(OSError, sd.PortAudioError):
                stream.close()

    def finished(self) -> bool:
        if self._paused or self._buffer.size == 0:
            return False
        if self._pos >= len(self._buffer):
            return True
        return bool(self._stream is not None and not self._stream.active and self._pos > 0)

    def _callback(self, outdata, frames, _time, _status) -> None:
        pos = self._pos
        buf = self._buffer
        remaining = len(buf) - pos
        if remaining <= 0:
            outdata.fill(0)
            raise sd.CallbackStop
        n = min(frames, remaining)
        outdata[:n, 0] = buf[pos : pos + n] * self._volume
        if n < frames:
            outdata[n:].fill(0)
            self._pos = pos + n
            raise sd.CallbackStop
        self._pos = pos + n
