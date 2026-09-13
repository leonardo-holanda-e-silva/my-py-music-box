# My Py Music Box

Desktop app that emulates a classic **21-tine** steel music box.

Three pages:

- **Play** — plays a score
- **Composer** — creates and edits the cylinder (pins)
- **Settings** — app preferences

**Open-source** software ([MIT](LICENSE) license).  
Owned by **[LHES Tech Solutions](https://lhes.tech)**.

Visual identity: [`branding/PALETTE.md`](branding/PALETTE.md).

End-user run instructions: [English](README.html) · [Português](LEIAME.html).

## Requirements

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)

## Development

```bash
uv sync
uv run my-py-music-box
```

On Linux and WSL, also install PortAudio and the Qt xcb libraries:

```bash
sudo apt install libportaudio2 libxcb-cursor0 libxcb-xinerama0 libxkbcommon-x11-0 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-randr0 libxcb-render-util0
```

Tests:

```bash
uv run pytest
```

## Documentation (SDD)

Start with [`docs/sdd/00-overview.md`](docs/sdd/00-overview.md).

## Packaging

See [`docs/sdd/05-infrastructure.md`](docs/sdd/05-infrastructure.md) and [`docs/sdd/06-packaging.md`](docs/sdd/06-packaging.md).

```bash
uv sync --group packaging
uv run briefcase create windows --no-input
uv run briefcase build windows --no-input
uv run briefcase package windows --no-input --adhoc-sign
```

The Windows installer is written to `dist/My Py Music Box-0.1.0.msi`.
