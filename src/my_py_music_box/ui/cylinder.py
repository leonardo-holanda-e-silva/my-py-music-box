from __future__ import annotations

from kivy.graphics import Color, Line, Rectangle
from kivy.properties import BooleanProperty, NumericProperty, ObjectProperty
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget

from my_py_music_box.score.model import Score
from my_py_music_box.ui.theme import GOLD_RGBA, MUTED_RGBA, NAVY_RGBA, PANEL_RGBA

CELL_W = 28
CELL_H = 22
GUTTER = 36
# Cap canvas instructions on mobile (scores can be 500+ steps).
_MAX_DRAW_STEPS = 48


class CylinderWidget(Widget):
    """21-tine pin grid. Editable when `editable` is True."""

    score = ObjectProperty(None, allownone=True)
    playhead = NumericProperty(-1)
    editable = BooleanProperty(False)
    view_start = NumericProperty(0)

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.bind(
            pos=self._redraw,
            size=self._redraw,
            score=self._redraw,
            playhead=self._redraw,
            view_start=self._redraw,
        )

    def set_score(self, score: Score | None) -> None:
        self.score = score
        steps = score.steps if score else 8
        self.size = (GUTTER + steps * CELL_W + 8, 21 * CELL_H + 8)
        self.size_hint = (None, None)
        self.view_start = 0
        self._redraw()

    def set_view_start(self, step: int) -> None:
        if self.score is None:
            return
        max_start = max(0, self.score.steps - _MAX_DRAW_STEPS)
        self.view_start = max(0, min(int(step), max_start))

    def _redraw(self, *_args) -> None:
        self.canvas.clear()
        if self.score is None:
            return
        steps = self.score.steps
        start = int(self.view_start)
        end = min(steps, start + _MAX_DRAW_STEPS)
        with self.canvas:
            Color(*PANEL_RGBA)
            Rectangle(pos=self.pos, size=self.size)
            ox, oy = self.pos
            for tooth in range(21):
                y = oy + (20 - tooth) * CELL_H + 4
                Color(*MUTED_RGBA)
                Line(
                    points=[ox + 4, y + CELL_H / 2, ox + GUTTER - 4, y + CELL_H / 2],
                    width=1,
                )
                for step in range(start, end):
                    x = ox + GUTTER + step * CELL_W
                    Color(*NAVY_RGBA)
                    Line(rectangle=(x, y, CELL_W - 2, CELL_H - 2), width=1)
            pin_set = {
                (p.step, p.tooth)
                for p in self.score.pins
                if start <= p.step < end
            }
            Color(*GOLD_RGBA)
            for step, tooth in pin_set:
                x = ox + GUTTER + step * CELL_W + 4
                y = oy + (20 - tooth) * CELL_H + 8
                Rectangle(pos=(x, y), size=(CELL_W - 10, CELL_H - 10))
            if 0 <= self.playhead < steps:
                Color(GOLD_RGBA[0], GOLD_RGBA[1], GOLD_RGBA[2], 0.35)
                x = ox + GUTTER + self.playhead * CELL_W
                Rectangle(pos=(x, oy + 4), size=(CELL_W - 2, 21 * CELL_H))

    def on_touch_down(self, touch):
        if not self.editable or self.score is None or not self.collide_point(*touch.pos):
            return super().on_touch_down(touch)
        ox, oy = self.pos
        local_x = touch.x - ox - GUTTER
        local_y = touch.y - oy - 4
        if local_x < 0 or local_y < 0:
            return True
        step = int(local_x // CELL_W)
        tooth = 20 - int(local_y // CELL_H)
        if 0 <= step < self.score.steps and 0 <= tooth < 21:
            self.score.toggle_pin(step, tooth)
            self._redraw()
            return True
        return True


class CylinderScroll(ScrollView):
    def __init__(self, **kwargs) -> None:
        kwargs.setdefault("do_scroll_y", False)
        kwargs.setdefault("bar_width", 6)
        super().__init__(**kwargs)
        self.cylinder = CylinderWidget()
        self.add_widget(self.cylinder)
        self.bind(scroll_x=self._on_scroll)

    def set_score(self, score: Score | None) -> None:
        self.cylinder.set_score(score)
        self._sync_view()

    def set_editable(self, editable: bool) -> None:
        self.cylinder.editable = editable

    def set_playhead(self, step: int | None) -> None:
        self.cylinder.playhead = -1 if step is None else int(step)
        if step is None or self.cylinder.score is None:
            return
        target = GUTTER + step * CELL_W
        max_x = max(self.cylinder.width - self.width, 1)
        self.scroll_x = min(1.0, max(0.0, target / max_x))
        self._sync_view()

    def _on_scroll(self, *_args) -> None:
        self._sync_view()

    def _sync_view(self) -> None:
        if self.cylinder.score is None:
            return
        max_x = max(self.cylinder.width - self.width, 1)
        x = self.scroll_x * max_x
        start = max(0, int((x - GUTTER) // CELL_W) - 2)
        self.cylinder.set_view_start(start)
