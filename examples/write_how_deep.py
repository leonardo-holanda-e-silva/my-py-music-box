"""Write examples/How Deep Is Your Music Box.caixa.json — C-major music-box miniature."""

from pathlib import Path

from my_py_music_box.paths import EXAMPLE_SCORE_NAME
from my_py_music_box.score.model import NOTE_NAMES, Pin, Score
from my_py_music_box.score.store import save

TOOTH = {name: index for index, name in enumerate(NOTE_NAMES)}


def pin(step: int, note: str) -> Pin:
    return Pin(step, TOOTH[note])


def build() -> Score:
    melody = [
        # "I know your eyes in the morning sun"
        (0, "G5"),
        (2, "A5"),
        (4, "G5"),
        (5, "F5"),
        (6, "E5"),
        (7, "F5"),
        (8, "G5"),
        (10, "A5"),
        (12, "C6"),
        (12, "C7"),
        # "I need you so, I'm not ashamed to say"
        (16, "G5"),
        (18, "A5"),
        (20, "G5"),
        (21, "F5"),
        (22, "E5"),
        (23, "F5"),
        (24, "G5"),
        (26, "A5"),
        (28, "C6"),
        (28, "C7"),
        (30, "E6"),
        # "How deep is your love, how deep is your love"
        (32, "E6"),
        (33, "D6"),
        (34, "C6"),
        (35, "B5"),
        (36, "A5"),
        (38, "G5"),
        (40, "E6"),
        (41, "D6"),
        (42, "C6"),
        (43, "B5"),
        (44, "A5"),
        (46, "G5"),
        # "I really need to learn"
        (48, "A5"),
        (50, "B5"),
        (52, "C6"),
        (54, "D6"),
        (56, "E6"),
        (58, "D6"),
        (60, "C6"),
        (62, "G5"),
        (63, "C6"),
    ]
    harmony = [
        (0, "C5"),
        (0, "E5"),
        (0, "G4"),
        (8, "F5"),
        (8, "A4"),
        (8, "C5"),
        (16, "C5"),
        (16, "E5"),
        (16, "G4"),
        (24, "G4"),
        (24, "B4"),
        (24, "D5"),
        (32, "C5"),
        (32, "E5"),
        (32, "G5"),
        (40, "A4"),
        (40, "C5"),
        (40, "E5"),
        (48, "F5"),
        (48, "A4"),
        (48, "C5"),
        (56, "G4"),
        (56, "B4"),
        (56, "D5"),
        (56, "G6"),
        (60, "C5"),
        (60, "E5"),
        (62, "G4"),
    ]
    return Score(
        steps=64,
        bpm=88,
        steps_per_beat=2,
        pins=[pin(step, note) for step, note in melody + harmony],
    )


if __name__ == "__main__":
    target = Path(__file__).resolve().parent / EXAMPLE_SCORE_NAME
    save(build(), target)
    print(f"Wrote {target}")
