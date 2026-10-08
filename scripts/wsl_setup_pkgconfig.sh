#!/usr/bin/env bash
set -euo pipefail
PREFIX="${HOME}/.local"
SRC_DIR="${HOME}/.cache/src"
VER="0.29.2"
mkdir -p "$SRC_DIR" "$PREFIX/bin"
if [[ ! -x "$PREFIX/bin/pkg-config" ]]; then
  cd "$SRC_DIR"
  if [[ ! -d "pkg-config-${VER}" ]]; then
    curl -L --fail -o "pkg-config-${VER}.tar.gz" \
      "https://pkgconfig.freedesktop.org/releases/pkg-config-${VER}.tar.gz"
    tar -xzf "pkg-config-${VER}.tar.gz"
  fi
  cd "pkg-config-${VER}"
  ./configure --prefix="$PREFIX" --with-internal-glib
  make -j"$(nproc)"
  make install
fi
"$PREFIX/bin/pkg-config" --version
# Prove openssl is visible
export PKG_CONFIG_PATH="$PREFIX/lib64/pkgconfig:$PREFIX/lib/pkgconfig:${PKG_CONFIG_PATH:-}"
"$PREFIX/bin/pkg-config" --modversion openssl
echo "pkg-config ready"
