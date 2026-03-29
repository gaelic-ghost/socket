#!/usr/bin/env python3
"""Validate required keys for a speech run manifest JSON file."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REQUIRED_KEYS = [
    "timestamp",
    "input_source",
    "profile_id",
    "effective_voice",
    "effective_instructions",
    "effective_speed",
    "summarize_mode",
    "target_chars",
    "playback_backend",
    "playback_result",
    "audio_output_path",
    "text_sha256",
]


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_manifest.py <manifest.json>")
        return 2

    manifest_path = Path(sys.argv[1])
    if not manifest_path.exists():
        print(f"[ERROR] File not found: {manifest_path}")
        return 2

    try:
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"[ERROR] Invalid JSON: {exc}")
        return 2

    missing = [key for key in REQUIRED_KEYS if key not in payload]
    if missing:
        print("[ERROR] Missing required keys:")
        for key in missing:
            print(f"- {key}")
        return 1

    print("[OK] Manifest contains all required keys.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
