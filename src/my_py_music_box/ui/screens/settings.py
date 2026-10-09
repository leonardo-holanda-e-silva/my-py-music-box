from __future__ import annotations

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.slider import Slider
from kivy.uix.textinput import TextInput

from my_py_music_box.paths import logo_path
from my_py_music_box.score.model import MAX_STEPS, MIN_BPM, MIN_STEPS
from my_py_music_box.ui.bg import bind_cream_background
from my_py_music_box.ui.theme import CREAM, GOLD, MUTED, NAVY


def _rgba(hex_color: str) -> tuple[float, float, float, float]:
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return r / 255, g / 255, b / 255, 1


class SettingsScreen(Screen):
    def __init__(self, app_ref, **kwargs) -> None:
        super().__init__(**kwargs)
        self.app_ref = app_ref

        root = BoxLayout(orientation="vertical", padding=12, spacing=10)
        root.add_widget(
            Label(text="Settings", color=_rgba(NAVY), font_size="20sp", size_hint_y=None, height=36)
        )

        logo = logo_path()
        if logo is not None:
            from kivy.uix.image import Image

            root.add_widget(
                Image(source=str(logo), size_hint_y=None, height=120, fit_mode="contain")
            )

        vol_row = BoxLayout(size_hint_y=None, height=40, spacing=8)
        vol_row.add_widget(Label(text="Volume", color=_rgba(NAVY), size_hint_x=0.3))
        self.volume = Slider(min=0, max=100, value=70)
        vol_row.add_widget(self.volume)
        root.add_widget(vol_row)

        bpm_row = BoxLayout(size_hint_y=None, height=40, spacing=8)
        bpm_row.add_widget(Label(text="Default BPM", color=_rgba(NAVY), size_hint_x=0.4))
        self.bpm = TextInput(text="72", multiline=False, input_filter="int")
        bpm_row.add_widget(self.bpm)
        root.add_widget(bpm_row)

        steps_row = BoxLayout(size_hint_y=None, height=40, spacing=8)
        steps_row.add_widget(Label(text="Default steps", color=_rgba(NAVY), size_hint_x=0.4))
        self.steps = TextInput(text="32", multiline=False, input_filter="int")
        steps_row.add_widget(self.steps)
        root.add_widget(steps_row)

        save_btn = Button(
            text="Save settings",
            size_hint_y=None,
            height=48,
            background_color=_rgba(GOLD),
            color=_rgba(NAVY),
        )
        save_btn.bind(on_release=lambda _b: self._save())
        root.add_widget(save_btn)

        self.status = Label(text="", color=_rgba(MUTED), size_hint_y=None, height=28)
        root.add_widget(self.status)

        root.add_widget(Label(size_hint_y=1))
        root.add_widget(
            Label(
                text="My Py Music Box is open-source software.\n© LHES Tech Solutions · lhes.tech",
                color=_rgba(MUTED),
                halign="center",
                size_hint_y=None,
                height=56,
            )
        )

        nav = BoxLayout(size_hint_y=None, height=44, spacing=8)
        for text, screen in (("Library", "library"), ("Play", "play"), ("Composer", "composer")):
            btn = Button(text=text, background_color=_rgba(NAVY), color=_rgba(CREAM))
            btn.bind(on_release=lambda _b, s=screen: self.app_ref.show_screen(s))
            nav.add_widget(btn)
        root.add_widget(nav)

        self.add_widget(root)
        bind_cream_background(self)

    def on_enter(self, *_args) -> None:
        self.volume.value = self.app_ref.repo.get_volume()
        self.bpm.text = str(self.app_ref.repo.get_default_bpm())
        self.steps.text = str(self.app_ref.repo.get_default_steps())

    def _save(self) -> None:
        try:
            bpm = max(MIN_BPM, min(180, int(self.bpm.text or 72)))
            steps = max(MIN_STEPS, min(MAX_STEPS, int(self.steps.text or 32)))
        except ValueError:
            self.status.text = "Invalid values"
            return
        vol = int(self.volume.value)
        self.app_ref.repo.set_volume(vol)
        self.app_ref.repo.set_default_bpm(bpm)
        self.app_ref.repo.set_default_steps(steps)
        self.app_ref.engine.volume = vol / 100.0
        self.status.text = "Saved"
