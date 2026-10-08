#!/usr/bin/env bash
set -euo pipefail
export PATH="$HOME/.local/bin:$PATH"
VENV="${HOME}/.venvs/buildozer"
uv venv --clear "$VENV"
uv pip install --python "$VENV/bin/python" -U pip wheel setuptools 'cython==0.29.36' buildoze
"$VENV/bin/buildozer" --version
