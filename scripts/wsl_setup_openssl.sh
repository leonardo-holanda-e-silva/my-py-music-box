#!/usr/bin/env bash
set -euo pipefail
PREFIX="${HOME}/.local"
OPENSSL_VER="3.3.2"
SRC_DIR="${HOME}/.cache/src"
mkdir -p "$SRC_DIR" "$PREFIX" "$HOME/.config/my-py-music-box"
if [[ ! -f "$PREFIX/include/openssl/ssl.h" ]]; then
  cd "$SRC_DIR"
  if [[ ! -d "openssl-${OPENSSL_VER}" ]]; then
    curl -L --fail -o "openssl-${OPENSSL_VER}.tar.gz" \
      "https://www.openssl.org/source/openssl-${OPENSSL_VER}.tar.gz"
    tar -xzf "openssl-${OPENSSL_VER}.tar.gz"
  fi
  cd "openssl-${OPENSSL_VER}"
  ./config --prefix="$PREFIX" --openssldir="$PREFIX/ssl" --libdir=lib shared zlib no-tests
  make -j"$(nproc)"
  make install_sw
fi
LIBDIR="$PREFIX/lib"
[[ -d "$PREFIX/lib64/pkgconfig" ]] && LIBDIR="$PREFIX/lib64"
# Do NOT export LD_LIBRARY_PATH — it breaks system Python SSL cert verification.
cat > "$HOME/.config/my-py-music-box/openssl.env" <<EOF
export PATH="$PREFIX/bin:\$PATH"
export PKG_CONFIG_PATH="$LIBDIR/pkgconfig:\${PKG_CONFIG_PATH:-}"
export CPPFLAGS="-I$PREFIX/include \${CPPFLAGS:-}"
export CFLAGS="-I$PREFIX/include \${CFLAGS:-}"
export LDFLAGS="-L$LIBDIR -Wl,-rpath,$LIBDIR \${LDFLAGS:-}"
# Needed so hostpython can import the _ssl module built against this OpenSSL.
export LD_LIBRARY_PATH="$LIBDIR:\${LD_LIBRARY_PATH:-}"
EOF
test -f "$PREFIX/include/openssl/ssl.h"
"$PREFIX/bin/openssl" version
echo "OpenSSL ready at $PREFIX"
