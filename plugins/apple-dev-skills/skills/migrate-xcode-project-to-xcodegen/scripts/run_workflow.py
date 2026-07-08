#!/usr/bin/env python3
"""Runtime entrypoint for migrate-xcode-project-to-xcodegen."""

from __future__ import annotations

import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from migrate_xcode_project_to_xcodegen import main  # noqa: E402


if __name__ == "__main__":
    raise SystemExit(main())
