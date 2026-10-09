"""Shared cream window background helpers."""

from __future__ import annotations

from kivy.graphics import Color, Rectangle

from my_py_music_box.ui.theme import CREAM_RGBA


def bind_cream_background(widget) -> None:
    with widget.canvas.before:
        Color(*CREAM_RGBA)
        bg = Rectangle(pos=widget.pos, size=widget.size)

    def _sync(*_args) -> None:
        bg.pos = widget.pos
        bg.size = widget.size

    widget.bind(pos=_sync, size=_sync)
