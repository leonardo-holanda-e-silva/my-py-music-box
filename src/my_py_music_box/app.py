from __future__ import annotations

import os
import sys


def _configure_qt_platform() -> None:
    """Prefer Wayland on WSL. PyQt5's xcb plugin often fails until extra libxcb packages exist."""
    if sys.platform != "linux" or os.environ.get("QT_QPA_PLATFORM"):
        return
    if os.environ.get("WSL_DISTRO_NAME") and os.environ.get("WAYLAND_DISPLAY"):
        os.environ["QT_QPA_PLATFORM"] = "wayland"


def main() -> None:
    _configure_qt_platform()
    from PyQt5.QtWidgets import QApplication

    from my_py_music_box.ui.shell import MainWindow

    app = QApplication(sys.argv)
    app.setApplicationName("My Py Music Box")
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
