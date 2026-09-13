from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel


class ComposerPage(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Composer — criar e editar a partitura (ver docs/sdd/03-composer.md)"))
        layout.addStretch()
