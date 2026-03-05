#!/usr/bin/env python3
"""Two-pass README alignment maintainer for *-skills repositories."""

from __future__ import annotations

import argparse
import fnmatch
import json
import os
import re
import shlex
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

PUBLIC_REPOS = {"apple-dev-skills", "productivity-skills", "python-skills"}
PRIVATE_REPOS = {"private-skills"}
BOOTSTRAP_REPOS = {"a11y-skills"}

EXPECTED_OWNER = "gaelic-ghost"

CORE_SECTION_KEYS = [
    "what",
    "guide",
    "customization_matrix",
    "quickstart",
    "individual",
    "update_skills",
    "more_resources",
    "layout",
    "notes",
    "keywords",
    "license",
]

SECTION_CANONICAL_HEADINGS = {
    "what": "What These Agent Skills Help With",
    "guide": "Skill Guide (When To Use What)",
    "customization_matrix": "Customization Workflow Matrix",
    "quickstart": "Quick Start (Vercel Skills CLI)",
    "individual": "Install individually by Skill or Skill Pack",
    "update_skills": "Update Skills",
    "more_resources": "More resources for similar Skills",
    "layout": "Repository Layout",
    "notes": "Notes",
    "license": "License",
    "keywords": "Keywords",
}

SECTION_PATTERNS = {
    "what": r"^##\s+What These Agent Skills Help With\s*$",
    "guide": r"^##\s+Skill Guide \(When To Use What\)\s*$",
    "customization_matrix": r"^##\s+Customization Workflow Matrix\s*$",
    "quickstart": r"^##\s+Quick Start \(Vercel Skills CLI\)\s*$",
    "individual": r"^##\s+Install individually by Skill or Skill Pack\s*$",
    "update_skills": r"^##\s+Update Skills\s*$",
    "more_resources": r"^##\s+More resources for similar Skills\s*$",
    "layout": r"^##\s+Repository Layout\s*$",
    "notes": r"^##\s+Notes\s*$",
    "license": r"^##\s+License\s*$",
    "keywords": r"^##\s+Keywords\s*$",
}

MORE_RESOURCES_SUBSECTION_KEYS = ["find_cli", "find_skill"]

MORE_RESOURCES_SUBSECTION_CANONICAL_HEADINGS = {
    "find_cli": "Find Skills like these with the `skills` CLI by Vercel — [vercel-labs/skills](https://github.com/vercel-labs/skills)",
    "find_skill": "Find Skills like these with the `Find Skills` Agent Skill by Vercel — [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills)",
}

MORE_RESOURCES_SUBSECTION_PATTERNS = {
    "find_cli": r"^###\s+Find Skills like these with.*`?skills`?\s+CLI",
    "find_skill": r"^###\s+Find Skills like these with.*`?Find Skills`?.*(?:Agent\s+Skill|Skill)",
}

MORE_RESOURCES_SUBSECTION_TEMPLATES = {
    "find_cli": (
        "```bash\n"
        "npx skills find \"xcode mcp\"\n"
        "npx skills find \"swift package workflow\"\n"
        "npx skills find \"dash docset apple docs\"\n"
        "```\n"
    ),
    "find_skill": (
        "```bash\n"
        "# `Find Skills` is a part of Vercel's `agent-skills` repo\n"
        "npx skills add vercel-labs/agent-skills --skill find-skills\n"
        "```\n"
    ),
}

LEGACY_MORE_RESOURCES_TOP_LEVEL_PATTERNS = {
    "find_cli": r"^##\s+Find Skills like these with.*`?skills`?\s+CLI",
    "find_skill": r"^##\s+Find Skills like these with.*`?Find Skills`?",
}

MORE_RESOURCES_ANCHOR_LINE = 'Then ask your Agent for help finding a skill for "" or ""'

HEADING_ALIASES = {
    "how to add (skills cli)": "quickstart",
    "how to add (vercel skills cli)": "quickstart",
    "how to add with skills cli": "quickstart",
    "quickstart (skills cli)": "quickstart",
    "customization workflow matrix": "customization_matrix",
    "included skills": "guide",
    "included skill": "guide",
    "skills included": "guide",
    "install by skill": "individual",
    "install individually by skill": "individual",
    "install individually by skills": "individual",
    "install individually by skill or skill pack": "individual",
    "search keywords": "keywords",
    "keywords": "keywords",
    "update skills": "update_skills",
    "more resources for similar skills": "more_resources",
}

HIGH_CONFIDENCE_HEADING_PATTERNS = [
    ("customization_matrix", re.compile(r"^customization\s+workflow\s+matrix$", re.IGNORECASE)),
    ("quickstart", re.compile(r"^quick\s*start.*skills\s*cli$", re.IGNORECASE)),
    ("quickstart", re.compile(r"^how\s+to\s+add.*skills\s*cli$", re.IGNORECASE)),
    ("individual", re.compile(r"^install\s+(?:individually|individual)\s+by\s+skill\s+or\s+skill\s+pack$", re.IGNORECASE)),
    ("individual", re.compile(r"^install\s+(?:individually|individual)\s+by\s+skills?$", re.IGNORECASE)),
    ("individual", re.compile(r"^install\s+by\s+skills?$", re.IGNORECASE)),
    ("keywords", re.compile(r"^(?:search\s+)?keywords$", re.IGNORECASE)),
    ("update_skills", re.compile(r"^update\s+skills$", re.IGNORECASE)),
    ("guide", re.compile(r"^included\s+skills?$", re.IGNORECASE)),
    ("more_resources", re.compile(r"^more\s+resources.*similar\s+skills$", re.IGNORECASE)),
]

MORE_RESOURCES_SUBSECTION_ALIASES = {
    "find skills like these with find skills agent skill by vercel — [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills)": "find_skill",
    "find skills like these with find skills skill by vercel — [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills)": "find_skill",
    "find skills like these with the find skills by vercel — [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills)": "find_skill",
}

MORE_RESOURCES_SUBSECTION_HIGH_CONFIDENCE_PATTERNS = [
    ("find_cli", re.compile(r"^find\s+skills?.*skills\s*cli.*$", re.IGNORECASE)),
    ("find_skill", re.compile(r"^find\s+skills?.*find\s+skills.*(?:agent\s+skill|skill).*$", re.IGNORECASE)),
]

