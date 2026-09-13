# SDD-06 — Instaladores Windows, macOS e Linux

## Meta

Um usuário sem Python instalado consegue instalar e abrir **My Py Music Box**.

## Ferramenta

[Briefcase](https://briefcase.readthedocs.io/) (BeeWare), declarado no grupo `packaging` do `pyproject.toml`.

Motivo: um fluxo para as três plataformas; metadados já no `pyproject.toml`.  
PyInstaller fica de reserva se o Briefcase travar no áudio PortAudio. Os `*.spec` do PyInstaller **não** devem ser commitados — o `.gitignore` do repo já ignora `*.spec`.

## Artefatos alvo

| SO | Comando | Artefato |
|---|---|---|
| Windows | `uv run briefcase package windows` | `.msi` ou `.exe` |
| macOS | `uv run briefcase package macOS` | `.dmg` |
| Linux | `uv run briefcase package linux` | `.AppImage` ou `.deb` |

Ícone e identificador: `dev.leonardo.mypymusicbox` (ajustável).

## CI (tarefa T-08)

GitHub Actions com 3 jobs (`windows-latest`, `macos-latest`, `ubuntu-latest`):

1. `astral-sh/setup-uv`
2. `uv sync --group packaging`
3. `briefcase create && build && package`
4. Upload do artefato no Release

Assinatura de código (Apple / Authenticode) é TBD; v0.1 pode distribuir sem assinatura, com aviso no README.

## Runtime empacotado

O bundle precisa incluir:

- Python + PyQt5
- NumPy
- sounddevice **e** a lib PortAudio do wheel

Teste de aceitação do instalador: abrir o app, carregar `examples/exemplo.caixa.json`, apertar Play e ouvir som.
