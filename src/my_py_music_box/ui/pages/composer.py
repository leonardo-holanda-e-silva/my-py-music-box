from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel


class ComposerPage(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Composer — create and edit the score (see docs/sdd/03-composer.md)"))
        layout.addStretch()