SECTION_TEMPLATES = {
    "what": "## What These Agent Skills Help With\n\nDescribe the audience and the workflows this repository improves.\n",
    "guide": "## Skill Guide (When To Use What)\n\n- `<skill-name>`\n  - Use when ...\n  - Helps by ...\n",
    "customization_matrix": (
        "## Customization Workflow Matrix\n\n"
        "| Skill | Chat Customization Flow (SKILL.md) | Durable Config (`template` + persisted `customization.yaml`) | Automation Knobs | README Migration Status |\n"
        "| --- | --- | --- | --- | --- |\n"
        "| `<skill-name>` | Yes | Yes | No | README removed |\n"
    ),
    "quickstart": (
        "## Quick Start (Vercel Skills CLI)\n\n"
        "Use the Vercel `skills` CLI against this repository to install any skill directory you want to use. "
        "Or install them all conveniently with one command.\n\n"
        "```bash\n"
        "# Install your choice of skill(s) interactively via the Vercel `skills` CLI\n"
        "# Using `npx` fetches `skills` without installing it on your machine\n"
        "npx skills add gaelic-ghost/{repo}\n"
        "```\n"
        "\n"
        "The CLI will prompt you to choose which skill(s) to install from this repo.\n\n"
        "```bash\n"
        "# Install all skills from this repo non-interactively\n"
        "npx skills add gaelic-ghost/{repo} --all\n"
        "```\n"
    ),
    "individual": (
        "## Install individually by Skill or Skill Pack\n\n"
        "```bash\n"
        "npx skills add gaelic-ghost/{repo} --skill <skill-name>\n"
        "```\n"
    ),
    "update_skills": (
        "## Update Skills\n\n"
        "```bash\n"
        "# Check for available updates to installed Skills\n"
        "npx skills check\n"
        "# Update installed Skills\n"
        "npx skills update\n"
        "```\n"
    ),
    "more_resources": (
        "## More resources for similar Skills\n\n"
        "### Find Skills like these with the `skills` CLI by Vercel — "
        "[vercel-labs/skills](https://github.com/vercel-labs/skills)\n\n"
        "```bash\n"
        "npx skills find \"xcode mcp\"\n"
        "npx skills find \"swift package workflow\"\n"
        "npx skills find \"dash docset apple docs\"\n"
        "```\n\n"
        "### Find Skills like these with the `Find Skills` Agent Skill by Vercel — "
        "[vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills)\n\n"
        "```bash\n"
        "# `Find Skills` is a part of Vercel's `agent-skills` repo\n"
        "npx skills add vercel-labs/agent-skills --skill find-skills\n"
        "```\n\n"
        "Then ask your Agent for help finding a skill for \"\" or \"\"\n\n"
        "### Leaderboard\n\n"
        "- Skills catalog: [skills.sh](https://skills.sh/)\n"
    ),
    "layout": "## Repository Layout\n\n```text\n.\n├── README.md\n└── <skill-directories>/\n```\n",
    "notes": "## Notes\n\n- Keep README commands and skill inventory synchronized.\n",
    "license": "## License\n\nSee [LICENSE](./LICENSE).\n",
    "keywords": "## Keywords\n\nCodex skills, automation, workflows, documentation alignment.\n",
}


@dataclass
class Issue:
    issue_id: str
    category: str
    severity: str
    repo: str
    doc_file: str
    evidence: str
    recommended_fix: str
    auto_fixable: bool
    fixed: bool = False
    normalized_from: Optional[str] = None
    normalized_to: Optional[str] = None
    normalization_method: Optional[str] = None

    def to_dict(self) -> Dict[str, object]:
        payload: Dict[str, object] = {
            "issue_id": self.issue_id,
            "category": self.category,
            "severity": self.severity,
            "repo": self.repo,
            "doc_file": self.doc_file,
            "evidence": self.evidence,
            "recommended_fix": self.recommended_fix,
            "auto_fixable": self.auto_fixable,
            "fixed": self.fixed,
        }
        if self.normalized_from is not None:
            payload["normalized_from"] = self.normalized_from
        if self.normalized_to is not None:
            payload["normalized_to"] = self.normalized_to
        if self.normalization_method is not None:
            payload["normalization_method"] = self.normalization_method
        return payload


@dataclass
class HeadingNormalizationEvent:
    line: int
    section_key: str
    original_heading: str
    normalized_heading: str
    normalization_method: str

    def to_dict(self) -> Dict[str, object]:
        return {
            "line": self.line,
            "section_key": self.section_key,
            "original_heading": self.original_heading,
            "normalized_heading": self.normalized_heading,
            "normalization_method": self.normalization_method,
        }


@dataclass
class SkillsAddCommand:
    raw_line: str
    normalized_line: str
    owner: Optional[str]
    repo: Optional[str]
    legacy_skill: Optional[str]
    option_skill: Optional[str]
    has_all: bool
    unknown_options: List[str]
    extra_positionals: List[str]
    parse_error: Optional[str]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit and optionally align README standards for *-skills repos")
    parser.add_argument("--workspace", required=True, help="Workspace root")
    parser.add_argument("--repo-glob", default="*-skills", help="Repo directory glob")
    parser.add_argument("--exclude", action="append", default=[], help="Path to exclude (repeatable)")
    parser.add_argument("--apply-fixes", action="store_true", help="Apply bounded README fixes")
    parser.add_argument("--json-out", help="Write JSON report path")
    parser.add_argument("--md-out", help="Write Markdown report path")
    parser.add_argument("--print-json", action="store_true", help="Print JSON report")
    parser.add_argument("--print-md", action="store_true", help="Print Markdown report")
    parser.add_argument("--fail-on-issues", action="store_true", help="Exit non-zero when unresolved issues remain")
    return parser.parse_args()


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="ignore")


