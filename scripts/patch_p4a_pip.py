#!/usr/bin/env python3
"""Patch p4a build.py so pip can install Android wheels on the host."""
from __future__ import annotations

import re
from pathlib import Path

BUILD_PY = Path(
    "/home/leonardo/builds/my-py-music-box/.buildozer/android/platform/"
    "python-for-android/pythonforandroid/build.py"
)

MARKER = "Cross-install Android wheels"

NEW = '''# Cross-install Android wheels: host pip rejects android_* tags
            # unless platform/python-version/abi are forced.
            py_ver = ctx.python_recipe.major_minor_version_string.replace(".", "")
            plat = f"android_{ctx.ndk_api}_{arch.arch}"
            target = ctx.get_site_packages_dir(arch).replace("'", "'\\\"'\\\"'")
            shprint(sh.bash, '-c', (
                "venv/bin/pip install -v --target '{target}' --no-deps "
                "--platform {plat} --python-version {py_ver} "
                "--implementation cp --abi cp{py_ver} --only-binary=:all: "
                "-r requirements.txt "
                "|| venv/bin/pip install -v --target '{target}' --no-deps "
                "--no-binary=:all: -r requirements.txt"
            ).format(target=target, plat=plat, py_ver=py_ver),
                    _env=copy.copy(env))'''

PAT = re.compile(
    r"shprint\(sh\.bash, '-c', \(\s*"
    r"\"venv/bin/pip \" \+\s*"
    r"\"install -v --target '\{0\}' --no-deps -r requirements\.txt\"\s*"
    r"\)\.format\(ctx\.get_site_packages_dir\(arch\)\.replace\(\"'\", \"'\\\"'\\\"'\"\)\),\s*"
    r"_env=copy\.copy\(env\)\)",
    re.M,
)


def main() -> int:
    if not BUILD_PY.exists():
        print(f"p4a build.py not found: {BUILD_PY}")
        return 0
    text = BUILD_PY.read_text(encoding="utf-8")
    if MARKER in text:
        print("p4a pip install already patched")
        return 0
    new_text, n = PAT.subn(NEW, text, count=1)
    if n != 1:
        print("Could not find pip install block to patch (continuing)")
        return 0
    BUILD_PY.write_text(new_text, encoding="utf-8")
    print("Patched p4a pip install for Android wheel tags")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
