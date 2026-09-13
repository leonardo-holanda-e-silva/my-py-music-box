# SDD-01 — Domain: comb, cylinder, score

## Comb

21 tines, index 0…20, fixed names:

```
G4 A4 B4 C5 D5 E5 F5 G5 A5 B5 C6 D6 E6 F6 G6 A6 B6 C7 D7 E7 F7
```

- One pitch per tine.
- The same tine can be pinned on several steps.
- There is no per-pin dynamics in this version.

## Cylinder

- `steps`: number of columns (8–64, default 32).
- `steps_per_beat`: default 4 (each step = a sixteenth note if the beat is a quarter note).
- `bpm`: 30–180.
- Each cell `(step, tooth)` has at most one pin.

## File contract — `caixa-musica-v1`

Preferred extension: `.caixa.json`

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

Validation rules:

- `format` is required and must equal `caixa-musica-v1`
- `tooth` ∈ [0, 20]
- `step` ∈ [0, steps)
- `note`, if present, must match `NOTE_NAMES[tooth]`
- duplicate pins `(step, tooth)` are collapsed

Invalid files do not play; the UI shows the error and does not change the in-memory score.

## Engine

Input: valid score + volume + device.  
Output: float32 44.1 kHz mono buffer, mixing the 21 samples shifted in time.

The timbre lives in `audio/` (tine synthesis). Swapping the sample generator **does not** change the JSON contract.
