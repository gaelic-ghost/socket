from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest


def _load_module():
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "roadmap_alignment_maintainer.py"
    spec = importlib.util.spec_from_file_location("roadmap_alignment_maintainer", module_path)
    assert spec is not None
    assert spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


m = _load_module()


def test_read_optional_config_reads_known_scalars(tmp_path: Path) -> None:
    config_path = tmp_path / "config" / "customization.template.yaml"
    config_path.parent.mkdir(parents=True)
    config_path.write_text(
        "\n".join(
            [
                'schemaVersion: "1"',
                'profile: default',
                "isCustomized: false",
                'planHistoryVerbosity: standard',
                'changeLogVerbosity: standard',
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    config = m.read_optional_config(tmp_path, None)

    assert config["config_path"] == str(config_path)
    assert config["profile"] == "default"
    assert config["planHistoryVerbosity"] == "standard"


def test_main_invalid_project_root_returns_1(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    missing_root = tmp_path / "missing"
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "roadmap_alignment_maintainer.py",
            "--project-root",
            str(missing_root),
            "--run-mode",
            "check-only",
        ],
    )

    rc = m.main()
    captured = capsys.readouterr()

    assert rc == 1
    assert "Project root does not exist or is not a directory" in captured.err


def test_main_check_only_valid_roadmap_reports_no_findings(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    roadmap = tmp_path / "ROADMAP.md"
    roadmap.write_text(
        "\n".join(
            [
                "# Project Roadmap",
                "",
                "## Vision",
                "",
                "- Keep delivery deterministic.",
                "",
                "## Product principles",
                "",
                "- Prefer bounded maintenance workflows.",
                "",
                "## Milestone Progress",
                "",
                "- [ ] Milestone 0: Foundation",
                "",
                "## Milestone 0: Foundation",
                "",
                "Scope:",
                "",
                "- [ ] Define initial scope.",
                "",
                "Tickets:",
                "",
                "- [ ] First implementation task.",
                "",
                "Exit criteria:",
                "",
                "- [ ] Scope, tickets, and validation are complete.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "roadmap_alignment_maintainer.py",
            "--project-root",
            str(tmp_path),
            "--run-mode",
            "check-only",
            "--print-md",
        ],
    )

    rc = m.main()
    captured = capsys.readouterr()

    assert rc == 0
    assert captured.out.strip() == "No findings."
    assert captured.err == ""
