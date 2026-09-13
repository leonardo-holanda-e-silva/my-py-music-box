from __future__ import annotations

from PyQt5.QtWidgets import (
    QHBoxLayout,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from my_py_music_box.ui.pages.composer import ComposerPage
from my_py_music_box.ui.pages.play import PlayPage
from my_py_music_box.ui.pages.settings import SettingsPage
from my_py_music_box.ui.theme import STYLESHEET


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("My Py Music Box")
        self.resize(1100, 700)
        self.setStyleSheet(STYLESHEET)

        root = QWidget()
        self.setCentralWidget(root)
        layout = QVBoxLayout(root)

        nav = QHBoxLayout()
        self.btn_play = QPushButton("Play")
        self.btn_composer = QPushButton("Composer")
        self.btn_settings = QPushButton("Settings")
        nav.addWidget(self.btn_play)
        nav.addWidget(self.btn_composer)
        nav.addWidget(self.btn_settings)
        nav.addStretch()
        layout.addLayout(nav)

        self.stack = QStackedWidget()
        self.page_play = PlayPage()
        self.page_composer = ComposerPage()
        self.page_settings = SettingsPage()
        self.stack.addWidget(self.page_play)
        self.stack.addWidget(self.page_composer)
        self.stack.addWidget(self.page_settings)
        layout.addWidget(self.stack)

        self.btn_play.clicked.connect(lambda: self._show(0))
        self.btn_composer.clicked.connect(lambda: self._show(1))
        self.btn_settings.clicked.connect(lambda: self._show(2))
        self.page_play.open_in_composer_requested.connect(lambda: self._show(1))
        self.page_play.title_changed.connect(self._on_score_title)
        self.statusBar().showMessage("My Py Music Box is open-source software. © LHES Tech Solutions")

    def _show(self, index: int) -> None:
        if index != 0:
            self.page_play.stop()
        self.stack.setCurrentIndex(index)

    def _on_score_title(self, name: str) -> None:
        self.setWindowTitle(f"My Py Music Box — {name}")
        self.statusBar().showMessage(name)

    def closeEvent(self, event) -> None:
        self.page_play.stop()
        super().closeEvent(event)
