# My Py Music Box

POC mobile app (Kivy) that emulates a classic **21-tine** music box.

Pages: **Library**, **Play**, **Composer**, **Settings**.

Scores live in **SQLite**. Import/export uses `.caixa.json` (`caixa-musica-v1`).

**Open-source** ([MIT](LICENSE)). Owned by **[LHES Tech Solutions](https://lhes.tech)**.

Visual identity: [`branding/PALETTE.md`](branding/PALETTE.md).

## Requirements

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)
- Android APK build: [Buildozer](https://buildozer.readthedocs.io/) on **Linux/WSL**

## Desktop smoke test

```bash
uv sync
uv run my-py-music-box
```

Tests (unit only):

```bash
uv run pytest
```

## Android APK (WSL)

```bash
# once: install Buildozer deps on Ubuntu/WSL, then:
pip install buildozer
buildozer android debug
```

Install the APK from `bin/*.apk` on the phone.

Built-in scores shipped in the APK:

- Example
- How Deep Is Your Love

## Score format

See [`docs/sdd/01-domain.md`](docs/sdd/01-domain.md) and `assets/scores/`.
