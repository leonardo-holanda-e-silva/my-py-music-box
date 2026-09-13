from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel


class SettingsPage(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Settings — preferências (ver docs/sdd/04-settings.md)"))
        layout.addStretch()
        layout.addWidget(
            QLabel(
                "My Py Music Box is open-source software.\n"
                "© LHES Tech Solutions · https://lhes.tech"
            )
        )
