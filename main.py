"""Buildozer / python-for-android entrypoint."""

from __future__ import annotations

import sys
import traceback
from pathlib import Path

_ROOT = Path(__file__).resolve().parent
_SRC = _ROOT / "src"
if _SRC.is_dir() and str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))


def _write_crash(text: str) -> Path | None:
    candidates = [
        _ROOT / "crash.log",
        Path.home() / "mymusicbox-crash.log",
        Path("/sdcard/Download/mymusicbox-crash.log"),
    ]
    try:
        from android.storage import app_storage_path  # type: ignore

        candidates.insert(0, Path(app_storage_path()) / "mymusicbox-crash.log")
    except Exception:
        pass
    for path in candidates:
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
            return path
        except Exception:
            continue
    return None


def _show_crash(text: str) -> None:
    from kivy.app import App
    from kivy.uix.label import Label
    from kivy.uix.scrollview import ScrollView

    class CrashApp(App):
        def build(self):
            label = Label(
                text=text,
                color=(1, 0.9, 0.9, 1),
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

    CrashApp().run()


def main() -> None:
    try:
        from my_py_music_box.app import main as run_app

        run_app()
    except Exception:
        text = traceback.format_exc()
        path = _write_crash(text)
        if path is not None:
            text = f"Crash log: {path}\n\n{text}"
        try:
            _show_crash(text[:8000])
        except Exception:
            raise


# p4a sometimes imports this module without __name__ == "__main__"
main()
