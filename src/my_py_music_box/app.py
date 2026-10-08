from __future__ import annotations

import os
import traceback
from pathlib import Path

# Prefer a desktop-friendly backend when not on Android.
if not any(key in os.environ for key in ("ANDROID_ARGUMENT", "ANDROID_ROOT")):
    os.environ.setdefault("KIVY_NO_ARGS", "1")


class _BrokenEngine:
    def __init__(self, reason: str) -> None:
        self.volume = 0.7
        self.reason = reason

    def is_playing(self) -> bool:
        return False

    def is_paused(self) -> bool:
        return False

    def is_active(self) -> bool:
        return False

    def finished(self) -> bool:
        return True

    def current_step(self) -> int | None:
        return None

    def play(self, *_a, **_k):
        raise RuntimeError(f"Audio unavailable: {self.reason}")

    def pause(self) -> None:
        return None

    def resume(self) -> None:
        return None

    def stop(self) -> None:
        return None


def main() -> None:
    from kivy.app import App
    from kivy.uix.label import Label
    from kivy.uix.screenmanager import ScreenManager
    from kivy.uix.scrollview import ScrollView

    from my_py_music_box.db.repository import Repository
    from my_py_music_box.paths import db_path
    from my_py_music_box.ui.screens.composer import ComposerScreen
    from my_py_music_box.ui.screens.library import LibraryScreen
    from my_py_music_box.ui.screens.play import PlayScreen
    from my_py_music_box.ui.screens.settings import SettingsScreen

    class MusicBoxApp(App):
        title = "My Py Music Box"

        def build(self):
            try:
                return self._build_ui()
            except Exception:
                text = traceback.format_exc()
                try:
                    crash = Path(self.user_data_dir) / "crash.log"
                    crash.write_text(text, encoding="utf-8")
                    text = f"Crash log: {crash}\n\n{text}"
                except Exception:
                    pass
                label = Label(
                    text=text[:8000],
                    color=(0.2, 0.05, 0.05, 1),
                    size_hint_y=None,
                    halign="left",
                    valign="top",
                    font_size="12sp",
                    padding=(12, 12),
                )
                label.bind(texture_size=label.setter("size"))
                scroll = ScrollView()
                scroll.add_widget(label)
                return scroll

        def _build_ui(self):
            # Engine pulls numpy — keep UI bootable if audio stack fails.
            try:
                from my_py_music_box.audio.engine import Engine

                self.engine = Engine()
            except Exception as exc:  # noqa: BLE001
                self.engine = _BrokenEngine(str(exc))

            self.repo = Repository(db_path(self.user_data_dir))
            self.repo.seed_builtins()
            try:
                self.engine.volume = self.repo.get_volume() / 100.0
            except Exception:
                pass
            self.current_record = None

            self.sm = ScreenManager()
            self.sm.add_widget(LibraryScreen(self, name="library"))
            self.sm.add_widget(PlayScreen(self, name="play"))
            self.sm.add_widget(ComposerScreen(self, name="composer"))
            self.sm.add_widget(SettingsScreen(self, name="settings"))

            last = self.repo.get_last_score_id()
            if last is not None:
                self.current_record = self.repo.get_score(last)
            else:
                scores = self.repo.list_scores()
                if scores:
                    preferred = next(
                        (s for s in scores if s.title == "Example"), scores[0]
                    )
                    self.current_record = preferred
                    self.repo.set_last_score_id(preferred.id)
            return self.sm

        def show_screen(self, name: str) -> None:
            self.sm.current = name

        def open_score(self, score_id: int, switch: bool = True) -> None:
            record = self.repo.get_score(score_id)
            if record is None:
                return
            self.current_record = record
            self.repo.set_last_score_id(score_id)
            if switch:
                self.sm.current = "play"

        def on_stop(self) -> None:
            try:
                self.engine.stop()
            except Exception:
                pass
            try:
                self.repo.close()
            except Exception:
                pass

    MusicBoxApp().run()


if __name__ == "__main__":
    main()
