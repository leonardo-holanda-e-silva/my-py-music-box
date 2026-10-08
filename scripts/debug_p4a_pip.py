#!/usr/bin/env python3
from pathlib import Path

text = Path(
    "/home/leonardo/builds/my-py-music-box/.buildozer/android/platform/"
    "python-for-android/pythonforandroid/build.py"
).read_text(encoding="utf-8")
i = text.find("venv/bin/pip")
print("INDEX", i)
print(repr(text[i - 40 : i + 280]))
print("CRLF around area", "\r\n" in text[i : i + 300])

# Try regex replace instead
import re

pat = re.compile(
    r"shprint\(sh\.bash, '-c', \(\s*"
    r"\"venv/bin/pip \" \+\s*"
    r"\"install -v --target '\{0\}' --no-deps -r requirements\.txt\"\s*"
    r"\)\.format\(ctx\.get_site_packages_dir\(arch\)\.replace\(\"'\", \"'\\\"'\\\"'\"\)\),\s*"
    r"_env=copy\.copy\(env\)\)",
    re.M,
)
m = pat.search(text)
print("REGEX MATCH", bool(m))
if m:
    print("MATCH REPR", repr(m.group(0)[:120]))
