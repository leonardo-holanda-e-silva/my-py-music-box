#!/usr/bin/env python3
"""Drop Kivy network python_depends (requests stack) — unused in this POC."""
from __future__ import annotations

from pathlib import Path

RECIPE = Path(
    "/home/leonardo/builds/my-py-music-box/.buildozer/android/platform/"
    "python-for-android/pythonforandroid/recipes/kivy/__init__.py"
)

OLD = "python_depends = ['certifi', 'chardet', 'idna', 'requests', 'urllib3', 'filetype']"
NEW = "python_depends = []  # POC: no network stack"


def main() -> int:
    if not RECIPE.exists():
        print(f"kivy recipe not found: {RECIPE}")
        return 0
    text = RECIPE.read_text(encoding="utf-8")
    if NEW in text or "python_depends = []" in text:
        print("kivy python_depends already cleared")
        return 0
    if OLD not in text:
        print("Could not find kivy python_depends line")
        return 1
    RECIPE.write_text(text.replace(OLD, NEW, 1), encoding="utf-8")
    print("Cleared kivy python_depends (no requests stack)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
