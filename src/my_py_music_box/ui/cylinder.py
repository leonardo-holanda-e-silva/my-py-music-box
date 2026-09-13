from __future__ import annotations

from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QColor, QPainter, QPen
from PyQt5.QtWidgets import QWidget

from my_py_music_box.score.model import NOTE_NAMES, Score
from my_py_music_box.ui.theme import ATELIER, BRASS, GOLD, INK, IVORY, PLUM, SCORE

CELL_W = 18
CELL_H = 16
GUTTER = 40


class CylinderView(QWidget):
    """Read-only 21 × N pin grid with an optional playhead."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._score: Score | None = None
        self._playhead: int | None = None
        self.setMinimumHeight(21 * CELL_H + 8)

    def set_score(self, score: Score | None) -> None:
        self._score = score
        self._playhead = None
        steps = score.steps if score else 32
        self.setMinimumWidth(GUTTER + steps * CELL_W + 8)
        self.update()

    def set_playhead(self, step: int | None) -> None:
        self._playhead = step
        self.update()

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(ATELIER))
        score = self._score
        steps = score.steps if score else 32
        pins = {(p.step, p.tooth) for p in score.pins} if score else set()

        for tooth in range(21):
            row = 20 - tooth
            y = 4 + row * CELL_H
            painter.setPen(QColor(SCORE))
            painter.drawText(QRectF(0, y, GUTTER - 4, CELL_H), Qt.AlignRight | Qt.AlignVCenter, NOTE_NAMES[tooth])
            for step in range(steps):
                x = GUTTER + step * CELL_W
                even = (step // 4) % 2 == 0
                painter.fillRect(x, y, CELL_W - 1, CELL_H - 1, QColor(INK if even else PLUM))
                if (step, tooth) in pins:
                    painter.setPen(Qt.NoPen)
                    painter.setBrush(QColor(BRASS))
                    painter.drawEllipse(QRectF(x + 3, y + 2, CELL_W - 8, CELL_H - 6))

        if self._playhead is not None and 0 <= self._playhead < steps:
            x = GUTTER + self._playhead * CELL_W
            overlay = QColor(GOLD)
            overlay.setAlpha(72)
            painter.fillRect(x, 4, CELL_W, 21 * CELL_H, overlay)
            painter.setPen(QPen(QColor(GOLD), 2))
            painter.drawLine(x, 4, x, 4 + 21 * CELL_H)

        painter.setPen(QColor(BRASS))
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(GUTTER, 4, steps * CELL_W, 21 * CELL_H)
        painter.setPen(QColor(IVORY))
