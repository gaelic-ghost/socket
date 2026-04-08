#!/usr/bin/env python3
"""Two-pass docs maintenance workflow for skills-export repositories."""

from __future__ import annotations

import argparse
import fnmatch
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

PUBLIC_REPOS = {"productivity-skills", "python-skills"}
PRIVATE_REPOS = {"private-skills"}
BOOTSTRAP_REPOS = {"a11y-skills"}
DEFAULT_DOC_SCOPE = "readme"
EXACT_NO_FINDINGS = "No findings."

ROADMAP_REQUIRED_TOP_LEVEL = ["Vision", "Product Principles", "Milestone Progress"]
ROADMAP_MILESTONE_HEADING_RE = re.compile(r"^##\s+Milestone\s+(\d+)\s*:\s*(.+?)\s*$")
ROADMAP_PROGRESS_ENTRY_RE = re.compile(r"^\s*-\s+\[( |x)\]\s+Milestone\s+(\d+)\s*:\s*(.+?)\s*$")

SKILLS_SECTION_KEYS = [
    "active_skills",
    "repo_purpose",
    "limitations",
    "install",
    "layout",
    "tooling",
    "license",
]

SECTION_CANONICAL_HEADINGS = {
    "active_skills": "Exported Skills",
    "repo_purpose": "Honest Scope",
    "limitations": "Hard Codex Limitation",
    "install": "Install Guidance",
    "layout": "Repository Layout",
    "tooling": "Maintainer Tooling",
    "license": "License",
}

HEADING_ALIASES = {
    "active skills": "active_skills",
    "exported skills": "active_skills",
    "repo purpose": "repo_purpose",
    "honest scope": "repo_purpose",
    "hard codex limitation": "limitations",
    "install guidance": "install",
    "repository layout": "layout",
    "maintainer tooling": "tooling",
    "maintainer python tooling": "tooling",
    "license": "license",
}

FORBIDDEN_SNIPPETS = [
            ".agents/plugins/marketplace.json",
    ".claude-plugin/marketplace.json",
    "claude --plugin-dir",
    "~/.codex/plugins/",
    "repo-local packaged plugin",
    "bundled plugin",
    "Codex local plugin installs",
]

TOOLING_REQUIRED_SNIPPETS = [
    "uv sync --dev",
    "uv tool install ruff",
    "uv tool install mypy",
    "uv run --group dev pytest",
]


@dataclass
class Issue:
    issue_id: str
    category: str
    severity: str
    repo: str
    doc_file: str
    evidence: str
    recommended_fix: str
    auto_fixable: bool = False


@dataclass
class Fix:
    repo: str
    file: str
    rule: str
    status: str


def discover_repos(workspace: Path, repo_glob: str, excludes: Sequence[Path]) -> List[Path]:
    repos: List[Path] = []
    for child in sorted(workspace.iterdir()):
        if not child.is_dir():
            continue
        if any(child.resolve() == ex.resolve() for ex in excludes):
            continue
        if fnmatch.fnmatch(child.name, repo_glob):
            repos.append(child)
    return repos


def detect_profile(repo: Path) -> str:
    repo_name = repo.name
    if repo_name in PUBLIC_REPOS:
        return "public-curated"
    if repo_name in PRIVATE_REPOS:
        return "private-internal"
    if repo_name in BOOTSTRAP_REPOS:
        return "bootstrap"
    if (repo / "skills").is_dir():
        return "skills-maintainer"
    return "generic"


def find_skill_dirs(repo: Path) -> List[str]:
    skills: List[str] = []
    seen: set[str] = set()
    for pattern in ("*/SKILL.md", "skills/*/SKILL.md"):
        for p in sorted(repo.glob(pattern)):
            if p.parent.name in {"scripts", "references", "assets", "agents"}:
                continue
            if p.parent.name not in seen:
                skills.append(p.parent.name)
                seen.add(p.parent.name)
    return skills


def expected_section_keys(profile: str) -> List[str]:
    if profile == "skills-maintainer":
        return list(SKILLS_SECTION_KEYS)
    return list(SKILLS_SECTION_KEYS)


def heading_lines(text: str) -> List[Tuple[int, str]]:
    out: List[Tuple[int, str]] = []
    for idx, line in enumerate(text.splitlines(), start=1):
        if line.startswith("## "):
            out.append((idx, line.strip()))
    return out


def _normalize_heading(raw: str) -> str | None:
    text = raw.strip().lower()
    text = re.sub(r"^##\s+", "", text)
    return HEADING_ALIASES.get(text)


