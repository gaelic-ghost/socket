from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parent.parent / "scripts" / "audit_skill_surfaces.py"
SPEC = importlib.util.spec_from_file_location("audit_skill_surfaces", MODULE_PATH)
assert SPEC and SPEC.loader
audit_skill_surfaces = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = audit_skill_surfaces
SPEC.loader.exec_module(audit_skill_surfaces)


def write(path: Path, contents: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(contents, encoding="utf-8")


def make_repo(tmp_path: Path) -> Path:
    write(
        tmp_path / "plugins" / "swiftasb-skills" / "skills" / "build-swiftui-app" / "SKILL.md",
        "\n".join(
            [
                "# Build SwiftUI App",
                "",
                "As of SwiftASB `v1.6.0`, use current app-facing handles.",
                "",
                "Use `apple-dev-skills:explore-apple-swift-docs` for Apple framework docs.",
                "",
            ]
        ),
    )
    write(
        tmp_path / "plugins" / "swiftasb-skills" / "skills" / "diagnose-integration" / "SKILL.md",
        "\n".join(
            [
                "# Diagnose Integration",
                "",
                "Run the repository's documented validation path.",
                "",
            ]
        ),
    )
    write(
        tmp_path / "plugins" / "productivity-skills" / "skills" / "maintain-project-readme" / "SKILL.md",
        "\n".join(
            [
                "# Maintain README",
                "",
                "When the user explicitly requests subagents, use bounded discovery.",
                "",
            ]
        ),
    )
    shared_reference = "# Shared\n\nSame text.\n"
    write(
        tmp_path
        / "plugins"
        / "apple-dev-skills"
        / "skills"
        / "xcode-build-run-workflow"
        / "references"
        / "snippets"
        / "apple-core.md",
        shared_reference,
    )
    write(
        tmp_path
        / "plugins"
        / "apple-dev-skills"
        / "skills"
        / "xcode-testing-workflow"
        / "references"
        / "snippets"
        / "apple-core.md",
        shared_reference,
    )
    return tmp_path


def test_build_report_counts_skill_surfaces_and_hotspots(tmp_path: Path) -> None:
    repo_root = make_repo(tmp_path)

    report = audit_skill_surfaces.build_report(repo_root, top=2)

    assert report.skill_count == 3
    assert report.reference_count == 2
    assert report.skill_lines_by_plugin["swiftasb-skills"] == 8
    assert [surface.relative_path for surface in report.largest_skills] == [
        "plugins/swiftasb-skills/skills/build-swiftui-app/SKILL.md",
        "plugins/productivity-skills/skills/maintain-project-readme/SKILL.md",
    ]
    assert len(report.duplicate_references) == 1
    assert len(report.duplicate_references[0].paths) == 2
    assert any(hit.phrase == "When the user explicitly requests subagents" for hit in report.phrase_hits)
    assert report.version_hits[0].path == "plugins/swiftasb-skills/skills/build-swiftui-app/SKILL.md"
    assert any(
        missing.path == "plugins/swiftasb-skills/skills/build-swiftui-app/SKILL.md"
        and missing.expected == "swiftasb:explain-swiftasb"
        for missing in report.missing_handoffs
    )


def test_json_report_is_serializable(tmp_path: Path) -> None:
    report = audit_skill_surfaces.build_report(make_repo(tmp_path), top=1)

    payload = audit_skill_surfaces.report_to_json(report)

    assert payload["skill_count"] == 3
    assert json.loads(json.dumps(payload))["reference_count"] == 2
    assert payload["largest_skills"] == [
        {
            "plugin": "swiftasb-skills",
            "path": "plugins/swiftasb-skills/skills/build-swiftui-app/SKILL.md",
            "line_count": 5,
        }
    ]


def test_markdown_report_includes_primary_sections(tmp_path: Path) -> None:
    report = audit_skill_surfaces.build_report(make_repo(tmp_path), top=1)

    markdown = audit_skill_surfaces.render_markdown(report)

    assert "# Socket Skill Surface Audit" in markdown
    assert "## Exact Duplicate References" in markdown
    assert "## Version-Sensitive Lines" in markdown
    assert "plugins/swiftasb-skills/skills/build-swiftui-app/SKILL.md:3" in markdown


def test_main_writes_markdown_report_to_output_path(tmp_path: Path) -> None:
    repo_root = make_repo(tmp_path / "repo")
    output_path = Path("docs/agents/skill-surface-audit.md")

    exit_code = audit_skill_surfaces.main(
        [
            "--repo-root",
            str(repo_root),
            "--top",
            "1",
            "--output",
            str(output_path),
        ]
    )

    rendered = (repo_root / output_path).read_text(encoding="utf-8")
    assert exit_code == 0
    assert rendered.startswith("# Socket Skill Surface Audit")
    assert "## Missing Expected Handoffs" in rendered


def test_main_writes_json_report_to_output_path(tmp_path: Path) -> None:
    repo_root = make_repo(tmp_path / "repo")
    output_path = tmp_path / "audit.json"

    exit_code = audit_skill_surfaces.main(
        [
            "--repo-root",
            str(repo_root),
            "--format",
            "json",
            "--output",
            str(output_path),
        ]
    )

    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert exit_code == 0
    assert payload["skill_count"] == 3
    assert payload["reference_count"] == 2


def test_swiftui_or_swiftdata_skills_include_direct_swiftdata_rule() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    skill_paths = sorted((repo_root / "plugins").glob("*/skills/*/SKILL.md"))
    swiftui_or_swiftdata_paths = [
        path
        for path in skill_paths
        if "SwiftUI" in path.read_text(encoding="utf-8")
        or "SwiftData" in path.read_text(encoding="utf-8")
    ]

    assert swiftui_or_swiftdata_paths
    missing_rule = [
        path.relative_to(repo_root).as_posix()
        for path in swiftui_or_swiftdata_paths
        if "## SwiftData And SwiftUI Rule" not in path.read_text(encoding="utf-8")
    ]

    assert missing_rule == []


def test_apple_swiftdata_snippets_reject_weak_query_only_guidance() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    stale_phrase = "Prefer `@Query` for view-driven SwiftData fetching"
    apple_skill_files = sorted((repo_root / "plugins" / "apple-dev-skills").glob("**/*.md"))
    stale_paths = [
        path.relative_to(repo_root).as_posix()
        for path in apple_skill_files
        if stale_phrase in path.read_text(encoding="utf-8")
    ]

    assert stale_paths == []
