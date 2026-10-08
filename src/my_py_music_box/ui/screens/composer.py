from __future__ import annotations

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput

from my_py_music_box.score.model import MAX_STEPS, MIN_BPM, MIN_STEPS, Score
from my_py_music_box.ui.cylinder import CylinderScroll
from my_py_music_box.ui.theme import CREAM, GOLD, MUTED, NAVY


def _rgba(hex_color: str) -> tuple[float, float, float, float]:
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return r / 255, g / 255, b / 255, 1


class ComposerScreen(Screen):
    def __init__(self, app_ref, **kwargs) -> None:
        super().__init__(**kwargs)
        self.app_ref = app_ref
        self._draft: Score | None = None
        self._title = "Untitled"
        self._score_id: int | None = None

        root = BoxLayout(orientation="vertical", padding=12, spacing=8)
        root.add_widget(
            Label(text="Composer", color=_rgba(NAVY), font_size="20sp", size_hint_y=None, height=36)
        )
        self.status = Label(text="", color=_rgba(MUTED), size_hint_y=None, height=24)
        root.add_widget(self.status)

        form = BoxLayout(size_hint_y=None, height=40, spacing=6)
        self.title_input = TextInput(text="Untitled", multiline=False, size_hint_x=0.5)
        self.bpm_input = TextInput(text="72", multiline=False, input_filter="int", size_hint_x=0.25)
        self.steps_input = TextInput(text="32", multiline=False, input_filter="int", size_hint_x=0.25)
        form.add_widget(self.title_input)
        form.add_widget(self.bpm_input)
        form.add_widget(self.steps_input)
        root.add_widget(form)

        self.cylinder = CylinderScroll(size_hint=(1, 1))
        self.cylinder.set_editable(True)
        root.add_widget(self.cylinder)

        actions = BoxLayout(size_hint_y=None, height=48, spacing=8)
        for text, handler in (
            ("New", self._new),
            ("Apply", self._apply_meta),
            ("Save", self._save),
            ("Export", self._export),
        ):
            btn = Button(text=text, background_color=_rgba(GOLD), color=_rgba(NAVY))
            btn.bind(on_release=lambda _b, h=handler: h())
            actions.add_widget(btn)
        root.add_widget(actions)

        nav = BoxLayout(size_hint_y=None, height=44, spacing=8)
        for text, screen in (("Library", "library"), ("Play", "play"), ("Settings", "settings")):
            btn = Button(text=text, background_color=_rgba(NAVY), color=_rgba(CREAM))
            btn.bind(on_release=lambda _b, s=screen: self.app_ref.show_screen(s))
            nav.add_widget(btn)
        root.add_widget(nav)

        self.add_widget(root)
        with self.canvas.before:
            from kivy.graphics import Color, Rectangle

            Color(*_rgba(CREAM))
            self._bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_bg, size=self._update_bg)

    def _update_bg(self, *_args) -> None:
        self._bg.pos = self.pos
        self._bg.size = self.size

    def on_enter(self, *_args) -> None:
        record = self.app_ref.current_record
        if record is not None:
            self._score_id = record.id if record.source != "builtin" else None
            self._title = record.title if record.source != "builtin" else f"{record.title} (copy)"
            self._draft = record.score.copy()
            if record.source == "builtin":
                self._score_id = None
        else:
            self._new()
            return
        self.title_input.text = self._title
        self.bpm_input.text = str(self._draft.bpm)
        self.steps_input.text = str(self._draft.steps)
        self.cylinder.set_score(self._draft)
        self.status.text = "Editing"

    def _new(self) -> None:
        self._score_id = None
        self._title = "Untitled"
        self._draft = Score(
            steps=self.app_ref.repo.get_default_steps(),
            bpm=self.app_ref.repo.get_default_bpm(),
            pins=[],
        )
        self.title_input.text = self._title
        self.bpm_input.text = str(self._draft.bpm)
        self.steps_input.text = str(self._draft.steps)
        self.cylinder.set_score(self._draft)
        self.status.text = "New score"

    def _apply_meta(self) -> None:
        if self._draft is None:
            return
        try:
            bpm = max(MIN_BPM, min(180, int(self.bpm_input.text or 72)))
            steps = max(MIN_STEPS, min(MAX_STEPS, int(self.steps_input.text or 32)))
        except ValueError:
            self.status.text = "Invalid BPM or steps"
            return
        self._draft.bpm = bpm
        self._draft.set_steps(steps)
        self._title = self.title_input.text.strip() or "Untitled"
        self.cylinder.set_score(self._draft)
        self.status.text = "Updated"

    def _save(self) -> None:
        self._apply_meta()
        if self._draft is None:
            return
        title = self.title_input.text.strip() or "Untitled"
        if self._score_id is None:
            self._score_id = self.app_ref.repo.insert_score(title, self._draft, source="user")
        else:
            self.app_ref.repo.update_score(self._score_id, title, self._draft)
        self.app_ref.open_score(self._score_id)
        self.status.text = "Saved"

    def _export(self) -> None:
        if self._draft is None:
            return
        self._apply_meta()
        from pathlib import Path

        from my_py_music_box.paths import user_data_dir
        from my_py_music_box.score.store import save

        name = (self.title_input.text.strip() or "export").replace(" ", "-")
        path = user_data_dir(self.app_ref.user_data_dir) / f"{name}.caixa.json"
        save(self._draft, path)
        self.status.text = f"Exported: {path.name}"
