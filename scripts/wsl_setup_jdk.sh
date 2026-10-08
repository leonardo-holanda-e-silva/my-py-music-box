#!/usr/bin/env bash
set -euo pipefail
export PATH="$HOME/.local/bin:$PATH"
JDK_ROOT="${HOME}/.jdks"
JDK_DIR="${JDK_ROOT}/jdk-17.0.13+11"
if [[ ! -x "${JDK_DIR}/bin/javac" ]]; then
  mkdir -p "$JDK_ROOT"
  TMP="$(mktemp -d)"
  URL="https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.13%2B11/OpenJDK17U-jdk_x64_linux_hotspot_17.0.13_11.tar.gz"
  echo "Downloading Temurin JDK 17..."
  curl -L --fail -o "$TMP/jdk.tgz" "$URL"
  tar -xzf "$TMP/jdk.tgz" -C "$JDK_ROOT"
  rm -rf "$TMP"
fi
# Normalize extracted folder name if needed
if [[ ! -x "${JDK_DIR}/bin/javac" ]]; then
  FOUND="$(find "$JDK_ROOT" -maxdepth 2 -type f -name javac | head -n1)"
  JDK_DIR="$(dirname "$(dirname "$FOUND")")"
fi
echo "JDK at $JDK_DIR"
"$JDK_DIR/bin/javac" -version
# Persist for later shells
mkdir -p "$HOME/.config/my-py-music-box"
echo "export JAVA_HOME=\"$JDK_DIR\"" > "$HOME/.config/my-py-music-box/java.env"
echo "export PATH=\"\$JAVA_HOME/bin:\$PATH\"" >> "$HOME/.config/my-py-music-box/java.env"
