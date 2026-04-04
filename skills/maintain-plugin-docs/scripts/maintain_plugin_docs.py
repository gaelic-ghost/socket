#!/usr/bin/env python3
"""Two-pass plugin-docs maintenance workflow for skills and plugin repositories."""

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
DEFAULT_DOC_SCOPE = "readme"

ROADMAP_DEFAULT_TEMPLATE = """# Project Roadmap

## Vision

- Define the long-term outcome for this plugin-development repository.

## Product Principles

- Keep plugin-development docs deterministic, reviewable, and aligned with real repo behavior.

## Milestone Progress

- [ ] Milestone 0: Foundation

## Milestone 0: Foundation

Scope:

- [ ] Define initial plugin-development scope.

Tickets:

- [ ] Add the first implementation task.

Exit criteria:

- [ ] Scope, tickets, and validation are complete.
"""

ROADMAP_REQUIRED_TOP_LEVEL = ["Vision", "Product Principles", "Milestone Progress"]
ROADMAP_REQUIRED_TOP_LEVEL_ALIASES = {"Product principles": "Product Principles"}
ROADMAP_REQUIRED_MILESTONE_SUBSECTIONS = ["Scope", "Tickets", "Exit criteria"]
ROADMAP_CHECKBOX_RE = re.compile(r"^\s*-\s+\[( |x)\]\s+.+$")
ROADMAP_ANY_CHECKBOX_RE = re.compile(r"^\s*-\s+\[[^\]]\]\s+.+$")
ROADMAP_MILESTONE_HEADING_RE = re.compile(r"^##\s+Milestone\s+(\d+)\s*:\s*(.+?)\s*$")
ROADMAP_PROGRESS_ENTRY_RE = re.compile(r"^\s*-\s+\[( |x)\]\s+Milestone\s+(\d+)\s*:\s*(.+?)\s*$")
ROADMAP_SUBSECTION_LABEL_RE = re.compile(r"^(Scope|Tickets|Exit criteria):\s*$")

CORE_SECTION_KEYS = [
    "toc",
    "what",
    "guide",
    "quickstart",
    "individual",
    "update_skills",
    "more_resources",
    "layout",
    "notes",
    "keywords",
    "license",
]

PLUGIN_MAINTAINER_SECTION_KEYS = [
    "active_skills",
    "repo_purpose",
    "packaging",
    "standards",
    "tooling",
    "install",
    "layout",
    "license",
]

