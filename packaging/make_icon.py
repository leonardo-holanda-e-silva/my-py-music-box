"""Write packaging/icon.ico from the brand palette (stdlib only)."""

from __future__ import annotations

import struct
import zlib
from pathlib import Path

INK = (0x1A, 0x14, 0x23, 255)
BRASS = (0xC4, 0xA3, 0x5A, 255)
GOLD = (0xE6, 0xC9, 0x7A, 255)
IVORY = (0xF4, 0xEB, 0xD0, 255)


def _png(size: int, pixels: list[tuple[int, int, int, int]]) -> bytes:
    def chunk(tag: bytes, data: bytes) -> bytes:
        return (
            struct.pack(">I", len(data))
            + tag
            + data
            + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        )

    raw = b""
    for y in range(size):
        raw += b"\x00"
        for x in range(size):
            raw += bytes(pixels[y * size + x])
    return b"".join(
        [
            b"\x89PNG\r\n\x1a\n",
            chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0)),
            chunk(b"IDAT", zlib.compress(raw, 9)),
            chunk(b"IEND", b""),
        ]
    )


def _pixels(size: int) -> list[tuple[int, int, int, int]]:
    cx = cy = (size - 1) / 2
    body_r = size * 0.38
    lid_r = size * 0.22
    pixels: list[tuple[int, int, int, int]] = []
    for y in range(size):
        for x in range(size):
            dx, dy = x - cx, y - cy
            dist = (dx * dx + dy * dy) ** 0.5
            if dist <= body_r and dy > -size * 0.05:
                color = BRASS if abs(dy) < size * 0.06 else GOLD
            elif dist <= lid_r and dy < 0:
                color = IVORY
            else:
                color = INK
            pixels.append(color)
    return pixels


def write_ico(path: Path) -> None:
    sizes = (256, 48, 32, 16)
    pngs = [_png(size, _pixels(size)) for size in sizes]
    header = struct.pack("<HHH", 0, 1, len(sizes))
    entries = b""
    offset = 6 + 16 * len(sizes)
    blobs = b""
    for size, png in zip(sizes, pngs, strict=True):
        width = 0 if size == 256 else size
        entries += struct.pack("<BBBBHHII", width, width, 0, 0, 1, 32, len(png), offset)
        blobs += png
        offset += len(png)
    path.write_bytes(header + entries + blobs)


if __name__ == "__main__":
    target = Path(__file__).resolve().parent / "icon.ico"
    write_ico(target)
    print(f"Wrote {target}")
