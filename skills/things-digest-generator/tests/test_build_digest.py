from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest


def _load_module():
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "build_digest.py"
    spec = importlib.util.spec_from_file_location("build_digest", module_path)
    assert spec is not None
    assert spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


m = _load_module()


def test_resolve_settings_uses_template_defaults() -> None:
    settings, active_path, source = m.resolve_settings("")

    assert settings["daysAhead"] == 4
    assert settings["outputStyle"] == "operational"
    assert active_path.name == "customization.yaml"
    assert source.endswith("skills/things-digest-generator/config/customization.template.yaml")


def test_read_items_missing_path_raises_input_error(tmp_path: Path) -> None:
    missing = tmp_path / "missing.json"

    with pytest.raises(m.InputLoadError, match="Input error: missing required input file"):
        m.read_items(str(missing), "--areas")


def test_main_no_findings_outputs_exact_message(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    areas = tmp_path / "areas.json"
    projects = tmp_path / "projects.json"
    open_todos = tmp_path / "open.json"
    recent_done = tmp_path / "recent.json"

    for path in (areas, projects, open_todos, recent_done):
        path.write_text("[]\n", encoding="utf-8")

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "build_digest.py",
            "--areas",
            str(areas),
            "--projects",
            str(projects),
            "--open-todos",
            str(open_todos),
            "--recent-done",
            str(recent_done),
            "--today",
            "2026-03-06",
        ],
    )

    rc = m.main()
    captured = capsys.readouterr()

    assert rc == 0
    assert captured.out.strip() == "No findings."
    assert captured.err == ""