SECTION_CANONICAL_HEADINGS = {
    "active_skills": "Active Skills",
    "repo_purpose": "Repo Purpose",
    "packaging": "Packaging And Discovery",
    "standards": "Standards And Docs",
    "tooling": "Maintainer Python Tooling",
    "install": "Install",
    "toc": "Table of Contents",
    "what": "What These Agent Skills Help With",
    "guide": "Skill Guide (When To Use What)",
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
    "active_skills": r"^##\s+Active Skills\s*$",
    "repo_purpose": r"^##\s+Repo Purpose\s*$",
    "packaging": r"^##\s+Packaging And Discovery\s*$",
    "standards": r"^##\s+Standards And Docs\s*$",
    "tooling": r"^##\s+Maintainer Python Tooling\s*$",
    "install": r"^##\s+Install\s*$",
    "toc": r"^##\s+Table of Contents\s*$",
    "what": r"^##\s+What These Agent Skills Help With\s*$",
    "guide": r"^##\s+Skill Guide \(When To Use What\)\s*$",
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

TOOLING_REQUIRED_SNIPPETS = [
    "uv sync --dev",
    "uv tool install ruff",
    "uv tool install mypy",
    "uv run --group dev pytest",
]

HEADING_ALIASES = {
    "active skills": "active_skills",
    "repo purpose": "repo_purpose",
    "packaging and discovery": "packaging",
    "standards and docs": "standards",
    "maintainer python tooling": "tooling",
    "install": "install",
    "table of contents": "toc",
    "how to add (skills cli)": "quickstart",
    "how to add (vercel skills cli)": "quickstart",
    "how to add with skills cli": "quickstart",
    "quickstart (skills cli)": "quickstart",
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
    ("active_skills", re.compile(r"^active\s+skills$", re.IGNORECASE)),
    ("repo_purpose", re.compile(r"^repo\s+purpose$", re.IGNORECASE)),
    ("packaging", re.compile(r"^packaging\s+and\s+discovery$", re.IGNORECASE)),
    ("standards", re.compile(r"^standards\s+and\s+docs$", re.IGNORECASE)),
    ("tooling", re.compile(r"^maintainer\s+python\s+tooling$", re.IGNORECASE)),
    ("install", re.compile(r"^install$", re.IGNORECASE)),
    ("toc", re.compile(r"^table\s+of\s+contents$", re.IGNORECASE)),
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
    "active_skills": "## Active Skills\n\n- `<skill-name>`\n  - Current implementation: ...\n  - Intended scope: ...\n",
    "repo_purpose": "## Repo Purpose\n\nDescribe the maintainer-facing purpose of this skills or plugin repository.\n",
    "packaging": "## Packaging And Discovery\n\nSummarize the canonical `skills/` surface, plugin packaging roots, and discovery mirrors.\n",
    "standards": "## Standards And Docs\n\nList the primary standard and platform-specific references for this repo family.\n",
    "tooling": (
        "## Maintainer Python Tooling\n\n"
        "```bash\n"
        "uv sync --dev\n"
        "uv tool install ruff\n"
        "uv tool install mypy\n"
        "uv run --group dev pytest\n"
        "```\n"
    ),
    "install": "## Install\n\nDocument the primary plugin install surfaces first, then any secondary distribution paths.\n",
    "toc": (
        "## Table of Contents\n\n"
        "- [What These Agent Skills Help With](#what-these-agent-skills-help-with)\n"
        "- [Skill Guide (When To Use What)](#skill-guide-when-to-use-what)\n"
        "- [Quick Start (Vercel Skills CLI)](#quick-start-vercel-skills-cli)\n"
        "- [Install individually by Skill or Skill Pack](#install-individually-by-skill-or-skill-pack)\n"
        "- [Update Skills](#update-skills)\n"
        "- [More resources for similar Skills](#more-resources-for-similar-skills)\n"
        "- [Repository Layout](#repository-layout)\n"
        "- [Notes](#notes)\n"
        "- [Keywords](#keywords)\n"
        "- [License](#license)\n"
    ),
    "what": "## What These Agent Skills Help With\n\nDescribe the audience and the workflows this repository improves.\n",
    "guide": "## Skill Guide (When To Use What)\n\n- `<skill-name>`\n  - Use when ...\n  - Helps by ...\n",
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
    "keywords": "## Keywords\n\nCodex skills, automation, workflows, README maintenance.\n",
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
    parser = argparse.ArgumentParser(
        description="Audit and optionally apply plugin-docs maintenance for stack-specific skills and plugin repos"
    )
    parser.add_argument("--workspace", required=True, help="Workspace root")
    parser.add_argument("--repo-glob", default="*-skills", help="Repo directory glob")
    parser.add_argument(
        "--doc-scope",
        choices=["readme", "roadmap", "all"],
        default=DEFAULT_DOC_SCOPE,
        help="Document surface to audit and optionally fix",
    )
    parser.add_argument("--exclude", action="append", default=[], help="Path to exclude (repeatable)")
    parser.add_argument("--apply-fixes", action="store_true", help="Apply bounded docs fixes for the selected scope")
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


def repo_has_plugin_packaging(repo: Path) -> bool:
    return any(repo.glob("plugins/*/.codex-plugin/plugin.json")) or any(
        repo.glob("plugins/*/.claude-plugin/plugin.json")
    )


def detect_profile(repo: Path) -> str:
    repo_name = repo.name
    if repo_name in PUBLIC_REPOS:
        return "public-curated"
    if repo_name in PRIVATE_REPOS:
        return "private-internal"
    if repo_name in BOOTSTRAP_REPOS:
        return "bootstrap"
    if (repo / "skills").is_dir() and repo_has_plugin_packaging(repo):
        return "plugin-maintainer"
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
        # Public READMEs require a compact TOC and place keywords before license.
        return [
            "toc",
            "what",
            "guide",
            "quickstart",
            "individual",
            "update_skills",
            "more_resources",
            "layout",
            "notes",
            "keywords",
            "license",
        ]
    if profile == "plugin-maintainer":
        return list(PLUGIN_MAINTAINER_SECTION_KEYS)
    return list(CORE_SECTION_KEYS)


def heading_to_fragment(heading: str) -> str:
    fragment = heading.strip().lower()
    fragment = re.sub(r"[`]", "", fragment)
    fragment = re.sub(r"[^\w\s-]", "", fragment)
    fragment = re.sub(r"\s+", "-", fragment)
    fragment = re.sub(r"-+", "-", fragment).strip("-")
    return fragment


def check_compact_toc(repo: Path, text: str) -> List[Issue]:
    issues: List[Issue] = []
    lines = text.splitlines()
    headings = heading_lines(text)

    h2_headings = [(lineno, line) for lineno, line in headings if line.startswith("## ")]
    if not h2_headings:
        return issues

    toc_range = find_section_line_range(lines, SECTION_PATTERNS["toc"])
    if toc_range is None:
        # Missing TOC is handled by canonical required-section checks.
        return issues

    first_h2_lineno, first_h2_heading = h2_headings[0]
    if first_h2_heading != "## Table of Contents":
        issues.append(
            Issue(
                issue_id="toc-placement",
                category="schema-violation",
                severity="low",
                repo=repo.name,
                doc_file=str(repo / "README.md"),
                evidence=f"First H2 heading is `{first_h2_heading}` at line {first_h2_lineno}; TOC must be the first H2.",
                recommended_fix="Place `## Table of Contents` before other H2 sections.",
                auto_fixable=False,
            )
        )

    start_idx, end_idx = toc_range
    toc_lines = lines[start_idx + 1 : end_idx]
    toc_entries: List[Tuple[int, str]] = []
    for idx, raw in enumerate(toc_lines, start=start_idx + 2):
        line = raw.rstrip()
        if not line.strip():
            continue
        if re.match(r"^\s+-\s+", line):
            issues.append(
                Issue(
                    issue_id="toc-not-compact",
                    category="schema-violation",
                    severity="low",
                    repo=repo.name,
                    doc_file=str(repo / "README.md"),
                    evidence=f"Nested TOC bullet detected at line {idx}: `{line.strip()}`",
                    recommended_fix="Use top-level H2 links only (no nested bullets).",
                    auto_fixable=False,
                )
            )
            continue
        match = re.match(r"^-\s+\[(.+)\]\(#([^)]+)\)\s*$", line)
        if not match:
            issues.append(
                Issue(
                    issue_id="toc-entry-invalid",
                    category="schema-violation",
                    severity="low",
                    repo=repo.name,
                    doc_file=str(repo / "README.md"),
                    evidence=f"Invalid TOC entry at line {idx}: `{line.strip()}`",
                    recommended_fix="Use `- [Section](#fragment)` entries only in TOC.",
                    auto_fixable=False,
                )
            )
            continue
        toc_entries.append((idx, match.group(2).strip().lower()))

    h2_targets = {
        heading_to_fragment(h[3:]): h
        for _lineno, h in h2_headings
        if h != "## Table of Contents"
    }

    seen_fragments = set()
    for lineno, fragment in toc_entries:
        if fragment == "table-of-contents":
            issues.append(
                Issue(
                    issue_id="toc-self-link",
                    category="schema-violation",
                    severity="low",
                    repo=repo.name,
                    doc_file=str(repo / "README.md"),
                    evidence=f"TOC links to itself at line {lineno}.",
                    recommended_fix="Do not include `Table of Contents` in TOC entries.",
                    auto_fixable=False,
                )
            )
        if fragment not in h2_targets:
            issues.append(
                Issue(
                    issue_id="toc-broken-link",
                    category="schema-violation",
                    severity="low",
                    repo=repo.name,
                    doc_file=str(repo / "README.md"),
                    evidence=f"TOC link `#{fragment}` at line {lineno} does not target an H2 heading.",
                    recommended_fix="Point TOC links to existing H2 headings.",
                    auto_fixable=False,
                )
            )
        seen_fragments.add(fragment)

    missing_h2_links = [frag for frag in h2_targets if frag not in seen_fragments]
    if missing_h2_links:
        issues.append(
            Issue(
                issue_id="toc-missing-h2-links",
                category="schema-violation",
                severity="low",
                repo=repo.name,
                doc_file=str(repo / "README.md"),
                evidence=f"TOC does not include H2 sections: {', '.join(f'#{frag}' for frag in missing_h2_links)}",
                recommended_fix="Add TOC entries for every H2 heading except `Table of Contents`.",
                auto_fixable=False,
            )
        )

    return issues


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


def check_tooling_section(repo: Path, profile: str, lines: Sequence[str]) -> List[Issue]:
    if profile != "plugin-maintainer":
        return []

    section_range = find_section_line_range(lines, SECTION_PATTERNS["tooling"])
    if section_range is None:
        return []

    start_idx, end_idx = section_range
    section_text = "\n".join(lines[start_idx:end_idx])
    issues: List[Issue] = []
    for snippet in TOOLING_REQUIRED_SNIPPETS:
        if snippet in section_text:
            continue
        issues.append(
            Issue(
                issue_id="tooling-guidance-missing-snippet",
                category="schema-violation",
                severity="medium",
                repo=repo.name,
                doc_file=str(repo / "README.md"),
                evidence=f"`## Maintainer Python Tooling` is missing `{snippet}`.",
                recommended_fix="Document the default maintainer Python baseline with uv sync, uv-managed ruff and mypy tools, and pytest.",
                auto_fixable=True,
            )
        )
    return issues


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
    issues.extend(check_compact_toc(repo, text))
    issues.extend(check_tooling_section(repo, profile, all_lines))

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
        "## Table of Contents",
        "",
        "- [What These Agent Skills Help With](#what-these-agent-skills-help-with)",
        "- [Skill Guide (When To Use What)](#skill-guide-when-to-use-what)",
        "- [Quick Start (Vercel Skills CLI)](#quick-start-vercel-skills-cli)",
        "- [Install individually by Skill or Skill Pack](#install-individually-by-skill-or-skill-pack)",
        "- [Update Skills](#update-skills)",
        "- [More resources for similar Skills](#more-resources-for-similar-skills)",
        "- [Repository Layout](#repository-layout)",
        "- [Notes](#notes)",
        "- [Keywords](#keywords)",
        "- [License](#license)",
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
        "Codex skills, accessibility automation, speech workflows, README maintenance.",
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


def split_roadmap_sections(text: str) -> List[Tuple[str, List[str]]]:
    lines = text.splitlines()
    sections: List[Tuple[str, List[str]]] = []
    current_heading = "__preamble__"
    current_lines: List[str] = []

    for line in lines:
        if line.startswith("## "):
            sections.append((current_heading, current_lines))
            current_heading = line[3:].strip()
            current_lines = []
        else:
            current_lines.append(line)
    sections.append((current_heading, current_lines))
    return sections


def roadmap_milestone_sections(sections: Sequence[Tuple[str, List[str]]]) -> List[Tuple[int, str, List[str]]]:
    result: List[Tuple[int, str, List[str]]] = []
    for heading, lines in sections:
        match = ROADMAP_MILESTONE_HEADING_RE.match(f"## {heading}")
        if match:
            result.append((int(match.group(1)), match.group(2).strip(), lines))
    return result


def has_legacy_roadmap_format(text: str) -> bool:
    if re.search(r"^##\s+Current Milestone\s*$", text, flags=re.MULTILINE):
        return True
    if re.search(r"^##\s+Milestones\s*$", text, flags=re.MULTILINE) and "|" in text:
        return True
    if re.search(r"\|\s*Milestone\s*\|", text, flags=re.IGNORECASE):
        return True
    return False


def parse_legacy_roadmap_milestones(text: str) -> List[Tuple[int, str, str]]:
    rows: List[Tuple[int, str, str]] = []
    lines = text.splitlines()
    in_table = False
    for line in lines:
        if re.match(r"^\|\s*Milestone\s*\|", line, flags=re.IGNORECASE):
            in_table = True
            continue
        if in_table and re.match(r"^\|\s*[-:]+\s*\|", line):
            continue
        if in_table and line.strip().startswith("|"):
            cols = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cols) >= 2:
                name = cols[0]
                status = cols[1]
                match = re.search(r"(\d+)", name)
                idx = int(match.group(1)) if match else len(rows)
                title = re.sub(r"^Milestone\s*\d+\s*[:\-]?\s*", "", name, flags=re.IGNORECASE).strip() or name
                rows.append((idx, title, status))
        elif in_table and line.strip() == "":
            in_table = False
    return sorted(rows, key=lambda item: item[0])


def roadmap_status_to_checkbox(status: str) -> str:
    lowered = status.lower()
    if any(token in lowered for token in ["done", "complete", "completed", "shipped"]):
        return "[x]"
    return "[ ]"


def canonicalize_roadmap_heading(heading: str) -> str:
    return ROADMAP_REQUIRED_TOP_LEVEL_ALIASES.get(heading, heading)


def parse_roadmap_progress_entries(lines: Sequence[str]) -> Tuple[List[Tuple[int, bool, int, str]], List[Tuple[int, str]]]:
    entries: List[Tuple[int, bool, int, str]] = []
    invalid: List[Tuple[int, str]] = []
    progress_range = find_section_line_range(lines, r"^##\s+Milestone Progress\s*$")
    if progress_range is None:
        return entries, invalid

    start_idx, end_idx = progress_range
    for idx in range(start_idx + 1, end_idx):
        stripped = lines[idx].strip()
        if not stripped:
            continue
        match = ROADMAP_PROGRESS_ENTRY_RE.match(stripped)
        if not match:
            invalid.append((idx + 1, stripped))
            continue
        entries.append((idx + 1, match.group(1) == "x", int(match.group(2)), match.group(3).strip()))
    return entries, invalid


def parse_milestone_subsections(body_lines: Sequence[str]) -> Dict[str, List[str]]:
    sections: Dict[str, List[str]] = {name: [] for name in ROADMAP_REQUIRED_MILESTONE_SUBSECTIONS}
    preamble: List[str] = []
    current: Optional[str] = None

    for line in body_lines:
        label_match = ROADMAP_SUBSECTION_LABEL_RE.match(line.strip())
        if label_match:
            current = label_match.group(1)
            continue
        if current is None:
            preamble.append(line)
            continue
        sections[current].append(line)

    if preamble:
        sections["Scope"] = preamble + ([""] if preamble and sections["Scope"] else []) + sections["Scope"]
    return sections


def trim_blank_lines(lines: Sequence[str]) -> List[str]:
    trimmed = list(lines)
    while trimmed and not trimmed[0].strip():
        trimmed.pop(0)
    while trimmed and not trimmed[-1].strip():
        trimmed.pop()
    return trimmed


def default_milestone_subsection_lines(subsection: str) -> List[str]:
    if subsection == "Scope":
        return ["- [ ] Define milestone scope."]
    if subsection == "Tickets":
        return ["- [ ] Add milestone implementation tasks."]
    return ["- [ ] Define milestone exit criteria."]


def normalize_milestone_body(body_lines: Sequence[str]) -> List[str]:
    parsed = parse_milestone_subsections(body_lines)
    out: List[str] = []
    for subsection in ROADMAP_REQUIRED_MILESTONE_SUBSECTIONS:
        content = trim_blank_lines(parsed[subsection])
        if not content:
            content = default_milestone_subsection_lines(subsection)
        out.extend([f"{subsection}:", "", *content, ""])
    return out[:-1]


def milestone_is_complete(body_lines: Sequence[str]) -> bool:
    checkbox_lines = [line for line in body_lines if ROADMAP_CHECKBOX_RE.match(line)]
    if not checkbox_lines:
        return False
    return all("[x]" in line.lower() for line in checkbox_lines)


def validate_roadmap(repo: Path, text: str) -> List[Issue]:
    roadmap_path = repo / "ROADMAP.md"
    findings: List[Issue] = []
    lines = text.splitlines()
    first_non_empty = next((line.strip() for line in lines if line.strip()), "")
    if first_non_empty != "# Project Roadmap":
        findings.append(
            Issue(
                issue_id="roadmap-title",
                category="roadmap-violation",
                severity="high",
                repo=repo.name,
                doc_file=str(roadmap_path),
                evidence="ROADMAP must start with `# Project Roadmap`.",
                recommended_fix="Normalize the roadmap title to `# Project Roadmap`.",
                auto_fixable=True,
            )
        )

    sections = split_roadmap_sections(text)
    headings = {heading for heading, _body in sections}
    normalized_headings = {ROADMAP_REQUIRED_TOP_LEVEL_ALIASES.get(heading, heading) for heading in headings}
    for required in ROADMAP_REQUIRED_TOP_LEVEL:
        if required not in normalized_headings:
            findings.append(
                Issue(
                    issue_id=f"roadmap-missing-section-{required.lower().replace(' ', '-')}",
                    category="roadmap-violation",
                    severity="high",
                    repo=repo.name,
                    doc_file=str(roadmap_path),
                    evidence=f"Missing required roadmap section: {required}",
                    recommended_fix=f"Add the `{required}` section.",
                    auto_fixable=True,
                )
            )

    ordered_headings = [canonicalize_roadmap_heading(heading) for heading, _body in sections if heading != "__preamble__"]
    required_positions = [ordered_headings.index(required) for required in ROADMAP_REQUIRED_TOP_LEVEL if required in ordered_headings]
    if required_positions and required_positions != sorted(required_positions):
        findings.append(
            Issue(
                issue_id="roadmap-top-level-order",
                category="roadmap-violation",
                severity="medium",
                repo=repo.name,
                doc_file=str(roadmap_path),
                evidence="`Vision`, `Product Principles`, and `Milestone Progress` are not in canonical order.",
                recommended_fix="Order the roadmap as `Vision`, `Product Principles`, `Milestone Progress`, then milestone sections.",
                auto_fixable=True,
            )
        )

    for heading, _body in sections:
        canonical_heading = canonicalize_roadmap_heading(heading)
        if heading == "__preamble__" or heading == canonical_heading:
            continue
        findings.append(
            Issue(
                issue_id=f"roadmap-section-misnamed-{canonical_heading.lower().replace(' ', '-')}",
                category="roadmap-violation",
                severity="low",
                repo=repo.name,
                doc_file=str(roadmap_path),
                evidence=f"Section heading `## {heading}` should be `## {canonical_heading}`.",
                recommended_fix=f"Rename `## {heading}` to `## {canonical_heading}`.",
                auto_fixable=True,
            )
        )

    milestones = roadmap_milestone_sections(sections)
    if not milestones:
        findings.append(
            Issue(
                issue_id="roadmap-missing-milestones",
                category="roadmap-violation",
                severity="high",
                repo=repo.name,
                doc_file=str(roadmap_path),
                evidence="No milestone sections found.",
                recommended_fix="Add milestone sections with headings like `## Milestone N: Name`.",
                auto_fixable=True,
            )
        )
    else:
        ordered = [item[0] for item in milestones]
        if ordered != sorted(ordered):
            findings.append(
                Issue(
                    issue_id="roadmap-milestone-order",
                    category="roadmap-violation",
                    severity="medium",
                    repo=repo.name,
                    doc_file=str(roadmap_path),
                    evidence="Milestone sections are not in ascending order.",
                    recommended_fix="Reorder milestone sections into deterministic ascending order.",
                    auto_fixable=True,
                )
            )
        if len(set(ordered)) != len(ordered):
            findings.append(
                Issue(
                    issue_id="roadmap-milestone-duplicate-index",
                    category="roadmap-violation",
                    severity="high",
                    repo=repo.name,
                    doc_file=str(roadmap_path),
                    evidence="Duplicate milestone numbers found in milestone headings.",
                    recommended_fix="Use each milestone number exactly once.",
                    auto_fixable=True,
                )
            )
        if ordered and ordered != list(range(ordered[0], ordered[0] + len(ordered))):
            findings.append(
                Issue(
                    issue_id="roadmap-milestone-sequence",
                    category="roadmap-violation",
                    severity="medium",
                    repo=repo.name,
                    doc_file=str(roadmap_path),
                    evidence="Milestone numbers are not deterministic and sequential.",
                    recommended_fix="Use a contiguous milestone sequence without gaps or jumps.",
                    auto_fixable=True,
                )
            )

        for idx, _title, body in milestones:
            joined = "\n".join(body)
            subsection_order: List[int] = []
            for subsection in ROADMAP_REQUIRED_MILESTONE_SUBSECTIONS:
                if f"{subsection}:" not in joined:
                    findings.append(
                        Issue(
                            issue_id=f"roadmap-milestone-{idx}-missing-{subsection.lower().replace(' ', '-')}",
                            category="roadmap-violation",
                            severity="high",
                            repo=repo.name,
                            doc_file=str(roadmap_path),
                            evidence=f"Milestone {idx} is missing subsection `{subsection}:`.",
                            recommended_fix=f"Add the `{subsection}:` block to milestone {idx}.",
                            auto_fixable=True,
                        )
                    )
                    continue
                subsection_order.append(joined.index(f"{subsection}:"))
            if subsection_order and subsection_order != sorted(subsection_order):
                findings.append(
                    Issue(
                        issue_id=f"roadmap-milestone-{idx}-subsection-order",
                        category="roadmap-violation",
                        severity="medium",
                        repo=repo.name,
                        doc_file=str(roadmap_path),
                        evidence=f"Milestone {idx} subsections are not in `Scope`, `Tickets`, `Exit criteria` order.",
                        recommended_fix=f"Reorder milestone {idx} subsections to the canonical order.",
                        auto_fixable=True,
                    )
                )

    for line_no, line in enumerate(lines, start=1):
        if ROADMAP_ANY_CHECKBOX_RE.match(line) and not ROADMAP_CHECKBOX_RE.match(line):
            findings.append(
                Issue(
                    issue_id=f"roadmap-invalid-checkbox-{line_no}",
                    category="roadmap-violation",
                    severity="medium",
                    repo=repo.name,
                    doc_file=str(roadmap_path),
                    evidence=f"Invalid checkbox syntax on line {line_no}: `{line.strip()}`",
                    recommended_fix="Use only `[ ]` or `[x]` checkbox syntax.",
                    auto_fixable=True,
                )
            )

    progress_entries, invalid_progress_entries = parse_roadmap_progress_entries(lines)
    for line_no, line in invalid_progress_entries:
        findings.append(
            Issue(
                issue_id=f"roadmap-progress-entry-format-{line_no}",
                category="roadmap-violation",
                severity="medium",
                repo=repo.name,
                doc_file=str(roadmap_path),
                evidence=f"Invalid `Milestone Progress` entry on line {line_no}: `{line}`",
                recommended_fix="Use `- [ ] Milestone N: Title` or `- [x] Milestone N: Title` entries only.",
                auto_fixable=True,
            )
        )
    milestone_progress_count = len(progress_entries)
    if milestones and milestone_progress_count != len(milestones):
        findings.append(
            Issue(
                issue_id="roadmap-progress-count-mismatch",
                category="roadmap-violation",
                severity="medium",
                repo=repo.name,
                doc_file=str(roadmap_path),
                evidence="`Milestone Progress` count does not match the number of milestone sections.",
                recommended_fix="Update `Milestone Progress` so it reflects all milestone sections.",
                auto_fixable=True,
            )
        )
    if milestones and progress_entries:
        milestone_index_map = {idx: (title, body) for idx, title, body in milestones}
        for _line_no, checked, idx, title in progress_entries:
            milestone = milestone_index_map.get(idx)
            if milestone is None:
                findings.append(
                    Issue(
                        issue_id=f"roadmap-progress-missing-milestone-{idx}",
                        category="roadmap-violation",
                        severity="medium",
                        repo=repo.name,
                        doc_file=str(roadmap_path),
                        evidence=f"`Milestone Progress` includes Milestone {idx}, but no matching milestone section exists.",
                        recommended_fix="Keep `Milestone Progress` entries aligned with real milestone sections.",
                        auto_fixable=True,
                    )
                )
                continue
            milestone_title, body = milestone
            if title != milestone_title:
                findings.append(
                    Issue(
                        issue_id=f"roadmap-progress-title-mismatch-{idx}",
                        category="roadmap-violation",
                        severity="medium",
                        repo=repo.name,
                        doc_file=str(roadmap_path),
                        evidence=f"`Milestone Progress` labels Milestone {idx} as `{title}`, but the milestone heading uses `{milestone_title}`.",
                        recommended_fix="Use the same milestone title in `Milestone Progress` and the milestone heading.",
                        auto_fixable=True,
                    )
                )
            milestone_complete = milestone_is_complete(normalize_milestone_body(body))
            if checked != milestone_complete:
                findings.append(
                    Issue(
                        issue_id=f"roadmap-progress-reality-mismatch-{idx}",
                        category="roadmap-violation",
                        severity="medium",
                        repo=repo.name,
                        doc_file=str(roadmap_path),
                        evidence=f"`Milestone Progress` marks Milestone {idx} as {'complete' if checked else 'incomplete'}, but the milestone checklist state says it is {'complete' if milestone_complete else 'incomplete'}.",
                        recommended_fix="Make the `Milestone Progress` checkbox reflect the milestone checklist state.",
                        auto_fixable=True,
                    )
                )

    if has_legacy_roadmap_format(text):
        findings.append(
            Issue(
                issue_id="roadmap-legacy-format",
                category="roadmap-violation",
                severity="medium",
                repo=repo.name,
                doc_file=str(roadmap_path),
                evidence="Legacy roadmap format detected.",
                recommended_fix="Migrate the roadmap to checklist-style milestone sections.",
                auto_fixable=True,
            )
        )

    return findings


def build_roadmap_from_legacy(text: str) -> str:
    rows = parse_legacy_roadmap_milestones(text)
    if not rows:
        rows = [(0, "Foundation", "Planned")]

    out_lines: List[str] = [
        "# Project Roadmap",
        "",
        "## Vision",
        "",
        "- Preserved from legacy roadmap during checklist migration.",
        "",
        "## Product Principles",
        "",
        "- Keep plugin-development roadmap sections checklist-based and deterministic.",
        "",
        "## Milestone Progress",
        "",
    ]

    for idx, title, status in rows:
        out_lines.append(f"- {roadmap_status_to_checkbox(status)} Milestone {idx}: {title} ({status})")

    out_lines.append("")

    for idx, title, status in rows:
        out_lines.extend(
            [
                f"## Milestone {idx}: {title}",
                "",
                "Scope:",
                "",
                f"- [ ] Preserve legacy scope details for status: {status}.",
                "",
                "Tickets:",
                "",
                "- [ ] Add or reconcile milestone tasks.",
                "",
                "Exit criteria:",
                "",
                "- [ ] Milestone checklist is complete and validated.",
                "",
            ]
        )

    return "\n".join(out_lines).strip() + "\n"


def build_canonical_roadmap(text: str) -> str:
    if has_legacy_roadmap_format(text):
        return build_roadmap_from_legacy(text)

    original_sections = split_roadmap_sections(text)
    section_map = {
        canonicalize_roadmap_heading(heading): body
        for heading, body in original_sections
        if heading != "__preamble__"
    }
    milestone_sections = roadmap_milestone_sections(
        [(canonicalize_roadmap_heading(heading), body) for heading, body in original_sections]
    )
    milestone_sections = sorted(milestone_sections, key=lambda item: item[0])

    if not milestone_sections:
        milestone_sections = [
            (
                0,
                "Foundation",
                [
                    "Scope:",
                    "",
                    "- [ ] Define initial plugin-development scope.",
                    "",
                    "Tickets:",
                    "",
                    "- [ ] Add the first implementation task.",
                    "",
                    "Exit criteria:",
                    "",
                    "- [ ] Scope, tickets, and validation are complete.",
                ],
            )
        ]

    vision_body = trim_blank_lines(section_map.get("Vision", [])) or [
        "- Define the long-term outcome for this plugin-development repository."
    ]
    product_body = trim_blank_lines(section_map.get("Product Principles", [])) or [
        "- Keep plugin-development docs deterministic, reviewable, and aligned with real repo behavior."
    ]

    out_lines: List[str] = [
        "# Project Roadmap",
        "",
        "## Vision",
        "",
        *vision_body,
        "",
        "## Product Principles",
        "",
        *product_body,
        "",
        "## Milestone Progress",
        "",
    ]

    for idx, title, body in milestone_sections:
        normalized_body = normalize_milestone_body(body)
        checkbox = "[x]" if milestone_is_complete(normalized_body) else "[ ]"
        out_lines.append(f"- {checkbox} Milestone {idx}: {title}")

    out_lines.append("")

    for idx, title, body in milestone_sections:
        out_lines.extend(
            [
                f"## Milestone {idx}: {title}",
                "",
                *normalize_milestone_body(body),
                "",
            ]
        )

    extra_sections = [
        (canonicalize_roadmap_heading(heading), body)
        for heading, body in original_sections
        if heading not in {"__preamble__", "Vision", "Product Principles", "Milestone Progress"}
        and not ROADMAP_MILESTONE_HEADING_RE.match(f"## {canonicalize_roadmap_heading(heading)}")
    ]
    for heading, body in extra_sections:
        trimmed_body = trim_blank_lines(body)
        out_lines.extend([f"## {heading}", ""])
        if trimmed_body:
            out_lines.extend(trimmed_body)
            out_lines.append("")

    return "\n".join(out_lines).rstrip() + "\n"


def ensure_roadmap_apply_shape(text: str) -> str:
    if not text.strip():
        return ROADMAP_DEFAULT_TEMPLATE
    return build_canonical_roadmap(text)


def apply_fixes_for_roadmap(repo: Path) -> Tuple[bool, List[Dict[str, object]], Optional[str]]:
    fixes: List[Dict[str, object]] = []
    roadmap = repo / "ROADMAP.md"

    if not roadmap.exists():
        write_text(roadmap, ROADMAP_DEFAULT_TEMPLATE)
        fixes.append(
            {
                "repo": repo.name,
                "file": str(roadmap),
                "rule": "create-missing-roadmap",
                "status": "applied",
                "reason": "created canonical checklist roadmap",
            }
        )
        return True, fixes, None

    before = read_text(roadmap)
    after = ensure_roadmap_apply_shape(before)
    if after == before:
        return False, fixes, "no bounded roadmap fix applied"

    write_text(roadmap, after)
    fixes.append(
        {
            "repo": repo.name,
            "file": str(roadmap),
            "rule": "normalize-roadmap-structure",
            "status": "applied",
            "reason": "normalized roadmap to checklist structure",
        }
    )
    return True, fixes, None


def check_cross_doc_consistency(repo: Path, readme_text: Optional[str], roadmap_text: Optional[str]) -> List[Issue]:
    issues: List[Issue] = []
    if not readme_text or not roadmap_text:
        return issues

    sanitized_readme = readme_text
    sanitized_roadmap = re.sub(
        r"Rename the skill surface from `maintain-skills-readme` to `maintain-plugin-docs`\.",
        "",
        roadmap_text,
    )

    if "maintain-skills-readme" in sanitized_readme or "maintain-skills-readme" in sanitized_roadmap:
        issues.append(
            Issue(
                issue_id="cross-doc-legacy-skill-name",
                category="cross-doc-violation",
                severity="medium",
                repo=repo.name,
                doc_file=str(repo),
                evidence="Legacy skill name `maintain-skills-readme` still appears in current docs.",
                recommended_fix="Rename legacy references to `maintain-plugin-docs`.",
                auto_fixable=False,
            )
        )

    skill_dirs = find_skill_dirs(repo)
    for skill in skill_dirs:
        if skill not in readme_text:
            issues.append(
                Issue(
                    issue_id=f"cross-doc-readme-missing-skill-{skill}",
                    category="cross-doc-violation",
                    severity="medium",
                    repo=repo.name,
                    doc_file=str(repo / "README.md"),
                    evidence=f"README does not mention active skill `{skill}`.",
                    recommended_fix="Keep the README active skill inventory aligned with the real skill directories.",
                    auto_fixable=False,
                )
            )
        if skill not in roadmap_text:
            issues.append(
                Issue(
                    issue_id=f"cross-doc-roadmap-missing-skill-{skill}",
                    category="cross-doc-violation",
                    severity="medium",
                    repo=repo.name,
                    doc_file=str(repo / "ROADMAP.md"),
                    evidence=f"ROADMAP does not mention active skill `{skill}`.",
                    recommended_fix="Mention every active skill somewhere in the roadmap or milestone plan.",
                    auto_fixable=False,
                )
            )

    if "## Milestone 1: `maintain-plugin-docs` evolution" in roadmap_text:
        if "Current implementation:" not in readme_text or "Intended scope:" not in readme_text:
            issues.append(
                Issue(
                    issue_id="cross-doc-scope-wording",
                    category="cross-doc-violation",
                    severity="medium",
                    repo=repo.name,
                    doc_file=str(repo),
                    evidence="ROADMAP tracks current-versus-planned `maintain-plugin-docs` scope, but README does not present both `Current implementation` and `Intended scope` wording.",
                    recommended_fix="Keep README and ROADMAP aligned about current versus planned docs-maintainer scope.",
                    auto_fixable=False,
                )
            )

    install_range = find_section_line_range(readme_text.splitlines(), r"^##\s+Install\s*$")
    has_codex_plugin = any(repo.glob("plugins/*/.codex-plugin/plugin.json"))
    has_claude_plugin = any(repo.glob("plugins/*/.claude-plugin/plugin.json"))
    if install_range is not None and (has_codex_plugin or has_claude_plugin):
        start_idx, end_idx = install_range
        install_text = "\n".join(readme_text.splitlines()[start_idx:end_idx])
        codex_pos = install_text.find("Codex Plugin")
        claude_pos = install_text.find("Claude Code Plugin")
        cli_pos = install_text.find("Vercel `skills` CLI")
        if has_codex_plugin and codex_pos == -1:
            issues.append(
                Issue(
                    issue_id="cross-doc-missing-codex-plugin-install",
                    category="cross-doc-violation",
                    severity="medium",
                    repo=repo.name,
                    doc_file=str(repo / "README.md"),
                    evidence="README install section does not document the Codex Plugin install surface.",
                    recommended_fix="Lead the install section with Codex Plugin guidance before secondary CLI installs.",
                    auto_fixable=False,
                )
            )
        if has_claude_plugin and claude_pos == -1:
            issues.append(
                Issue(
                    issue_id="cross-doc-missing-claude-plugin-install",
                    category="cross-doc-violation",
                    severity="medium",
                    repo=repo.name,
                    doc_file=str(repo / "README.md"),
                    evidence="README install section does not document the Claude Code Plugin install surface.",
                    recommended_fix="Lead the install section with Claude Code Plugin guidance before secondary CLI installs.",
                    auto_fixable=False,
                )
            )
        primary_positions = [pos for pos in (codex_pos, claude_pos) if pos != -1]
        if cli_pos != -1 and primary_positions and cli_pos < min(primary_positions):
            issues.append(
                Issue(
                    issue_id="cross-doc-install-priority",
                    category="cross-doc-violation",
                    severity="medium",
                    repo=repo.name,
                    doc_file=str(repo / "README.md"),
                    evidence="README install section presents the Vercel `skills` CLI before the primary Codex/Claude plugin install surfaces.",
                    recommended_fix="Document Codex Plugin and Claude Code Plugin installs before secondary Vercel `skills` CLI examples.",
                    auto_fixable=False,
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

    lines.append("## Discovery Summary")
    lines.append(f"- Repos scanned: {len(report['repos_scanned'])}")
    lines.append(f"- Repos with issues: {len(report['repos_with_issues'])}")
    lines.append("")

    lines.append("## Profile Assignments")
    for name, profile in sorted(report["profile_assignments"].items()):
        lines.append(f"- {name}: {profile}")
    lines.append("")

    lines.append("## README Findings")
    if not report["readme_findings"]:
        lines.append("- None")
    else:
        for i in report["readme_findings"]:
            lines.append(f"- [{i['severity']}] {i['repo']}: {i['evidence']}")
    lines.append("")

    lines.append("## ROADMAP Findings")
    if not report["roadmap_findings"]:
        lines.append("- None")
    else:
        for i in report["roadmap_findings"]:
            lines.append(f"- [{i['severity']}] {i['repo']}: {i['evidence']}")
    lines.append("")

    lines.append("## Cross-Doc Findings")
    if not report["cross_doc_findings"]:
        lines.append("- None")
    else:
        for i in report["cross_doc_findings"]:
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
    readme_findings: List[Issue] = []
    roadmap_findings: List[Issue] = []
    cross_doc_findings: List[Issue] = []
    errors: List[Dict[str, str]] = []
    fixes_applied: List[Dict[str, object]] = []
    wants_readme = args.doc_scope in {"readme", "all"}
    wants_roadmap = args.doc_scope in {"roadmap", "all"}

    for repo in repos:
        profile = detect_profile(repo)
        profile_assignments[repo.name] = profile

        readme = repo / "README.md"
        roadmap = repo / "ROADMAP.md"
        skill_dirs = find_skill_dirs(repo)
        readme_text: Optional[str] = None
        roadmap_text: Optional[str] = None

        if wants_readme:
            if not readme.exists():
                readme_findings.append(
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
            else:
                readme_text = read_text(readme)
                readme_findings.extend(check_sections(repo, profile, readme_text))
                readme_findings.extend(find_todo_issues(repo, readme_text))
                readme_findings.extend(check_links(repo, readme_text))
                readme_findings.extend(check_commands(repo, profile, readme_text, skill_dirs))

        if wants_roadmap:
            if not roadmap.exists():
                roadmap_findings.append(
                    Issue(
                        issue_id="missing-roadmap",
                        category="roadmap-violation",
                        severity="high",
                        repo=repo.name,
                        doc_file=str(roadmap),
                        evidence="ROADMAP.md is missing.",
                        recommended_fix="Create a canonical checklist-style roadmap.",
                        auto_fixable=True,
                    )
                )
            else:
                roadmap_text = read_text(roadmap)
                roadmap_findings.extend(validate_roadmap(repo, roadmap_text))

        if wants_readme and wants_roadmap:
            if readme_text is None and readme.exists():
                readme_text = read_text(readme)
            if roadmap_text is None and roadmap.exists():
                roadmap_text = read_text(roadmap)
            cross_doc_findings.extend(check_cross_doc_consistency(repo, readme_text, roadmap_text))

    initial_unresolved = len(readme_findings) + len(roadmap_findings) + len(cross_doc_findings)

    if args.apply_fixes:
        for repo in repos:
            profile = profile_assignments[repo.name]
            skill_dirs = find_skill_dirs(repo)
            try:
                if wants_readme:
                    changed, fixes, reason = apply_fixes_for_repo(repo, profile, skill_dirs)
                    if fixes:
                        fixes_applied.extend(fixes)
                    elif reason:
                        fixes_applied.append({"repo": repo.name, "file": str(repo / "README.md"), "rule": "no-op", "status": "skipped", "reason": reason})
                    if changed:
                        readme = repo / "README.md"
                        text = read_text(readme)
                        readme_findings = [i for i in readme_findings if i.repo != repo.name]
                        readme_findings.extend(check_sections(repo, profile, text))
                        readme_findings.extend(find_todo_issues(repo, text))
                        readme_findings.extend(check_links(repo, text))
                        readme_findings.extend(check_commands(repo, profile, text, skill_dirs))

                if wants_roadmap:
                    changed, fixes, reason = apply_fixes_for_roadmap(repo)
                    if fixes:
                        fixes_applied.extend(fixes)
                    elif reason:
                        fixes_applied.append({"repo": repo.name, "file": str(repo / "ROADMAP.md"), "rule": "no-op", "status": "skipped", "reason": reason})
                    if changed:
                        roadmap = repo / "ROADMAP.md"
                        text = read_text(roadmap)
                        roadmap_findings = [i for i in roadmap_findings if i.repo != repo.name]
                        roadmap_findings.extend(validate_roadmap(repo, text))

                if wants_readme and wants_roadmap:
                    cross_doc_findings = [i for i in cross_doc_findings if i.repo != repo.name]
                    readme_text = read_text(repo / "README.md") if (repo / "README.md").exists() else None
                    roadmap_text = read_text(repo / "ROADMAP.md") if (repo / "ROADMAP.md").exists() else None
                    cross_doc_findings.extend(check_cross_doc_consistency(repo, readme_text, roadmap_text))
            except Exception as exc:
                errors.append({"repo": repo.name, "message": f"fix error: {exc}"})

    unresolved = len(readme_findings) + len(roadmap_findings) + len(cross_doc_findings)

    repos_with_issues = sorted({i.repo for i in readme_findings + roadmap_findings + cross_doc_findings})

    report: Dict[str, object] = {
        "run_context": {
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "workspace": str(workspace),
            "repo_glob": args.repo_glob,
            "doc_scope": args.doc_scope,
            "apply_fixes": args.apply_fixes,
            "exclusions": [str(e) for e in excludes],
        },
        "repos_scanned": [str(r) for r in repos],
        "profile_assignments": profile_assignments,
        "readme_findings": [i.to_dict() for i in readme_findings],
        "roadmap_findings": [i.to_dict() for i in roadmap_findings],
        "cross_doc_findings": [i.to_dict() for i in cross_doc_findings],
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
