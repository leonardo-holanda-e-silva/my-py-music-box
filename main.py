"""Desktop / local entrypoint (also usable by Buildozer as main.py)."""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent
_SRC = _ROOT / "src"
if _SRC.is_dir() and str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from my_py_music_box.app import main

if __name__ == "__main__":
    main()
