#!/usr/bin/env bash
set -eu
PID="${1:-}"
LOG="${HOME}/builds/buildozer-apk.log"
SRC="/mnt/c/Users/Leonardo/Documents/Projetos/my-py-music-box"
WORK="${HOME}/builds/my-py-music-box"

if [[ -z "$PID" ]]; then
  PID=$(pgrep -f 'buildozer android debug' | head -n1 || true)
fi
if [[ -z "$PID" ]]; then
  echo "No buildozer process found"
  exit 1
fi

echo "Waiting for buildozer pid=$PID"
while kill -0 "$PID" 2>/dev/null; do
  sleep 60
  echo "--- still building ---"
  tail -n 3 "$LOG" | sed 's/\x1b\[[0-9;]*m//g' || true
done

set +e
wait "$PID" 2>/dev/null
STATUS=$?
set -e
# If wait couldn't reap (not a child), infer from log
if grep -q 'Buildozer failed' "$LOG"; then
  STATUS=1
elif ls "$WORK"/bin/*.apk >/dev/null 2>&1; then
  STATUS=0
fi

echo "buildozer exit=$STATUS"
tail -n 50 "$LOG" | sed 's/\x1b\[[0-9;]*m//g'
mkdir -p "$SRC/bin"
cp -f "$WORK"/bin/*.apk "$SRC/bin/" 2>/dev/null || true
ls -lh "$WORK/bin" 2>/dev/null || true
ls -lh "$SRC/bin" 2>/dev/null || true
exit "$STATUS"