def write_text(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def read_excludes(raw_excludes: Sequence[str]) -> List[Path]:
    excludes: List[Path] = []
    seen: set[str] = set()
    for raw in raw_excludes:
        p = Path(raw).expanduser().resolve()
        key = str(p)
        if key not in seen:
            excludes.append(p)
            seen.add(key)
    return excludes


def is_excluded(path: Path, excludes: Sequence[Path]) -> bool:
    resolved = path.resolve()
    for ex in excludes:
        try:
            resolved.relative_to(ex)
            return True
        except ValueError:
            continue
    return False


def discover_repos(workspace: Path, repo_glob: str, excludes: Sequence[Path]) -> List[Path]:
    repos: List[Path] = []
    for child in sorted(workspace.iterdir()):
        if not child.is_dir():
            continue
        if is_excluded(child, excludes):
            continue
        if fnmatch.fnmatch(child.name, repo_glob):
            repos.append(child)
    return repos


def detect_profile(repo_name: str) -> str:
    if repo_name in PUBLIC_REPOS:
        return "public-curated"
    if repo_name in PRIVATE_REPOS:
        return "private-internal"
    if repo_name in BOOTSTRAP_REPOS:
        return "bootstrap"
    return "generic"


def find_skill_dirs(repo: Path) -> List[str]:
    skills: List[str] = []
    for p in sorted(repo.glob("*/SKILL.md")):
        if p.parent.name not in {"scripts", "references", "assets", "agents"}:
            skills.append(p.parent.name)
    return skills


def heading_lines(text: str) -> List[Tuple[int, str]]:
    out: List[Tuple[int, str]] = []
    for idx, line in enumerate(text.splitlines(), start=1):
        if line.startswith("## "):
            out.append((idx, line.strip()))
    return out


def canonical_heading_line(section_key: str) -> str:
    return f"## {SECTION_CANONICAL_HEADINGS[section_key]}"


def expected_section_keys(profile: str) -> List[str]:
    if profile == "public-curated":
        # Public READMEs include customization matrix and place keywords before license.
        return [
            "what",
            "guide",
            "customization_matrix",
            "quickstart",
            "individual",
            "update_skills",
            "more_resources",
            "layout",
            "notes",
            "keywords",
            "license",
        ]
    return list(CORE_SECTION_KEYS)


def heading_body(line: str) -> str:
    if line.startswith("### "):
        return line[4:].strip()
    return line[3:].strip() if line.startswith("## ") else line.strip()


def normalize_heading_lookup_key(value: str) -> str:
    key = re.sub(r"\s+", " ", value.strip().lower())
    key = key.replace("`", "")
    return key


def canonical_subheading_line(section_key: str) -> str:
    return f"### {MORE_RESOURCES_SUBSECTION_CANONICAL_HEADINGS[section_key]}"


def resolve_section_key_for_heading(line: str, allowed_keys: Sequence[str]) -> Tuple[Optional[str], Optional[str]]:
    body = heading_body(line)
    normalized_body = normalize_heading_lookup_key(body)
    allowed = set(allowed_keys)

    # Alias mappings are deterministic and preferred over pattern guesses.
    alias_key = HEADING_ALIASES.get(normalized_body)
    if alias_key and alias_key in allowed:
        return alias_key, "alias"

    matched_keys: List[str] = []
    for key, rx in HIGH_CONFIDENCE_HEADING_PATTERNS:
        if key in allowed and rx.search(normalized_body):
            matched_keys.append(key)
    if len(set(matched_keys)) == 1:
        return matched_keys[0], "pattern"
    if len(set(matched_keys)) > 1:
        return None, None

    return None, None


def resolve_more_resources_subsection_key_for_heading(line: str, allowed_keys: Sequence[str]) -> Tuple[Optional[str], Optional[str]]:
    body = heading_body(line)
    normalized_body = normalize_heading_lookup_key(body)
    allowed = set(allowed_keys)

    alias_key = MORE_RESOURCES_SUBSECTION_ALIASES.get(normalized_body)
    if alias_key and alias_key in allowed:
        return alias_key, "alias"

    matched_keys: List[str] = []
    for key, rx in MORE_RESOURCES_SUBSECTION_HIGH_CONFIDENCE_PATTERNS:
        if key in allowed and rx.search(normalized_body):
            matched_keys.append(key)
    if len(set(matched_keys)) == 1:
        return matched_keys[0], "pattern"
    if len(set(matched_keys)) > 1:
        return None, None

    return None, None


def resolve_legacy_more_resources_top_level_key(line: str) -> Optional[str]:
    if not line.startswith("## "):
        return None
    for key, pattern in LEGACY_MORE_RESOURCES_TOP_LEVEL_PATTERNS.items():
        if re.search(pattern, line, flags=re.IGNORECASE):
            return key
    return None


def find_section_line_range(lines: Sequence[str], section_pattern: str) -> Optional[Tuple[int, int]]:
    section_rx = re.compile(section_pattern, re.IGNORECASE)
    start_idx: Optional[int] = None
    for idx, line in enumerate(lines):
        if section_rx.search(line.strip()):
            start_idx = idx
            break
    if start_idx is None:
        return None
    end_idx = len(lines)
    for idx in range(start_idx + 1, len(lines)):
        if lines[idx].startswith("## "):
            end_idx = idx
            break
    return start_idx, end_idx


def check_more_resources_subsections(repo: Path, profile: str, lines: Sequence[str]) -> List[Issue]:
    if profile != "public-curated":
        return []

    issues: List[Issue] = []
    section_range = find_section_line_range(lines, SECTION_PATTERNS["more_resources"])
    if section_range is None:
        return issues

    start_idx, end_idx = section_range
    section_subheadings: List[Tuple[int, str]] = []
    for idx in range(start_idx + 1, end_idx):
        stripped = lines[idx].strip()
        if stripped.startswith("### "):
            section_subheadings.append((idx + 1, stripped))

    required_keys = list(MORE_RESOURCES_SUBSECTION_KEYS)
    for key in required_keys:
        pattern = MORE_RESOURCES_SUBSECTION_PATTERNS[key]
        found = any(re.search(pattern, heading, flags=re.IGNORECASE) for _, heading in section_subheadings)
        if not found:
            issues.append(
                Issue(
                    issue_id=f"more-resources-subsection-missing-{key}",
                    category="schema-violation",
                    severity="medium",
                    repo=repo.name,
                    doc_file=str(repo / "README.md"),
                    evidence=f"Missing required subsection `{key}` under `more_resources`.",
                    recommended_fix=f"Add required `###` subsection `{key}` under `## More resources for similar Skills`.",
                    auto_fixable=True,
                )
            )

    for lineno, line in section_subheadings:
        key, method = resolve_more_resources_subsection_key_for_heading(line, required_keys)
        if not key or not method:
            continue
        canonical = canonical_subheading_line(key)
        if line == canonical:
            continue
        issues.append(
            Issue(
                issue_id="more-resources-subsection-misnamed",
                category="schema-violation",
                severity="low",
                repo=repo.name,
                doc_file=str(repo / "README.md"),
                evidence=f"Subheading at line {lineno} should be `{canonical}`.",
                recommended_fix="Rename subsection heading to the canonical discoverability title.",
                auto_fixable=True,
                normalized_from=line,
                normalized_to=canonical,
                normalization_method=method,
            )
        )

    for key in required_keys:
        pattern = MORE_RESOURCES_SUBSECTION_PATTERNS[key]
        matches = [heading for _lineno, heading in section_subheadings if re.search(pattern, heading, flags=re.IGNORECASE)]
        if len(matches) > 1:
            issues.append(
                Issue(
                    issue_id="more-resources-subsection-duplicate",
                    category="schema-violation",
                    severity="low",
                    repo=repo.name,
                    doc_file=str(repo / "README.md"),
                    evidence=f"Multiple subsections match `{key}` under `more_resources`.",
                    recommended_fix="Consolidate duplicate discoverability subsections under one canonical heading.",
                    auto_fixable=False,
                )
            )

    anchor_idx: Optional[int] = None
    for idx in range(start_idx + 1, end_idx):
        if lines[idx].strip() == MORE_RESOURCES_ANCHOR_LINE:
            anchor_idx = idx
            break
    if anchor_idx is None:
        issues.append(
            Issue(
                issue_id="more-resources-anchor-missing",
                category="schema-violation",
                severity="medium",
                repo=repo.name,
                doc_file=str(repo / "README.md"),
                evidence=f"Missing required anchor line under `more_resources`: {MORE_RESOURCES_ANCHOR_LINE}",
                recommended_fix=f"Add this exact line before optional extra `###` subsections: {MORE_RESOURCES_ANCHOR_LINE}",
                auto_fixable=False,
            )
        )
        return issues

    for idx in range(start_idx + 1, anchor_idx):
        stripped = lines[idx].strip()
        if not stripped.startswith("### "):
            continue
        key, _method = resolve_more_resources_subsection_key_for_heading(stripped, required_keys)
        if key:
            continue
        issues.append(
            Issue(
                issue_id="more-resources-extra-subsection-before-anchor",
                category="schema-violation",
                severity="low",
                repo=repo.name,
                doc_file=str(repo / "README.md"),
                evidence=f"Optional subsection `{stripped}` appears before the anchor line.",
                recommended_fix=f"Move optional `###` subsections below this line: {MORE_RESOURCES_ANCHOR_LINE}",
                auto_fixable=False,
            )
        )

    return issues


def find_matching_heading_indices(headings: List[Tuple[int, str]], pattern: str) -> List[int]:
    rx = re.compile(pattern, re.IGNORECASE)
    matches: List[int] = []
    for idx, (_lineno, heading) in enumerate(headings):
        if rx.search(heading):
            matches.append(idx)
    return matches


def first_match_heading_index(headings: List[Tuple[int, str]], pattern: str) -> Optional[int]:
    rx = re.compile(pattern, re.IGNORECASE)
    for idx, (_lineno, heading) in enumerate(headings):
        if rx.search(heading):
            return idx
    return None


def check_sections(repo: Path, profile: str, text: str) -> List[Issue]:
    issues: List[Issue] = []
    lines = text.splitlines()

    first_non_empty = next((line.strip() for line in lines if line.strip()), "")
    if not first_non_empty.startswith("# "):
        issues.append(
            Issue(
                issue_id="missing-title",
                category="schema-violation",
                severity="high",
                repo=repo.name,
                doc_file=str(repo / "README.md"),
                evidence="README is missing an H1 title line.",
                recommended_fix="Add a top-level `# <repo-name>` heading.",
                auto_fixable=False,
            )
        )

    purpose_line = ""
    if first_non_empty.startswith("# "):
        try:
            title_idx = next(i for i, line in enumerate(lines) if line.strip() == first_non_empty)
            for line in lines[title_idx + 1 :]:
                stripped = line.strip()
                if not stripped:
                    continue
                purpose_line = stripped
                break
        except StopIteration:
            purpose_line = ""
    if not purpose_line or purpose_line.startswith("#"):
        issues.append(
            Issue(
                issue_id="missing-purpose-summary",
                category="schema-violation",
                severity="medium",
                repo=repo.name,
                doc_file=str(repo / "README.md"),
                evidence="README is missing a one-line purpose summary below the title.",
                recommended_fix="Add a concise one-line value proposition below the H1.",
                auto_fixable=False,
            )
        )

    headings = heading_lines(text)
    all_lines = text.splitlines()

    patterns = [(key, SECTION_PATTERNS[key]) for key in expected_section_keys(profile)]

    matched: List[Tuple[str, int]] = []
    for key, pattern in patterns:
        idx = first_match_heading_index(headings, pattern)
        if idx is None:
            issues.append(
                Issue(
                    issue_id=f"section-missing-{key}",
                    category="schema-violation",
                    severity="medium",
                    repo=repo.name,
                    doc_file=str(repo / "README.md"),
                    evidence=f"Missing required section: {key}",
                    recommended_fix=f"Add required section `{key}`.",
                    auto_fixable=True,
                )
            )
        else:
            matched.append((key, idx))

    for lineno, line in headings:
        key, method = resolve_section_key_for_heading(line, [k for k, _ in patterns])
        if not key or not method:
            continue
        canonical = canonical_heading_line(key)
        if line == canonical:
            continue
        issues.append(
            Issue(
                issue_id="section-misnamed",
                category="schema-violation",
                severity="low",
                repo=repo.name,
                doc_file=str(repo / "README.md"),
                evidence=f"Heading at line {lineno} should be `{canonical}`.",
                recommended_fix="Rename heading to the canonical section title.",
                auto_fixable=True,
                normalized_from=line,
                normalized_to=canonical,
                normalization_method=method,
            )
        )

    for key, pattern in patterns:
        matches = find_matching_heading_indices(headings, pattern)
        if len(matches) > 1:
            issues.append(
                Issue(
                    issue_id="duplicate-canonical-section",
                    category="schema-violation",
                    severity="low",
                    repo=repo.name,
                    doc_file=str(repo / "README.md"),
                    evidence=f"Multiple headings match required section `{key}`.",
                    recommended_fix="Manually consolidate duplicated section content under one canonical heading.",
                    auto_fixable=False,
                )
            )

    ordered_idxs = [idx for _, idx in matched]
    if ordered_idxs != sorted(ordered_idxs):
        issues.append(
            Issue(
                issue_id="section-order",
                category="schema-violation",
                severity="low",
                repo=repo.name,
                doc_file=str(repo / "README.md"),
                evidence="Required sections are out of expected order.",
                recommended_fix="Reorder headings to canonical section schema.",
                auto_fixable=False,
            )
        )

    issues.extend(check_more_resources_subsections(repo, profile, all_lines))

    return issues


def find_todo_issues(repo: Path, text: str) -> List[Issue]:
    issues: List[Issue] = []
    if re.search(r"\b(TODO|TBD|todo)\b", text):
        issues.append(
            Issue(
                issue_id="todo-placeholder",
                category="schema-violation",
                severity="medium",
                repo=repo.name,
                doc_file=str(repo / "README.md"),
                evidence="README contains TODO/TBD placeholders.",
                recommended_fix="Replace placeholders with concrete content.",
                auto_fixable=False,
            )
        )
    return issues


def parse_skills_add_command_line(line: str) -> Optional[SkillsAddCommand]:
    stripped = line.strip()
    if not re.match(r"^npx\s+skills\s+add\b", stripped):
        return None

    try:
        tokens = shlex.split(stripped)
    except ValueError as exc:
        return SkillsAddCommand(
            raw_line=stripped,
            normalized_line=stripped,
            owner=None,
            repo=None,
            legacy_skill=None,
            option_skill=None,
            has_all=False,
            unknown_options=[],
            extra_positionals=[],
            parse_error=f"could not parse command: {exc}",
        )

    if len(tokens) < 3 or tokens[0] != "npx" or tokens[1] != "skills" or tokens[2] != "add":
        return None

    args = tokens[3:]
    owner: Optional[str] = None
    repo: Optional[str] = None
    legacy_skill: Optional[str] = None
    option_skill: Optional[str] = None
    has_all = False
    unknown_options: List[str] = []
    extra_positionals: List[str] = []
    parse_error: Optional[str] = None

    target_index: Optional[int] = None
    for idx, arg in enumerate(args):
        if not arg.startswith("-"):
            target_index = idx
            break

    if target_index is None:
        parse_error = "missing target `<owner/repo>`."
        option_tokens = args
    else:
        target = args[target_index]
        m = re.match(r"^([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)(?:@([A-Za-z0-9_.-]+))?$", target)
        if m:
            owner, repo, legacy_skill = m.group(1), m.group(2), m.group(3)
        else:
            parse_error = f"invalid target `{target}`."
        option_tokens = args[target_index + 1 :]

    idx = 0
    while idx < len(option_tokens):
        tok = option_tokens[idx]
        if tok == "--all":
            has_all = True
            idx += 1
            continue
        if tok == "--skill":
            if idx + 1 >= len(option_tokens) or option_tokens[idx + 1].startswith("-"):
                parse_error = parse_error or "missing value for `--skill`."
                idx += 1
                continue
            option_skill = option_tokens[idx + 1]
            idx += 2
            continue
        if tok.startswith("--skill="):
            value = tok.split("=", 1)[1].strip()
            if value:
                option_skill = value
            else:
                parse_error = parse_error or "missing value for `--skill`."
            idx += 1
            continue
        if tok.startswith("-"):
            unknown_options.append(tok)
        else:
            extra_positionals.append(tok)
        idx += 1

    return SkillsAddCommand(
        raw_line=stripped,
        normalized_line=" ".join(tokens),
        owner=owner,
        repo=repo,
        legacy_skill=legacy_skill,
        option_skill=option_skill,
        has_all=has_all,
        unknown_options=unknown_options,
        extra_positionals=extra_positionals,
        parse_error=parse_error,
    )


def parse_skills_add_commands(text: str) -> List[SkillsAddCommand]:
    out: List[SkillsAddCommand] = []
    for line in text.splitlines():
        parsed = parse_skills_add_command_line(line)
        if parsed is not None:
            out.append(parsed)
    return out


def check_commands(repo: Path, profile: str, text: str, skill_dirs: List[str]) -> List[Issue]:
    issues: List[Issue] = []
    commands = parse_skills_add_commands(text)
    expected_repo = repo.name

    has_own_base = False
    own_cmd_counts: Dict[str, int] = {}

    for command in commands:
        if command.owner == EXPECTED_OWNER and command.repo == expected_repo:
            own_cmd_counts[command.normalized_line] = own_cmd_counts.get(command.normalized_line, 0) + 1

            if command.legacy_skill:
                issues.append(
                    Issue(
                        issue_id="legacy-skills-add-syntax",
                        category="command-integrity",
                        severity="medium",
                        repo=repo.name,
                        doc_file=str(repo / "README.md"),
                        evidence=f"Legacy `@skill` syntax used: `{command.raw_line}`.",
                        recommended_fix="Use `npx skills add <owner/repo> --skill <skill-name>`.",
                        auto_fixable=True,
                    )
                )

            if command.parse_error:
                issues.append(
                    Issue(
                        issue_id="invalid-skills-add-command",
                        category="command-integrity",
                        severity="medium",
                        repo=repo.name,
                        doc_file=str(repo / "README.md"),
                        evidence=f"Invalid skills add command `{command.raw_line}`: {command.parse_error}",
                        recommended_fix="Use `npx skills add <owner/repo> [--all|--skill <skill-name>]`.",
                        auto_fixable=False,
                    )
                )
                continue

            if command.unknown_options:
                issues.append(
                    Issue(
                        issue_id="unsupported-skills-add-options",
                        category="command-integrity",
                        severity="medium",
                        repo=repo.name,
                        doc_file=str(repo / "README.md"),
                        evidence=f"Unsupported options in `{command.raw_line}`: {', '.join(command.unknown_options)}",
                        recommended_fix="Use only `--all` or `--skill <skill-name>` options.",
                        auto_fixable=False,
                    )
                )

            if command.extra_positionals:
                issues.append(
                    Issue(
                        issue_id="invalid-skills-add-arguments",
                        category="command-integrity",
                        severity="medium",
                        repo=repo.name,
                        doc_file=str(repo / "README.md"),
                        evidence=f"Unexpected positional arguments in `{command.raw_line}`: {', '.join(command.extra_positionals)}",
                        recommended_fix="Remove extra positional arguments from `skills add` command.",
                        auto_fixable=False,
                    )
                )

            if command.has_all and command.option_skill:
                issues.append(
                    Issue(
                        issue_id="invalid-skills-add-option-combination",
                        category="command-integrity",
                        severity="medium",
                        repo=repo.name,
                        doc_file=str(repo / "README.md"),
                        evidence=f"`--all` and `--skill` cannot be combined in `{command.raw_line}`.",
                        recommended_fix="Use either `--all` or `--skill <skill-name>`, not both.",
                        auto_fixable=False,
                    )
                )

            if (
                not command.has_all
                and not command.option_skill
                and not command.legacy_skill
                and not command.unknown_options
                and not command.extra_positionals
            ):
                has_own_base = True

            if command.option_skill and command.option_skill not in skill_dirs:
                issues.append(
                    Issue(
                        issue_id=f"missing-skill-ref-{command.option_skill}",
                        category="command-integrity",
                        severity="high",
                        repo=repo.name,
                        doc_file=str(repo / "README.md"),
                        evidence=f"Install command references unknown skill `{command.option_skill}`.",
                        recommended_fix="Use only skill names that have a SKILL.md directory.",
                        auto_fixable=False,
                    )
                )

    if profile == "public-curated" and not has_own_base:
        issues.append(
            Issue(
                issue_id="missing-base-install-command",
                category="command-integrity",
                severity="high",
                repo=repo.name,
                doc_file=str(repo / "README.md"),
                evidence="No base `npx skills add gaelic-ghost/<repo>` command found.",
                recommended_fix="Add base skills install command for this repository.",
                auto_fixable=True,
            )
        )

    duplicates = [cmd for cmd, count in own_cmd_counts.items() if count > 1]
    if duplicates:
        issues.append(
            Issue(
                issue_id="duplicate-install-commands",
                category="command-integrity",
                severity="low",
                repo=repo.name,
                doc_file=str(repo / "README.md"),
                evidence="Duplicate install command blocks detected.",
                recommended_fix="Deduplicate repeated install commands.",
                auto_fixable=False,
            )
        )

    if profile == "public-curated":
        find_count = len(re.findall(r"^\s*npx\s+skills\s+find\s+", text, flags=re.MULTILINE))
        if find_count < 3:
            issues.append(
                Issue(
                    issue_id="insufficient-find-examples",
                    category="command-integrity",
                    severity="medium",
                    repo=repo.name,
                    doc_file=str(repo / "README.md"),
                    evidence=f"Only {find_count} `npx skills find` examples present.",
                    recommended_fix="Add at least 3 realistic skills find examples.",
                    auto_fixable=True,
                )
            )

    return issues


def check_links(repo: Path, text: str) -> List[Issue]:
    issues: List[Issue] = []
    link_rx = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    for link in link_rx.findall(text):
        if link.startswith(("http://", "https://", "mailto:")):
            continue
        if link.startswith("#"):
            continue
        path_part = link.split("#", 1)[0].strip()
        if not path_part:
            continue
        target = (repo / path_part).resolve()
        if not target.exists():
            issues.append(
                Issue(
                    issue_id=f"broken-link-{abs(hash(link)) % 100000}",
                    category="schema-violation",
                    severity="low",
                    repo=repo.name,
                    doc_file=str(repo / "README.md"),
                    evidence=f"Broken relative link target: {link}",
                    recommended_fix="Update or remove broken relative link.",
                    auto_fixable=False,
                )
            )
    return issues


def make_bootstrap_readme(repo: Path, skill_dirs: List[str]) -> str:
    lines = [
        f"# {repo.name}",
        "",
        "Codex skills focused on accessibility and speech-friendly automation workflows.",
        "",
        "## What These Agent Skills Help With",
        "",
        "This repository supports accessibility-centered agent workflows and practical speech/readability tooling.",
        "",
        "## Skill Guide (When To Use What)",
        "",
    ]
    for skill in skill_dirs:
        lines.extend([
            f"- `{skill}`",
            "  - Use when you need this accessibility-oriented workflow.",
            "  - Helps by providing repeatable, agent-safe steps.",
            "",
        ])
    lines.extend([
        "## Quick Start (Vercel Skills CLI)",
        "",
        "```bash",
        "# Install your choice of skill(s) interactively via the Vercel `skills` CLI",
        "# Using `npx` fetches `skills` without installing it on your machine",
        f"npx skills add {EXPECTED_OWNER}/{repo.name}",
        "```",
        "",
        "The CLI will prompt you to choose which skill(s) to install from this repo.",
        "",
        "```bash",
        "# Install all skills from this repo non-interactively",
        f"npx skills add {EXPECTED_OWNER}/{repo.name} --all",
        "```",
        "",
        "## Install individually by Skill or Skill Pack",
        "",
    ])
    for skill in skill_dirs:
        lines.extend(["```bash", f"npx skills add {EXPECTED_OWNER}/{repo.name} --skill {skill}", "```", ""])

    lines.extend([
        "## Customization Workflow Matrix",
        "",
        "| Skill | Chat Customization Flow (SKILL.md) | Durable Config (`template` + persisted `customization.yaml`) | Automation Knobs | README Migration Status |",
        "| --- | --- | --- | --- | --- |",
        "| `<skill-name>` | Yes | Yes | No | README removed |",
        "",
        "## Update Skills",
        "",
        "```bash",
        "# Check for available updates to installed Skills",
        "npx skills check",
        "# Update installed Skills",
        "npx skills update",
        "```",
        "",
    ])

    lines.extend([
        "## More resources for similar Skills",
        "",
        "### Find Skills like these with the `skills` CLI by Vercel — [vercel-labs/skills](https://github.com/vercel-labs/skills)",
        "",
        "```bash",
        "npx skills find \"accessibility codex\"",
        "npx skills find \"speech automation\"",
        "npx skills find \"readability workflow\"",
        "```",
        "",
        "### Find Skills like these with the `Find Skills` Agent Skill by Vercel — [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills)",
        "",
        "```bash",
        "# `Find Skills` is a part of Vercel's `agent-skills` repo",
        "npx skills add vercel-labs/agent-skills --skill find-skills",
        "```",
        "",
        "Then ask your Agent for help finding a skill for \"\" or \"\"",
        "",
        "### Leaderboard",
        "",
        "- Skills catalog: [skills.sh](https://skills.sh/)",
        "",
        "## Repository Layout",
        "",
        "```text",
        ".",
        "├── README.md",
        "└── <skill-directories>/",
        "```",
        "",
        "## Notes",
        "",
        "- Keep README commands aligned with available skills.",
        "",
        "## Keywords",
        "",
        "Codex skills, accessibility automation, speech workflows, documentation alignment.",
        "",
        "## License",
        "",
        "Add a LICENSE file when this repository is ready for sharing.",
    ])
    return "\n".join(lines).strip() + "\n"


def normalize_headings(text: str, profile: str) -> Tuple[str, List[HeadingNormalizationEvent]]:
    allowed_keys = expected_section_keys(profile)
    out_lines = text.splitlines()
    events: List[HeadingNormalizationEvent] = []

    for idx, line in enumerate(out_lines):
        if not line.startswith("## "):
            continue
        section_key, method = resolve_section_key_for_heading(line, allowed_keys)
        if not section_key or not method:
            continue
        canonical = canonical_heading_line(section_key)
        if line == canonical:
            continue
        out_lines[idx] = canonical
        events.append(
            HeadingNormalizationEvent(
                line=idx + 1,
                section_key=section_key,
                original_heading=line,
                normalized_heading=canonical,
                normalization_method=method,
            )
        )

    out = "\n".join(out_lines)
    if text.endswith("\n"):
        out += "\n"
    return out, events


def wrap_legacy_more_resources_headings(text: str) -> str:
    lines = text.splitlines()
    legacy_lines: List[Tuple[int, str]] = []
    for idx, line in enumerate(lines):
        stripped = line.strip()
        key = resolve_legacy_more_resources_top_level_key(stripped)
        if key:
            legacy_lines.append((idx, key))

    if not legacy_lines:
        return text

    section_range = find_section_line_range(lines, SECTION_PATTERNS["more_resources"])
    if section_range is None:
        first_legacy_idx = legacy_lines[0][0]
        insertion = ["## More resources for similar Skills", ""]
        lines[first_legacy_idx:first_legacy_idx] = insertion
        shift = len(insertion)
        legacy_lines = [(idx + shift, key) for idx, key in legacy_lines]

    for idx, key in legacy_lines:
        lines[idx] = canonical_subheading_line(key)

    section_range = find_section_line_range(lines, SECTION_PATTERNS["more_resources"])
    if section_range is not None:
        start_idx, end_idx = section_range
        has_anchor = any(lines[idx].strip() == MORE_RESOURCES_ANCHOR_LINE for idx in range(start_idx + 1, end_idx))
        if not has_anchor:
            lines[end_idx:end_idx] = ["", MORE_RESOURCES_ANCHOR_LINE, ""]

    out = "\n".join(lines)
    if text.endswith("\n"):
        out += "\n"
    return out


def normalize_more_resources_subheadings(text: str, profile: str) -> Tuple[str, List[HeadingNormalizationEvent]]:
    if profile != "public-curated":
        return text, []

    lines = text.splitlines()
    section_range = find_section_line_range(lines, SECTION_PATTERNS["more_resources"])
    if section_range is None:
        return text, []

    start_idx, end_idx = section_range
    events: List[HeadingNormalizationEvent] = []
    for idx in range(start_idx + 1, end_idx):
        stripped = lines[idx].strip()
        if not (stripped.startswith("### ") or stripped.startswith("## ")):
            continue
        key, method = resolve_more_resources_subsection_key_for_heading(stripped, MORE_RESOURCES_SUBSECTION_KEYS)
        if not key or not method:
            continue
        canonical = canonical_subheading_line(key)
        if stripped == canonical:
            continue
        lines[idx] = canonical
        events.append(
            HeadingNormalizationEvent(
                line=idx + 1,
                section_key=f"more_resources/{key}",
                original_heading=stripped,
                normalized_heading=canonical,
                normalization_method=method,
            )
        )

    out = "\n".join(lines)
    if text.endswith("\n"):
        out += "\n"
    return out, events


def append_missing_more_resources_subsections(text: str, profile: str) -> Tuple[str, List[str]]:
    if profile != "public-curated":
        return text, []

    lines = text.splitlines()
    section_range = find_section_line_range(lines, SECTION_PATTERNS["more_resources"])
    if section_range is None:
        return text, []

    start_idx, end_idx = section_range
    section_lines = [line.strip() for line in lines[start_idx + 1 : end_idx]]
    appended: List[str] = []
    insertion_lines: List[str] = []

    for key in MORE_RESOURCES_SUBSECTION_KEYS:
        pattern = re.compile(MORE_RESOURCES_SUBSECTION_PATTERNS[key], re.IGNORECASE)
        if any(pattern.search(line) for line in section_lines):
            continue
        insertion_lines.extend([
            "",
            canonical_subheading_line(key),
            "",
            *MORE_RESOURCES_SUBSECTION_TEMPLATES[key].splitlines(),
        ])
        appended.append(f"more_resources/{key}")

    if not insertion_lines:
        return text, []

    lines[end_idx:end_idx] = insertion_lines + [""]
    out = "\n".join(lines)
    if text.endswith("\n"):
        out += "\n"
    return out, appended


def insert_section_by_order(text: str, key: str, template: str, expected_keys: Sequence[str]) -> str:
    lines = text.splitlines()
    insert_idx = len(lines)
    try:
        key_pos = list(expected_keys).index(key)
    except ValueError:
        key_pos = -1

    if key_pos >= 0:
        for next_key in expected_keys[key_pos + 1 :]:
            next_rx = re.compile(SECTION_PATTERNS[next_key], re.IGNORECASE)
            found_idx: Optional[int] = None
            for idx, line in enumerate(lines):
                if next_rx.search(line.strip()):
                    found_idx = idx
                    break
            if found_idx is not None:
                insert_idx = found_idx
                break

    block_lines = template.strip("\n").splitlines()
    if insert_idx > 0 and lines[insert_idx - 1].strip():
        block_lines = [""] + block_lines
    if insert_idx < len(lines) and lines[insert_idx].strip():
        block_lines = block_lines + [""]

    lines[insert_idx:insert_idx] = block_lines
    out = "\n".join(lines)
    if text.endswith("\n"):
        out += "\n"
    return out


def append_missing_sections(text: str, repo_name: str, profile: str) -> Tuple[str, List[str], List[HeadingNormalizationEvent]]:
    out = wrap_legacy_more_resources_headings(text)
    appended: List[str] = []
    if out != text:
        appended.append("more_resources/legacy-wrap")

    out, events = normalize_headings(out, profile)
    out, subsection_events = normalize_more_resources_subheadings(out, profile)
    events.extend(subsection_events)

    expected_keys = expected_section_keys(profile)
    for key in expected_keys:
        pattern = SECTION_PATTERNS[key]
        if re.search(pattern, out, flags=re.IGNORECASE | re.MULTILINE):
            continue
        template = SECTION_TEMPLATES[key].format(repo=repo_name)
        out = insert_section_by_order(out, key, template, expected_keys)
        appended.append(key)

    out, appended_subsections = append_missing_more_resources_subsections(out, profile)
    appended.extend(appended_subsections)

    return out, appended, events


def normalize_legacy_skills_add_syntax(text: str) -> Tuple[str, int]:
    out_lines: List[str] = []
    rewrites = 0

    for line in text.splitlines():
        parsed = parse_skills_add_command_line(line)
        if (
            parsed is None
            or parsed.owner is None
            or parsed.repo is None
            or not parsed.legacy_skill
        ):
            out_lines.append(line)
            continue

        # Rewrite only the target syntax; keep supported options.
        tokens = ["npx", "skills", "add", f"{parsed.owner}/{parsed.repo}"]
        if parsed.has_all:
            tokens.append("--all")
        tokens.extend(["--skill", parsed.option_skill or parsed.legacy_skill])
        tokens.extend(parsed.unknown_options)
        tokens.extend(parsed.extra_positionals)

        leading_ws = re.match(r"^\s*", line).group(0)
        out_lines.append(f"{leading_ws}{' '.join(tokens)}")
        rewrites += 1

    out = "\n".join(out_lines)
    if text.endswith("\n"):
        out += "\n"
    return out, rewrites


def dedupe_skills_add_lines(text: str) -> Tuple[str, int]:
    out_lines: List[str] = []
    seen: set[str] = set()
    removed = 0

    for line in text.splitlines():
        # Preserve multi-line shell commands. A trailing "\" indicates the line is
        # intentionally continued on the next line and should not be deduplicated
        # independently from the full command block.
        if line.rstrip().endswith("\\"):
            out_lines.append(line)
            continue

        parsed = parse_skills_add_command_line(line)
        if parsed is not None:
            dedupe_key = parsed.normalized_line
            if dedupe_key in seen:
                removed += 1
                continue
            seen.add(dedupe_key)
        out_lines.append(line)

    out = "\n".join(out_lines)
    if text.endswith("\n"):
        out += "\n"
    return out, removed


def apply_fixes_for_repo(repo: Path, profile: str, skill_dirs: List[str]) -> Tuple[bool, List[Dict[str, object]], Optional[str]]:
    fixes: List[Dict[str, object]] = []
    readme = repo / "README.md"

    if not readme.exists():
        if profile == "bootstrap":
            write_text(readme, make_bootstrap_readme(repo, skill_dirs))
            fixes.append({"repo": repo.name, "file": str(readme), "rule": "create-missing-readme", "status": "applied", "reason": "bootstrap profile"})
            return True, fixes, None
        return False, fixes, "README.md missing and profile is not bootstrap"

    before = read_text(readme)
    after, appended, normalization_events = append_missing_sections(before, repo.name, profile)
    after, rewritten_legacy_commands = normalize_legacy_skills_add_syntax(after)
    deduped_after, removed_command_count = dedupe_skills_add_lines(after)
    after = deduped_after

    changed = after != before
    if not changed:
        return False, fixes, "no bounded fix applied"

    write_text(readme, after)

    if normalization_events:
        fixes.append(
            {
                "repo": repo.name,
                "file": str(readme),
                "rule": "normalize-misnamed-headings",
                "status": "applied",
                "reason": f"normalized {len(normalization_events)} heading(s)",
                "events": [event.to_dict() for event in normalization_events],
            }
        )
    if appended:
        fixes.append(
            {
                "repo": repo.name,
                "file": str(readme),
                "rule": "append-missing-sections",
                "status": "applied",
                "reason": f"bounded section insertion: {', '.join(appended)}",
            }
        )
    if rewritten_legacy_commands > 0:
        fixes.append(
            {
                "repo": repo.name,
                "file": str(readme),
                "rule": "normalize-skills-add-syntax",
                "status": "applied",
                "reason": f"rewrote {rewritten_legacy_commands} legacy `@skill` command(s) to `--skill` syntax",
            }
        )
    if removed_command_count > 0:
        fixes.append(
            {
                "repo": repo.name,
                "file": str(readme),
                "rule": "dedupe-install-commands",
                "status": "applied",
                "reason": f"removed {removed_command_count} duplicate install command line(s)",
            }
        )

    return True, fixes, None


def summarize_markdown(report: Dict[str, object]) -> str:
    lines: List[str] = []
    rc = report["run_context"]
    lines.append("## Run Context")
    lines.append(f"- Timestamp: {rc['timestamp_utc']}")
    lines.append(f"- Workspace: {rc['workspace']}")
    lines.append(f"- Repo glob: {rc['repo_glob']}")
    lines.append(f"- Apply fixes: {rc['apply_fixes']}")
    lines.append("")

    lines.append("## Discovery Summary")
    lines.append(f"- Repos scanned: {len(report['repos_scanned'])}")
    lines.append(f"- Repos with issues: {len(report['repos_with_issues'])}")
    lines.append("")

    lines.append("## Profile Assignments")
    for name, profile in sorted(report["profile_assignments"].items()):
        lines.append(f"- {name}: {profile}")
    lines.append("")

    lines.append("## Schema Violations")
    if not report["schema_violations"]:
        lines.append("- None")
    else:
        for i in report["schema_violations"]:
            lines.append(f"- [{i['severity']}] {i['repo']}: {i['evidence']}")
    lines.append("")

    lines.append("## Command Integrity Issues")
    if not report["command_integrity_issues"]:
        lines.append("- None")
    else:
        for i in report["command_integrity_issues"]:
            lines.append(f"- [{i['severity']}] {i['repo']}: {i['evidence']}")
    lines.append("")

    lines.append("## Fixes Applied")
    if not report["fixes_applied"]:
        lines.append("- None")
    else:
        for f in report["fixes_applied"]:
            lines.append(f"- [{f['status']}] {f['repo']} -> {f['file']} ({f['rule']})")
    lines.append("")

    lines.append("## Post-Fix Status")
    ps = report["post_fix_status"]
    lines.append(f"- Unresolved issues: {ps['unresolved_issues']}")
    lines.append(f"- Resolved issues: {ps['resolved_issues']}")
    lines.append("")

    lines.append("## Errors")
    if not report["errors"]:
        lines.append("- None")
    else:
        for e in report["errors"]:
            lines.append(f"- {e['repo']}: {e['message']}")

    return "\n".join(lines).strip() + "\n"


def main() -> int:
    args = parse_args()
    workspace = Path(args.workspace).expanduser().resolve()
    if not workspace.exists() or not workspace.is_dir():
        print(f"Workspace path invalid: {workspace}", file=sys.stderr)
        return 1

    excludes = read_excludes(args.exclude)
    repos = discover_repos(workspace, args.repo_glob, excludes)

    profile_assignments: Dict[str, str] = {}
    schema_issues: List[Issue] = []
    command_issues: List[Issue] = []
    errors: List[Dict[str, str]] = []
    fixes_applied: List[Dict[str, object]] = []

    for repo in repos:
        profile = detect_profile(repo.name)
        profile_assignments[repo.name] = profile

        readme = repo / "README.md"
        skill_dirs = find_skill_dirs(repo)

        if not readme.exists():
            schema_issues.append(
                Issue(
                    issue_id="missing-readme",
                    category="schema-violation",
                    severity="high",
                    repo=repo.name,
                    doc_file=str(readme),
                    evidence="README.md is missing.",
                    recommended_fix="Create README using profile-appropriate template.",
                    auto_fixable=(profile == "bootstrap"),
                )
            )
            continue

        text = read_text(readme)
        schema_issues.extend(check_sections(repo, profile, text))
        schema_issues.extend(find_todo_issues(repo, text))
        schema_issues.extend(check_links(repo, text))
        command_issues.extend(check_commands(repo, profile, text, skill_dirs))

    initial_unresolved = len(schema_issues) + len(command_issues)

    if args.apply_fixes:
        for repo in repos:
            profile = profile_assignments[repo.name]
            skill_dirs = find_skill_dirs(repo)
            try:
                changed, fixes, reason = apply_fixes_for_repo(repo, profile, skill_dirs)
                if fixes:
                    fixes_applied.extend(fixes)
                elif reason:
                    fixes_applied.append({"repo": repo.name, "file": str(repo / "README.md"), "rule": "no-op", "status": "skipped", "reason": reason})
                if changed:
                    # Re-evaluate repo after fix.
                    readme = repo / "README.md"
                    text = read_text(readme)
                    schema_issues = [i for i in schema_issues if i.repo != repo.name]
                    command_issues = [i for i in command_issues if i.repo != repo.name]
                    schema_issues.extend(check_sections(repo, profile, text))
                    schema_issues.extend(find_todo_issues(repo, text))
                    schema_issues.extend(check_links(repo, text))
                    command_issues.extend(check_commands(repo, profile, text, skill_dirs))
            except Exception as exc:
                errors.append({"repo": repo.name, "message": f"fix error: {exc}"})

    unresolved = len(schema_issues) + len(command_issues)

    repos_with_issues = sorted({i.repo for i in schema_issues + command_issues})

    report: Dict[str, object] = {
        "run_context": {
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "workspace": str(workspace),
            "repo_glob": args.repo_glob,
            "apply_fixes": args.apply_fixes,
            "exclusions": [str(e) for e in excludes],
        },
        "repos_scanned": [str(r) for r in repos],
        "profile_assignments": profile_assignments,
        "schema_violations": [i.to_dict() for i in schema_issues],
        "command_integrity_issues": [i.to_dict() for i in command_issues],
        "repos_with_issues": repos_with_issues,
        "fixes_applied": fixes_applied,
        "post_fix_status": {
            "initial_issues": initial_unresolved,
            "unresolved_issues": unresolved,
            "resolved_issues": max(0, initial_unresolved - unresolved),
        },
        "errors": errors,
    }

    md_report = summarize_markdown(report)
    json_report = json.dumps(report, indent=2, sort_keys=True)

    if args.md_out:
        Path(args.md_out).expanduser().write_text(md_report, encoding="utf-8")
    if args.json_out:
        Path(args.json_out).expanduser().write_text(json_report + "\n", encoding="utf-8")
    if args.print_md:
        print(md_report, end="")
    if args.print_json:
        print(json_report)

    if args.fail_on_issues and unresolved > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
