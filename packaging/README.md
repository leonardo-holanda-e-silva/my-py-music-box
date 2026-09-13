# Packaging assets

Briefcase icons and notes live here.

- `icon.ico` — Windows app/installer icon (regenerate with `python packaging/make_icon.py`)

Build a Windows MSI (does not require Python on the end-user machine):

```bash
uv sync --group packaging
uv run briefcase create windows --no-input
uv run briefcase build windows --no-input
uv run briefcase package windows --no-input --adhoc-sign
```

Output: `dist/My Py Music Box-0.1.0.msi`

The repository `.gitignore` ignores PyInstaller `*.spec` files, Briefcase logs, and the `dist/` and `build/` folders.
Do not commit installer binaries.

See `docs/sdd/06-packaging.md`.