def check_sections(repo: Path, profile: str, readme_text: str) -> List[Issue]:
    issues: List[Issue] = []
    found = [_normalize_heading(line) for _, line in heading_lines(readme_text)]
    found_keys = [item for item in found if item is not None]
    for key in expected_section_keys(profile):
        if key not in found_keys:
            issues.append(
                Issue(
                    issue_id="readme-missing-section",
                    category="readme-structure",
                    severity="medium",
                    repo=repo.name,
                    doc_file=str(repo / "README.md"),
                    evidence=f"README is missing section `{SECTION_CANONICAL_HEADINGS[key]}`.",
                    recommended_fix=f"Add a `## {SECTION_CANONICAL_HEADINGS[key]}` section.",
                )
            )
    for snippet in TOOLING_REQUIRED_SNIPPETS:
        if snippet not in readme_text:
            issues.append(
                Issue(
                    issue_id="tooling-guidance-missing-snippet",
                    category="readme-content",
                    severity="medium",
                    repo=repo.name,
                    doc_file=str(repo / "README.md"),
                    evidence=f"README is missing maintainer tooling snippet `{snippet}`.",
                    recommended_fix="Keep maintainer tooling guidance explicit in the README.",
                )
            )
    for snippet in FORBIDDEN_SNIPPETS:
        if snippet in readme_text:
            issues.append(
                Issue(
                    issue_id="readme-forbidden-guidance",
                    category="readme-content",
                    severity="high",
                    repo=repo.name,
                    doc_file=str(repo / "README.md"),
                    evidence=f"README still contains forbidden guidance snippet `{snippet}`.",
                    recommended_fix="Remove nested-plugin, installer, and repo-marketplace guidance from the README.",
                )
            )
    return issues


def _parse_roadmap_titles(text: str) -> tuple[list[tuple[int, str]], list[tuple[int, str]]]:
    milestones: list[tuple[int, str]] = []
    progress: list[tuple[int, str]] = []
    for line in text.splitlines():
        milestone_match = ROADMAP_MILESTONE_HEADING_RE.match(line)
        if milestone_match:
            milestones.append((int(milestone_match.group(1)), milestone_match.group(2)))
        progress_match = ROADMAP_PROGRESS_ENTRY_RE.match(line)
        if progress_match:
            progress.append((int(progress_match.group(2)), progress_match.group(3)))
    return milestones, progress


def check_roadmap(repo: Path, roadmap_text: str) -> List[Issue]:
    issues: List[Issue] = []
    for heading in ROADMAP_REQUIRED_TOP_LEVEL:
        if f"## {heading}" not in roadmap_text:
            issues.append(
                Issue(
                    issue_id="roadmap-missing-top-level",
                    category="roadmap-structure",
                    severity="high",
                    repo=repo.name,
                    doc_file=str(repo / "ROADMAP.md"),
                    evidence=f"ROADMAP is missing top-level section `{heading}`.",
                    recommended_fix=f"Add the `## {heading}` section.",
                )
            )
    milestones, progress = _parse_roadmap_titles(roadmap_text)
    if milestones:
        milestone_numbers = [num for num, _ in milestones]
        expected_numbers = list(range(min(milestone_numbers), max(milestone_numbers) + 1))
        if milestone_numbers != expected_numbers:
            issues.append(
                Issue(
                    issue_id="roadmap-non-sequential-milestones",
                    category="roadmap-structure",
                    severity="medium",
                    repo=repo.name,
                    doc_file=str(repo / "ROADMAP.md"),
                    evidence="ROADMAP milestone numbers are not sequential.",
                    recommended_fix="Renumber milestone sections so they are sequential.",
                )
            )
        if len(set(milestone_numbers)) != len(milestone_numbers):
            issues.append(
                Issue(
                    issue_id="roadmap-duplicate-milestones",
                    category="roadmap-structure",
                    severity="high",
                    repo=repo.name,
                    doc_file=str(repo / "ROADMAP.md"),
                    evidence="ROADMAP contains duplicate milestone numbers.",
                    recommended_fix="Remove duplicate milestone numbers.",
                )
            )
    if progress and milestones and progress != milestones:
        issues.append(
            Issue(
                issue_id="roadmap-progress-mismatch",
                category="roadmap-structure",
                severity="medium",
                repo=repo.name,
                doc_file=str(repo / "ROADMAP.md"),
                evidence="Milestone Progress entries do not match milestone section titles.",
                recommended_fix="Keep the Milestone Progress block aligned with milestone headings.",
            )
        )
    for snippet in FORBIDDEN_SNIPPETS:
        if snippet in roadmap_text:
            issues.append(
                Issue(
                    issue_id="roadmap-forbidden-guidance",
                    category="roadmap-content",
                    severity="high",
                    repo=repo.name,
                    doc_file=str(repo / "ROADMAP.md"),
                    evidence=f"ROADMAP still contains forbidden guidance snippet `{snippet}`.",
                    recommended_fix="Remove nested-plugin, installer, and repo-marketplace guidance from the roadmap.",
                )
            )
    return issues


