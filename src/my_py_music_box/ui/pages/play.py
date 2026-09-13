from __future__ import annotations

import json
from pathlib import Path

from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QSlider,
    QVBoxLayout,
    QWidget,
)

from my_py_music_box.audio.engine import Engine
from my_py_music_box.paths import example_score_path, examples_dir
from my_py_music_box.score.store import load
from my_py_music_box.ui.cylinder import CylinderView


class PlayPage(QWidget):
    open_in_composer_requested = pyqtSignal()
    title_changed = pyqtSignal(str)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._engine = Engine()
        self._score = None
        self._path: Path | None = None

        self.file_label = QLabel("No score")
        self.status_label = QLabel("")
        self.bpm_label = QLabel("BPM —")
        self.volume_label = QLabel("Volume 70")

        self.btn_open = QPushButton("Open")
        self.btn_example = QPushButton("Example")
        self.btn_reload = QPushButton("Reload")
        self.btn_play = QPushButton("Play")
        self.btn_pause = QPushButton("Pause")
        self.btn_stop = QPushButton("Stop")
        self.btn_composer = QPushButton("Open in Composer")

        self.volume = QSlider(Qt.Horizontal)
        self.volume.setRange(0, 100)
        self.volume.setValue(70)
        self.volume.setMaximumWidth(160)

        self.cylinder = CylinderView()
        scroll = QScrollArea()
        scroll.setWidget(self.cylinder)
        scroll.setWidgetResizable(True)

        top = QHBoxLayout()
        top.addWidget(self.file_label, 1)
        top.addWidget(self.btn_open)
        top.addWidget(self.btn_example)
        top.addWidget(self.btn_reload)

        controls = QHBoxLayout()
        controls.addWidget(self.btn_play)
        controls.addWidget(self.btn_pause)
        controls.addWidget(self.btn_stop)
        controls.addSpacing(16)
        controls.addWidget(self.bpm_label)
        controls.addSpacing(12)
        controls.addWidget(self.volume_label)
        controls.addWidget(self.volume)
        controls.addStretch()
        controls.addWidget(self.btn_composer)

        layout = QVBoxLayout(self)
        layout.addLayout(top)
        layout.addLayout(controls)
        layout.addWidget(scroll, 1)
        layout.addWidget(self.status_label)

        self.btn_open.clicked.connect(self._open)
        self.btn_example.clicked.connect(self._load_example)
        self.btn_reload.clicked.connect(self._reload)
        self.btn_play.clicked.connect(self._play)
        self.btn_pause.clicked.connect(self._pause)
        self.btn_stop.clicked.connect(self.stop)
        self.btn_composer.clicked.connect(self._open_in_composer)
        self.volume.valueChanged.connect(self._volume_changed)

        self._timer = QTimer(self)
        self._timer.setInterval(33)
        self._timer.timeout.connect(self._tick)

        self._engine.volume = 0.7
        self._refresh_buttons()
        self._load_example(silent=True)

    def stop(self) -> None:
        self._timer.stop()
        self._engine.stop()
        self.cylinder.set_playhead(None)
        self._refresh_buttons()

    def _volume_changed(self, value: int) -> None:
        self._engine.volume = value / 100.0
        self.volume_label.setText(f"Volume {value}")

    def _open(self) -> None:
        start = str(self._path.parent if self._path else examples_dir() or Path.home())
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Open score",
            start,
            "Music box score (*.caixa.json);;JSON (*.json);;All files (*.*)",
        )
        if path:
            self._load_path(Path(path))

    def _load_example(self, silent: bool = False) -> None:
        path = example_score_path()
        if path is None:
            if not silent:
                self.status_label.setText("Example score not found.")
            return
        self._load_path(path)

    def _reload(self) -> None:
        if self._path is None:
            self.status_label.setText("No score to reload.")
            return
        self._load_path(self._path)

    def _load_path(self, path: Path) -> None:
        self.stop()
        try:
            score = load(path)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            self.status_label.setText(f"Could not open score: {exc}")
            return
        self._score = score
        self._path = path
        self.cylinder.set_score(score)
        self.file_label.setText(path.name)
        self.bpm_label.setText(f"BPM {score.bpm}")
        self.status_label.setText("")
        self.title_changed.emit(path.name)
        self._refresh_buttons()

    def _play(self) -> None:
        if self._engine.is_paused():
            self._engine.resume()
            self._timer.start()
            self._refresh_buttons()
            return
        if self._score is None:
            self.status_label.setText("Open a score before playing.")
            return
        try:
            self._engine.play(self._score)
        except (OSError, RuntimeError) as exc:
            self.status_label.setText(f"Could not start audio: {exc}")
            self.stop()
            return
        self.status_label.setText("")
        self._timer.start()
        self._refresh_buttons()

    def _pause(self) -> None:
        if self._engine.is_playing():
            self._engine.pause()
            self._refresh_buttons()

    def _open_in_composer(self) -> None:
        self.stop()
        self.open_in_composer_requested.emit()

    def _tick(self) -> None:
        if self._engine.finished():
            self.stop()
            return
        self.cylinder.set_playhead(self._engine.current_step())

    def _refresh_buttons(self) -> None:
        has_score = self._score is not None
        playing = self._engine.is_playing()
        paused = self._engine.is_paused()
        self.btn_play.setEnabled(has_score and not playing)
        self.btn_pause.setEnabled(playing)
        self.btn_stop.setEnabled(playing or paused)
        self.btn_reload.setEnabled(self._path is not None)
        self.btn_composer.setEnabled(has_score)
        self.btn_example.setEnabled(example_score_path() is not None)
