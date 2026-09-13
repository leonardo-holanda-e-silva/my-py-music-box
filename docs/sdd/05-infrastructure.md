# SDD-05 — Code infrastructure

## Layout

```
my-py-music-box/
  pyproject.toml          # uv + briefcase
  uv.lock                 # generate with `uv lock` and commit
  LICENSE                 # MIT
  .gitignore              # repo template
  README.md
  docs/sdd/               # this set
  docs/tasks/
  examples/               # sample scores
  packaging/              # installer notes and assets
  src/my_py_music_box/
    app.py                # entrypoint
    ui/shell.py           # window + navigation
    ui/pages/play.py
    ui/pages/composer.py
    ui/pages/settings.py
    score/model.py
    score/store.py
    audio/bank.py
    audio/engine.py
  tests/
```

## Coordination with uv

Source of truth for dependencies: `pyproject.toml`.

```bash
uv sync                     # creates .venv and installs
uv lock                     # updates uv.lock
uv run my-py-music-box      # starts the app
uv run pytest
uv add package              # runtime
uv add --group dev package
uv add --group packaging briefcase
```

Do not use `requirements.txt` as the source. The old prototype file was retired.

Minimum Python: 3.11.

## Package

- Importable code in `src/my_py_music_box`
- Script: `my-py-music-box`
- Tests do not import PyQt5 when they only test pure score/audio (when possible)

## Quality

- Ruff in the `dev` group
- Pytest for JSON validation and the mixer
- No network at runtime

## What .gitignore already covers

The repository `.gitignore` is the standard Python template (includes `.venv`, `dist/`, `build/`, PyInstaller `*.spec`).  
`uv.lock` is **not** ignored (the line is commented out): the lock should be versioned.
