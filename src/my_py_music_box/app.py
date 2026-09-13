from __future__ import annotations

import sys

from PyQt5.QtWidgets import QApplication

from my_py_music_box.ui.shell import MainWindow


def main() -> None:
    app = QApplication(sys.argv)
    app.setApplicationName("My Py Music Box")
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
