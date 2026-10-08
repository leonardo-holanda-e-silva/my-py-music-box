#!/usr/bin/env bash
set -euo pipefail
RECIPE="/home/leonardo/builds/my-py-music-box/.buildozer/android/platform/python-for-android/pythonforandroid/recipes/hostpython3/__init__.py"
if [[ ! -f "$RECIPE" ]]; then
  echo "hostpython recipe not found yet: $RECIPE"
  exit 0
fi
python3 - <<'PY'
from pathlib import Path
path = Path("/home/leonardo/builds/my-py-music-box/.buildozer/android/platform/python-for-android/pythonforandroid/recipes/hostpython3/__init__.py")
text = path.read_text(encoding="utf-8")
needle = '''                shprint(
                    sh.Command(join(recipe_build_dir, "configure")),
                    "--prefix",
                    self.local_dir,
                    _env=env,
                )'''
replacement = '''                shprint(
                    sh.Command(join(recipe_build_dir, "configure")),
                    "--prefix",
                    self.local_dir,
                    "--disable-test-modules",
                    _env=env,
                )'''
if "--disable-test-modules" in text:
    print("hostpython recipe already patched")
elif needle not in text:
    raise SystemExit("Could not find configure block to patch")
else:
    path.write_text(text.replace(needle, replacement, 1), encoding="utf-8")
    print("Patched hostpython recipe: --disable-test-modules")
PY
