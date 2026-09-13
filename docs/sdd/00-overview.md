# SDD-00 — Overview and how components connect

**App:** My Py Music Box  
**Document version:** 0.1.0  
**Status:** current  
**Repo:** https://github.com/leonardo-holanda-e-silva/my-py-music-box

This file is the map. The other SDDs each describe one slice. If there is a conflict, this overview plus the score contract win.

## 1. Goal

Emulate the mechanism of a music box:

- a **comb** of 21 tines (fixed pitches)
- a **cylinder** with pins
- rotation at a constant BPM
- metallic tine sound, not piano or orchestral samples

The user enters through three pages: Play, Composer, Settings.

## 2. Non-goals (this version)

- More than 21 pitches
- MIDI / SoundFont engine (may become a backend later without changing the contract)
- Cloud account or sync
- Classical notation (staff)

## 3. Document map

| File | Responsibility |
|---|---|
| [00-overview.md](00-overview.md) | Connections, limits, flow |
| [01-domain.md](01-domain.md) | Comb, cylinder, score |
| [02-play.md](02-play.md) | Play page |
| [03-composer.md](03-composer.md) | Composer page |
| [04-settings.md](04-settings.md) | Settings page |
| [05-infrastructure.md](05-infrastructure.md) | Python package, uv, tests |
| [06-packaging.md](06-packaging.md) | Win / macOS / Linux installers |
| [../tasks/README.md](../tasks/README.md) | Task queue linked to the SDDs |

## 4. Components and dependencies

```
                    ┌────────────┐
                    │  Settings  │  persisted preferences
                    └─────┬──────┘
                          │ reads
┌─────────┐         ┌─────▼──────┐         ┌──────────┐
│  Play   │────────▶│  Engine    │◀────────│ Composer │
└─────────┘  plays  │  (audio +  │  writes └──────────┘
                    │   score)   │
                    └─────┬──────┘
                          │
              ┌───────────┼───────────┐
              ▼           ▼           ▼
         AudioBank    ScoreStore   AudioOut
         (21 tines)   (JSON)       (sounddevice)
```

- **UI** (`src/my_py_music_box/ui`) — shell with 3 pages; does not synthesize sound.
- **Score** (`src/my_py_music_box/score`) — reads / validates / writes `caixa-musica-v1`.
- **Audio** (`src/my_py_music_box/audio`) — 21-tine bank + mixer + device.
- **App** (`src/my_py_music_box/app.py`) — creates the window, loads settings, routes pages.

Rules:

1. Play and Composer **do not** know each other. Both talk to Score + Engine.
2. Settings **does not** play audio. It only changes values that Engine and UI read.
3. The score on disk is the source of truth for the melody. UI state is disposable.

## 5. Flows

### Open and play
Settings → last file (if any) → ScoreStore.load → Play.render → Engine.play

### Compose
Composer edits pins in memory → Save → ScoreStore.write → Play can reload the same file

### Switch page
The shell swaps the visible widget. The Engine stops when leaving Play, unless Settings defines “keep playing in the background” (does not exist yet; default = stop).

## 6. Stack

| Layer | Choice |
|---|---|
| Language | Python ≥ 3.11 |
| UI | PyQt5 |
| Audio | NumPy + sounddevice |
| Project / lock | **uv** (`pyproject.toml` + `uv.lock`) |
| Packaging | Briefcase (see SDD-06) |
| License | MIT — open source, owned by LHES Tech Solutions (https://lhes.tech) |
| Visual | `branding/PALETTE.md` + `ui/theme.py` |

The old GitHub description mentions Tkinter. The current implementation is **PyQt5**.

## 7. How to use these docs in a conversation

1. Open this overview.
2. Open the SDD for the page or infra under discussion.
3. Open the task in `docs/tasks/` if there is an ID.
4. Only then read the matching `.py` file.
