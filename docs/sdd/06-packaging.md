# SDD-06 — Windows, macOS, and Linux installers

## Goal

A user without Python installed can install and open **My Py Music Box**.

## Tool

[Briefcase](https://briefcase.readthedocs.io/) (BeeWare), declared in the `packaging` group of `pyproject.toml`.

Reason: one flow for all three platforms; metadata already lives in `pyproject.toml`.  
PyInstaller is a fallback if Briefcase stalls on PortAudio. PyInstaller `*.spec` files **must not** be committed — the repo `.gitignore` already ignores `*.spec`.

## Target artifacts

| OS | Command | Artifact |
|---|---|---|
| Windows | `uv run briefcase package windows` | `.msi` or `.exe` |
| macOS | `uv run briefcase package macOS` | `.dmg` |
| Linux | `uv run briefcase package linux` | `.AppImage` or `.deb` |

Icon and identifier: `dev.leonardo.mypymusicbox` (adjustable).

## CI (task T-08)

GitHub Actions with 3 jobs (`windows-latest`, `macos-latest`, `ubuntu-latest`):

1. `astral-sh/setup-uv`
2. `uv sync --group packaging`
3. `briefcase create && build && package`
4. Upload the artifact on the Release

Code signing (Apple / Authenticode) is TBD; v0.1 may ship unsigned, with a note in the README.

## Packaged runtime

The bundle must include:

- Python + PyQt5
- NumPy
- sounddevice **and** the PortAudio lib from the wheel

Installer acceptance test: open the app, load `examples/example.caixa.json`, press Play, and hear sound.
