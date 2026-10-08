"""Audio device listing is not used on mobile; kept as a stub for API stability."""

from __future__ import annotations


def list_output_devices() -> list[tuple[str, str]]:
    return [("default", "System default")]
