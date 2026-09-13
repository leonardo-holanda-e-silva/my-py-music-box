# SDD-04 — Settings page

**ID:** `page.settings`  
**Package:** `my_py_music_box.ui.pages.settings`

The list below is the **minimum viable** set. Items marked TBD are not in v0.1.

## v0.1 (define and persist)

| Key | Type | Default | Effect |
|---|---|---|---|
| `volume` | 0–100 | 70 | Output gain |
| `audio_device` | id or `"default"` | `"default"` | sounddevice device |
| `last_score_path` | path or null | null | Play/Composer reopen |
| `default_bpm` | 30–180 | 72 | Used for a new score |
| `default_steps` | 8–64 | 32 | Used for a new score |

Persistence: JSON file in the user config directory  
(`platformdirs` or `QStandardPaths.AppConfigLocation` / `my-py-music-box/settings.json`).

## Later (TBD)

- UI language (pt / en)
- Light / dark theme
- Comb quality (synthesis vs recorded samples)
- Keep playing when switching pages
- Default scores folder

## Behavior

- Immediate apply for volume
- Device applies on the next Play (avoids cutting the stream mid-note)
- Invalid values in the config file fall back to defaults, without crashing

## Done when

- [ ] Volume survives closing and reopening the app
- [ ] Invalid device falls back to default and warns
- [ ] Page does not import Engine except to list devices
