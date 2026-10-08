from __future__ import annotations

import sys
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parent


def _project_root() -> Path:
    # src/my_py_music_box -> src -> project
    return PACKAGE_ROOT.parents[1]


def assets_dir() -> Path:
    """Bundled assets (scores, branding). Works in source tree and Buildozer."""
    candidates = [
        PACKAGE_ROOT / "assets",
        _project_root() / "assets",
        Path(sys.argv[0]).resolve().parent / "assets",
        Path.cwd() / "assets",
    ]
    for path in candidates:
        if path.is_dir():
            return path
    return _project_root() / "assets"


def scores_assets_dir() -> Path:
    return assets_dir() / "scores"


def logo_path() -> Path | None:
    for candidate in (
        assets_dir() / "branding" / "logo-mark.jpg",
        _project_root() / "branding" / "logo-mark.jpg",
    ):
        if candidate.is_file():
            return candidate
    return None


def user_data_dir(app_user_data: str | Path | None = None) -> Path:
    if app_user_data is not None:
        path = Path(app_user_data)
        path.mkdir(parents=True, exist_ok=True)
        return path
    path = Path.home() / ".my-py-music-box"
    path.mkdir(parents=True, exist_ok=True)
    return path


def db_path(app_user_data: str | Path | None = None) -> Path:
    return user_data_dir(app_user_data) / "app.db"
