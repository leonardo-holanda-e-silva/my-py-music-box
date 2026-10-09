from __future__ import annotations

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView

from my_py_music_box.ui.bg import bind_cream_background
from my_py_music_box.ui.theme import GOLD, MUTED, NAVY, PANEL


class LibraryScreen(Screen):
    def __init__(self, app_ref, **kwargs) -> None:
        super().__init__(**kwargs)
        self.app_ref = app_ref
        root = BoxLayout(orientation="vertical", padding=12, spacing=8)
        root.add_widget(
            Label(
                text="My Py Music Box",
                color=self._rgba(NAVY),
                font_size="22sp",
                size_hint_y=None,
                height=40,
            )
        )
        root.add_widget(
            Label(
                text="Library",
                color=self._rgba(MUTED),
                size_hint_y=None,
                height=28,
            )
        )
        self.list_box = BoxLayout(orientation="vertical", size_hint_y=None, spacing=6)
        self.list_box.bind(minimum_height=self.list_box.setter("height"))
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(self.list_box)
        root.add_widget(scroll)

        nav = BoxLayout(size_hint_y=None, height=48, spacing=8)
        for text, screen in (
            ("Play", "play"),
            ("Composer", "composer"),
            ("Settings", "settings"),
        ):
            btn = Button(text=text, background_color=self._rgba(GOLD), color=self._rgba(NAVY))
            btn.bind(on_release=lambda _b, s=screen: self.app_ref.show_screen(s))
            nav.add_widget(btn)
        root.add_widget(nav)
        self.add_widget(root)
        bind_cream_background(self)

    @staticmethod
    def _rgba(hex_color: str) -> tuple[float, float, float, float]:
        h = hex_color.lstrip("#")
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        return r / 255, g / 255, b / 255, 1

    def on_enter(self, *_args) -> None:
        self.refresh()

    def refresh(self) -> None:
        self.list_box.clear_widgets()
        for record in self.app_ref.repo.list_scores():
            row = BoxLayout(size_hint_y=None, height=56, spacing=6)
            info = Label(
                text=f"{record.title}\n{record.score.steps} steps · {record.score.bpm} BPM · {record.source}",
                color=self._rgba(NAVY),
                halign="left",
                valign="middle",
            )
            info.bind(size=info.setter("text_size"))
            open_btn = Button(
                text="Open",
                size_hint_x=0.25,
                background_color=self._rgba(GOLD),
                color=self._rgba(NAVY),
            )
            open_btn.bind(on_release=lambda _b, rid=record.id: self.app_ref.open_score(rid))
            row.add_widget(info)
            row.add_widget(open_btn)
            if record.source != "builtin":
                del_btn = Button(
                    text="Del",
                    size_hint_x=0.18,
                    background_color=self._rgba(PANEL),
                    color=self._rgba(NAVY),
                )
                del_btn.bind(on_release=lambda _b, rid=record.id: self._delete(rid))
                row.add_widget(del_btn)
            self.list_box.add_widget(row)

    def _delete(self, score_id: int) -> None:
        self.app_ref.repo.delete_score(score_id)
        self.refresh()
