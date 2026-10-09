# My Py Music Box

App desktop (Kivy) that emulates a classic **21-tine** music box.

Screens: **Library**, **Play**, **Composer**, **Settings**.

Scores live in **SQLite**. Import/export uses `.caixa.json` (`caixa-musica-v1`).

**Open-source** ([MIT](LICENSE)). Owned by **[LHES Tech Solutions](https://lhes.tech)**.

Visual identity: [`branding/PALETTE.md`](branding/PALETTE.md).

## Requirements

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)

## Run (desktop)

```bash
uv sync
uv run my-py-music-box
```

Or:

```bash
uv run python main.py
```

Built-in scores are seeded on first launch from `assets/scores/`:

- Example
- How Deep Is Your Love

## Tests

```bash
uv run pytest
```

## Score format

See [`docs/sdd/01-domain.md`](docs/sdd/01-domain.md) and `assets/scores/`.
