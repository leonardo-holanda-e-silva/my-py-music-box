# SDD-03 — Composer page

**ID:** `page.composer`  
**Package:** `my_py_music_box.ui.pages.composer`

## Purpose

Create and edit the cylinder: pins, steps, piece BPM.

## Screen content

- 21 × N grid (tine × step), editable
- Pin counter
- Fields: steps, score BPM
- Buttons: New, Open, Save, Save as, Example, Clear
- Short preview of a tine when clicking the row label (optional in v0.1; separate task)

## Behavior

- Click a cell: toggle the pin
- Changing `steps` drops pins with `step >= steps`
- Dirty (unsaved) blocks “New” until confirmed
- Save writes `caixa-musica-v1` via ScoreStore
- Play is not this page’s job; “Test” may send the in-memory score to the Engine **without** writing to disk (task `T-04`)

## Done when

- [ ] Pin toggle
- [ ] JSON round-trip (save / open identical pins and metadata)
- [ ] Example loads the melody from `examples/`
- [ ] Window title marks a dirty file with `*`
