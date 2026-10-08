# SDD-05 — Infrastructure (POC)

## Layout

```
my-py-music-box/
  main.py                 # Buildozer entry
  buildozer.spec
  pyproject.toml
  assets/scores/          # builtin JSON scores
  assets/branding/
  src/my_py_music_box/
    app.py
    db/repository.py
    score/
    audio/
    ui/
  tests/                  # unit tests only
```

## uv

```bash
uv sync
uv lock
uv run my-py-music-box
uv run pytest
```

## SQLite

DB path: `App.user_data_dir / app.db` (Android private storage; `~/.my-py-music-box` on desktop).

Tables: `scores`, `prefs`. Builtins seeded once from `assets/scores/*.json`.

## Android

Build on WSL/Linux: `buildozer android debug` → `bin/*.apk`.
