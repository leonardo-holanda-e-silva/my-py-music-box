from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel


class PlayPage(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Play — play the score (see docs/sdd/02-play.md)"))
        layout.addStretch()