def check_cross_doc(repo: Path, readme_text: str, roadmap_text: str) -> List[Issue]:
    issues: List[Issue] = []
    skill_names = set(find_skill_dirs(repo))
    if skill_names:
        readme_skills = {name for name in skill_names if f"`{name}`" in readme_text}
        if readme_skills != skill_names:
            missing = ", ".join(sorted(skill_names - readme_skills))
            issues.append(
                Issue(
                    issue_id="cross-doc-missing-skill-mention",
                    category="cross-doc-violation",
                    severity="medium",
                    repo=repo.name,
                    doc_file=str(repo / "README.md"),
                    evidence=f"README does not mention all exported skills. Missing: {missing}",
                    recommended_fix="Keep the README exported-skills list aligned with the live `skills/` directory.",
                )
            )
    if "proper repo-private plugin scoping" not in readme_text and "too restricted to provide proper repo-private plugin scoping" not in readme_text:
        issues.append(
            Issue(
                issue_id="cross-doc-missing-codex-limit-warning",
                category="cross-doc-violation",
                severity="high",
                repo=repo.name,
                doc_file=str(repo / "README.md"),
                evidence="README does not state the hard Codex scoping limitation plainly enough.",
                recommended_fix="Keep the Codex limitation warning explicit in the README.",
            )
        )
    if any(snippet in readme_text for snippet in FORBIDDEN_SNIPPETS) or any(snippet in roadmap_text for snippet in FORBIDDEN_SNIPPETS):
        issues.append(
            Issue(
                issue_id="cross-doc-forbidden-contract",
                category="cross-doc-violation",
                severity="high",
                repo=repo.name,
                doc_file=str(repo),
                evidence="Repo docs still describe forbidden nested-plugin or installer contract details.",
                recommended_fix="Remove nested-plugin, installer, and repo-marketplace guidance from repo docs.",
            )
        )
    return issues


def summarize_markdown(report: Dict[str, object]) -> str:
    lines: List[str] = []
    rc = report["run_context"]
    lines.append("## Run Context")
    lines.append(f"- Timestamp: {rc['timestamp_utc']}")
    lines.append(f"- Workspace: {rc['workspace']}")
    lines.append(f"- Repo glob: {rc['repo_glob']}")
    lines.append(f"- Doc scope: {rc['doc_scope']}")
    lines.append(f"- Apply fixes: {rc['apply_fixes']}")
    lines.append("")
    for title, key in (("README Findings", "readme_findings"), ("ROADMAP Findings", "roadmap_findings"), ("Cross-Doc Findings", "cross_doc_findings")):
        lines.append(f"## {title}")
        items = report[key]
        if not items:
            lines.append("- None")
        else:
            for item in items:
                lines.append(f"- {item['doc_file']}: {item['evidence']}")
        lines.append("")
    lines.append("## Fixes Applied")
    if not report["fixes_applied"]:
        lines.append("- None")
    else:
        for item in report["fixes_applied"]:
            lines.append(f"- [{item['status']}] {item['repo']} -> {item['file']} ({item['rule']})")
    return "\n".join(lines).strip()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--repo-glob", required=True)
    parser.add_argument("--doc-scope", choices=("readme", "roadmap", "all"), default=DEFAULT_DOC_SCOPE)
    parser.add_argument("--apply-fixes", action="store_true")
    parser.add_argument("--print-json", action="store_true")
    parser.add_argument("--print-md", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    workspace = Path(args.workspace).resolve()
    repos = discover_repos(workspace, args.repo_glob, [])
    if not repos:
        print(json.dumps({"error": "No repositories matched the requested glob."}, indent=2))
        return 1
    repo = repos[0]
    readme_text = (repo / "README.md").read_text(encoding="utf-8") if (repo / "README.md").exists() else ""
    roadmap_text = (repo / "ROADMAP.md").read_text(encoding="utf-8") if (repo / "ROADMAP.md").exists() else ""
    profile = detect_profile(repo)
    readme_findings = check_sections(repo, profile, readme_text) if args.doc_scope in {"readme", "all"} else []
    roadmap_findings = check_roadmap(repo, roadmap_text) if args.doc_scope in {"roadmap", "all"} else []
    cross_doc_findings = check_cross_doc(repo, readme_text, roadmap_text) if args.doc_scope == "all" else []
    report = {
        "run_context": {
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "workspace": str(workspace),
            "repo_glob": args.repo_glob,
            "doc_scope": args.doc_scope,
            "apply_fixes": args.apply_fixes,
        },
        "discovery": {"repos": [str(repo)]},
        "readme_findings": [issue.__dict__ for issue in readme_findings],
        "roadmap_findings": [issue.__dict__ for issue in roadmap_findings],
        "cross_doc_findings": [issue.__dict__ for issue in cross_doc_findings],
        "fixes_applied": [],
        "errors": [],
    }
    if args.print_md and not any((readme_findings, roadmap_findings, cross_doc_findings)):
        print(EXACT_NO_FINDINGS)
        return 0
    if args.print_md:
        print(summarize_markdown(report))
    else:
        print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
