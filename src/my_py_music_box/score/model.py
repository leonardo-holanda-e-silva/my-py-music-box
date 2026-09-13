from __future__ import annotations

from dataclasses import dataclass, field

FORMAT = "caixa-musica-v1"

NOTE_NAMES = [
    "G4", "A4", "B4",
    "C5", "D5", "E5", "F5", "G5", "A5", "B5",
    "C6", "D6", "E6", "F6", "G6", "A6", "B6",
    "C7", "D7", "E7", "F7",
]


@dataclass
class Pin:
    step: int
    tooth: int

    @property
    def note(self) -> str:
        return NOTE_NAMES[self.tooth]


@dataclass
class Score:
    steps: int = 32
    bpm: int = 72
    steps_per_beat: int = 4
    pins: list[Pin] = field(default_factory=list)

    def validate(self) -> None:
        if not 8 <= self.steps <= 64:
            raise ValueError("steps out of range 8–64")
        if not 30 <= self.bpm <= 180:
            raise ValueError("bpm out of range 30–180")
        seen: set[tuple[int, int]] = set()
        unique: list[Pin] = []
        for pin in self.pins:
            if not 0 <= pin.tooth < 21:
                raise ValueError(f"invalid tooth: {pin.tooth}")
            if not 0 <= pin.step < self.steps:
                raise ValueError(f"invalid step: {pin.step}")
            key = (pin.step, pin.tooth)
            if key not in seen:
                seen.add(key)
                unique.append(pin)
        self.pins = unique

    def to_dict(self) -> dict:
        self.validate()
        return {
            "format": FORMAT,
            "notes": NOTE_NAMES,
            "steps": self.steps,
            "bpm": self.bpm,
            "steps_per_beat": self.steps_per_beat,
            "pins": [
                {"step": p.step, "tooth": p.tooth, "note": p.note} for p in self.pins
            ],
        }

    @classmethod
    def from_dict(cls, data: dict) -> Score:
        if data.get("format") != FORMAT:
            raise ValueError("invalid format")
        pins: list[Pin] = []
        for item in data.get("pins", []):
            tooth = int(item["tooth"])
            if not 0 <= tooth < 21:
                raise ValueError(f"invalid tooth: {tooth}")
            pin = Pin(int(item["step"]), tooth)
            note = item.get("note")
            if note is not None and note != pin.note:
                raise ValueError(f"note {note!r} does not match tooth {tooth}")
            pins.append(pin)
        score = cls(
            steps=int(data.get("steps", 32)),
            bpm=int(data.get("bpm", 72)),
            steps_per_beat=int(data.get("steps_per_beat", 4)),
            pins=pins,
        )
        score.validate()
        return score
