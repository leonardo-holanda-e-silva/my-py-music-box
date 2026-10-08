#!/usr/bin/env bash
set -eu
# Prefer userspace tools; strip Windows PATH entries with spaces (breaks env/exec)
export PATH="$HOME/.local/bin:$HOME/.venvs/buildozer/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

if [[ -f "$HOME/.config/my-py-music-box/java.env" ]]; then
  # shellcheck disable=SC1091
  source "$HOME/.config/my-py-music-box/java.env"
fi
if [[ -f "$HOME/.config/my-py-music-box/openssl.env" ]]; then
  # shellcheck disable=SC1091
  source "$HOME/.config/my-py-music-box/openssl.env"
fi
# shellcheck disable=SC1091
source "$HOME/.venvs/buildozer/bin/activate"
export PATH="$HOME/.local/bin:$VIRTUAL_ENV/bin:$PATH"

command -v autoreconf >/dev/null || {
  echo "autoreconf missing; install autoconf/automake/libtool into ~/.local"
  exit 1
}
command -v java >/dev/null || {
  echo "java missing; source java.env"
  exit 1
}

SRC="/mnt/c/Users/Leonardo/Documents/Projetos/my-py-music-box"
WORK="${HOME}/builds/my-py-music-box"
mkdir -p "$WORK"
cp -a "$SRC/main.py" "$SRC/buildozer.spec" "$SRC/pyproject.toml" "$SRC/README.md" "$WORK/"
rm -rf "$WORK/src" "$WORK/assets" "$WORK/branding"
cp -a "$SRC/src" "$WORK/"
cp -a "$SRC/assets" "$WORK/"
cp -a "$SRC/branding" "$WORK/" 2>/dev/null || true
cd "$WORK"

if [[ ! -d .buildozer/android/platform/python-for-android ]]; then
  buildozer android update || true
fi
bash "$SRC/scripts/wsl_patch_hostpython.sh"
bash "$SRC/scripts/wsl_patch_p4a_pip.sh"
python3 "$SRC/scripts/patch_kivy_deps.py"

HP_BIN=".buildozer/android/platform/build-arm64-v8a/build/other_builds/hostpython3/desktop/hostpython3/native-build/root/usr/local/bin/python"
if [[ -x "$HP_BIN" ]]; then
  echo "Reusing existing hostpython at $HP_BIN"
  "$HP_BIN" -c 'import ssl; print(ssl.OPENSSL_VERSION)'
fi

# Drop ffpyplayer/ffmpeg leftovers if present (requirements no longer include them)
rm -rf .buildozer/android/platform/build-arm64-v8a/dists/mymusicbox
rm -rf .buildozer/android/platform/build-arm64-v8a/build/other_builds/ffpyplayer*
rm -rf .buildozer/android/platform/build-arm64-v8a/build/other_builds/ffmpeg*

echo "Building APK in $PWD"
LOG="$HOME/builds/buildozer-apk.log"
: >"$LOG"
nohup buildozer android debug >>"$LOG" 2>&1 &
PID=$!
echo "buildozer pid=$PID log=$LOG"
while kill -0 "$PID" 2>/dev/null; do
  sleep 60
  echo "--- $(date -Iseconds) still building ---"
  # Prefer high-level INFO lines over clang spam
  grep -E '\[INFO\]|Command failed|BUILD SUCCESSFUL|\.apk' "$LOG" | tail -n 8 || tail -n 3 "$LOG"
done
set +e
wait "$PID"
STATUS=$?
set -e
echo "buildozer exit=$STATUS"
tail -n 80 "$LOG"
mkdir -p "$SRC/bin"
cp -f bin/*.apk "$SRC/bin/" 2>/dev/null || true
ls -lh bin 2>/dev/null || true
ls -lh "$SRC/bin" 2>/dev/null || true
exit "$STATUS"
