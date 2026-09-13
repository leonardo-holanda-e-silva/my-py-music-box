"""Visual tokens — see branding/PALETTE.md."""

INK = "#1A1423"
ATELIER = "#2B1B33"
PLUM = "#4A2545"
OXBLOOD = "#7A2E3A"
BRASS = "#C4A35A"
GOLD = "#E6C97A"
IVORY = "#F4EBD0"
SCORE = "#C9B896"
VERDIGRIS = "#2F6F6B"

STYLESHEET = f"""
QMainWindow, QWidget {{
    background: {INK};
    color: {IVORY};
    font-family: Palatino, Georgia, serif;
}}
QPushButton {{
    background: {PLUM};
    color: {IVORY};
    border: 1px solid {BRASS};
    padding: 8px 16px;
    border-radius: 4px;
}}
QPushButton:hover {{
    background: {OXBLOOD};
    border-color: {GOLD};
}}
QPushButton:checked, QPushButton[active="true"] {{
    background: {BRASS};
    color: {INK};
}}
QLabel {{
    color: {SCORE};
}}
QStatusBar {{
    background: {ATELIER};
    color: {SCORE};
}}
QScrollArea {{
    border: 1px solid {BRASS};
    background: {ATELIER};
}}
QSlider::groove:horizontal {{
    height: 6px;
    background: {PLUM};
    border-radius: 3px;
}}
QSlider::handle:horizontal {{
    width: 14px;
    margin: -5px 0;
    background: {GOLD};
    border-radius: 7px;
}}
"""
