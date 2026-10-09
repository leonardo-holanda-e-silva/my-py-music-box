from __future__ import annotations

from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.slider import Slider

from my_py_music_box.ui.bg import bind_cream_background
from my_py_music_box.ui.cylinder import CylinderScroll
from my_py_music_box.ui.theme import CREAM, GOLD, MUTED, NAVY


def _rgba(hex_color: str) -> tuple[float, float, float, float]:
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return r / 255, g / 255, b / 255, 1


class PlayScreen(Screen):
    def __init__(self, app_ref, **kwargs) -> None:
        super().__init__(**kwargs)
        self.app_ref = app_ref
        self._tick = None

        root = BoxLayout(orientation="vertical", padding=12, spacing=8)
        self.title_lbl = Label(
            text="Play",
            color=_rgba(NAVY),
            font_size="20sp",
            size_hint_y=None,
            height=36,
        )
        root.add_widget(self.title_lbl)
        self.status = Label(text="", color=_rgba(MUTED), size_hint_y=None, height=24)
        root.add_widget(self.status)

        self.cylinder = CylinderScroll(size_hint=(1, 1))
        self.cylinder.set_editable(False)
        root.add_widget(self.cylinder)

        vol_row = BoxLayout(size_hint_y=None, height=40, spacing=8)
        vol_row.add_widget(Label(text="Vol", color=_rgba(NAVY), size_hint_x=0.2))
        self.volume = Slider(min=0, max=100, value=70)
        self.volume.bind(value=self._on_volume)
        vol_row.add_widget(self.volume)
        root.add_widget(vol_row)

        controls = BoxLayout(size_hint_y=None, height=48, spacing=8)
        for text, handler in (
            ("Play", self._play),
            ("Pause", self._pause),
            ("Stop", self._stop),
        ):
            btn = Button(text=text, background_color=_rgba(GOLD), color=_rgba(NAVY))
            btn.bind(on_release=lambda _b, h=handler: h())
            controls.add_widget(btn)
        root.add_widget(controls)

        nav = BoxLayout(size_hint_y=None, height=44, spacing=8)
        for text, screen in (("Library", "library"), ("Composer", "composer"), ("Settings", "settings")):
            btn = Button(text=text, background_color=_rgba(NAVY), color=_rgba(CREAM))
            btn.bind(on_release=lambda _b, s=screen: self.app_ref.show_screen(s))
            nav.add_widget(btn)
        root.add_widget(nav)

        self.add_widget(root)
        bind_cream_background(self)

    def on_enter(self, *_args) -> None:
        self.volume.value = self.app_ref.repo.get_volume()
        self._sync_score()
        if self._tick is None:
            self._tick = Clock.schedule_interval(self._on_tick, 1 / 20)

    def on_leave(self, *_args) -> None:
        self.app_ref.engine.stop()
        if self._tick is not None:
            self._tick.cancel()
            self._tick = None

    def _sync_score(self) -> None:
        record = self.app_ref.current_record
        if record is None:
            self.title_lbl.text = "Play — no score"
            self.cylinder.set_score(None)
            return
        self.title_lbl.text = f"Play — {record.title}"
        self.cylinder.set_score(record.score.copy())

    def _on_volume(self, _slider, value) -> None:
        vol = int(value)
        self.app_ref.repo.set_volume(vol)
        self.app_ref.engine.volume = vol / 100.0

    def _play(self) -> None:
        record = self.app_ref.current_record
        if record is None:
            self.status.text = "Open a score from Library."
            return
        if self.app_ref.engine.is_paused():
            self.app_ref.engine.resume()
            self.status.text = "Playing"
            return
        try:
            self.app_ref.engine.volume = self.volume.value / 100.0
            self.app_ref.engine.play(record.score)
            self.status.text = "Playing"
        except Exception as exc:  # noqa: BLE001 — show to user in POC
            self.status.text = str(exc)

    def _pause(self) -> None:
        self.app_ref.engine.pause()
        self.status.text = "Paused"

    def _stop(self) -> None:
        self.app_ref.engine.stop()
        self.cylinder.set_playhead(None)
        self.status.text = "Stopped"

    def _on_tick(self, _dt) -> None:
        engine = self.app_ref.engine
        if engine.finished():
            engine.stop()
            self.cylinder.set_playhead(None)
            self.status.text = "Finished"
            return
        step = engine.current_step()
        self.cylinder.set_playhead(step)
