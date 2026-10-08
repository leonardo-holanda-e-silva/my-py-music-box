# SDD-00 — Overview (POC)

**App:** My Py Music Box  
**Document version:** 0.2.0-poc  
**Status:** POC — Kivy + SQLite Android  

## Goal

Emulate a 21-tine music box on Android (Kivy). Desktop Kivy is only for smoke tests.

## Non-goals (POC)

- iOS, desktop installers, Play Store release
- Broad test suite (unit tests only)
- Dual PyQt + Kivy UI

## Document map

| File | Responsibility |
|---|---|
| [00-overview.md](00-overview.md) | Connections |
| [01-domain.md](01-domain.md) | Comb, cylinder, score JSON |
| [02-play.md](02-play.md) | Play |
| [03-composer.md](03-composer.md) | Composer |
| [04-settings.md](04-settings.md) | Settings |
| [05-infrastructure.md](05-infrastructure.md) | Package, uv, SQLite, Buildozer |

## Stack

| Layer | Choice |
|---|---|
| UI | Kivy |
| Storage | SQLite (`scores`, `prefs`) |
| Score I/O | JSON `caixa-musica-v1` |
| Audio | NumPy render → WAV → SoundLoader |
| Android | Buildozer / python-for-android |
| License | MIT — LHES Tech Solutions |

## Components

```
Library / Play / Composer / Settings
        │
        ├─► Repository (SQLite)
        └─► Engine (render + SoundLoader)
```
