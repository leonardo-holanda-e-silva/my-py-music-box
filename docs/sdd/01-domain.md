# SDD-01 — Domain: comb, cylinder, score

## Comb

21 tines, index 0…20:

```
G4 A4 B4 C5 D5 E5 F5 G5 A5 B5 C6 D6 E6 F6 G6 A6 B6 C7 D7 E7 F7
```

## Cylinder

- `steps`: 8–1024
- `steps_per_beat`: default 4
- `bpm`: 30–180
- Each cell `(step, tooth)` has at most one pin

## File contract — `caixa-musica-v1`

Extension: `.caixa.json` (plain `.json` accepted for import)

```json
{
  "format": "caixa-musica-v1",
  "notes": ["G4", "…", "F7"],
  "steps": 32,
  "bpm": 68,
  "steps_per_beat": 4,
  "pins": [
    {"step": 0, "tooth": 3, "note": "C5"}
  ]
}
```

## Persistence

Primary store: SQLite. JSON is import/export only.
