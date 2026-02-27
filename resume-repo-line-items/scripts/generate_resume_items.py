#!/usr/bin/env python3
"""Generate plaintext resume line items from scan_repos.py JSON output.

This script is deterministic and read-only.
It uses repository metadata and file markers to create professional bullet points.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

SUMMARY_FALLBACK = "Built and maintained a production-oriented software project with release discipline and practical engineering standards."

TOOL_PRIORITY = [
    "TypeScript",
    "Python",
    "Go",
    "Rust",
    "Swift",
    "Node.js",
    "Astro",
    "Next.js",
    "FastAPI",
    "Docker",
    "GitHub Actions",
    "Terraform",
    "pnpm",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate plaintext resume entries from scan JSON.")
    parser.add_argument("--scan-json", required=True, help="Path to scan_repos.py output JSON")
    parser.add_argument(
        "--include-unselected",
        action="store_true",
        help="Include repos that did not pass selection (useful for debugging).",
    )
    parser.add_argument(
        "--max-repos",
        type=int,
        default=0,
        help="Maximum number of repos to include (0 means all).",
    )
    parser.add_argument("--output", default="", help="Write plaintext output to a file")
    return parser.parse_args()


def load_scan(path: str) -> dict[str, Any]:
    return json.loads(Path(path).expanduser().read_text())


def top_languages(repo: dict[str, Any], limit: int = 3) -> list[str]:
    return [item["language"] for item in repo.get("languages", [])[:limit]]


def prioritized_tools(repo: dict[str, Any]) -> list[str]:
    markers = list(repo.get("tech_markers", []))
    languages = top_languages(repo, limit=4)
    combined = markers + languages

    deduped = []
    seen = set()
    for tool in combined:
        if tool not in seen:
            deduped.append(tool)
            seen.add(tool)

    ranked = sorted(
        deduped,
        key=lambda tool: TOOL_PRIORITY.index(tool) if tool in TOOL_PRIORITY else len(TOOL_PRIORITY) + 10,
    )
    return ranked[:5]


def choose_primary_tool(repo: dict[str, Any]) -> str:
    tools = prioritized_tools(repo)
    if tools:
        return tools[0]
    langs = top_languages(repo, limit=1)
    if langs:
        return langs[0]
    return "modern software tooling"


def build_summary(repo: dict[str, Any]) -> str:
    tools = prioritized_tools(repo)
    latest_tag = repo.get("latest_tag") or "a tagged release"

    if tools:
        tool_text = ", ".join(tools[:3])
        return (
            f"Delivered and released {repo['name']} using {tool_text}, "
            f"with repeatable delivery reflected in {latest_tag}."
        )

    return SUMMARY_FALLBACK


def bullet_delivery(repo: dict[str, Any]) -> str:
    primary = choose_primary_tool(repo)
    tag = repo.get("latest_tag") or "a tagged release"
    return (
        f"Implemented core features with {primary} to solve concrete product requirements. "
        f"Delivered the work through versioned releases, culminating in {tag}, so changes were easier to adopt and trust."
    )


def bullet_quality(repo: dict[str, Any]) -> str:
    markers = set(repo.get("tech_markers", []))

    if "GitHub Actions" in markers:
        return (
            "Set up GitHub Actions workflows to automate validation before release. "
            "Reduced manual QA overhead and improved confidence in merge and release decisions."
        )

    if "Docker" in markers or "Docker Compose" in markers:
        return (
            "Containerized the runtime with Docker to standardize local and deployment environments. "
            "Lowered setup friction and improved reliability across machines and stages."
        )

    return (
        "Applied structured engineering practices around testing, review, and release readiness. "
        "Raised implementation quality and reduced the chance of regressions in shipped changes."
    )


def bullet_architecture(repo: dict[str, Any]) -> str:
    tools = prioritized_tools(repo)
    if len(tools) >= 2:
        pair = f"{tools[0]} and {tools[1]}"
    elif tools:
        pair = tools[0]
    else:
        pair = "an appropriate project stack"

    return (
        f"Designed and iterated the project architecture with {pair} to keep development velocity high as scope expanded. "
        "Enabled faster feature iteration while preserving maintainability."
    )


def bullet_collaboration(repo: dict[str, Any]) -> str:
    contributors = repo.get("external_contributors", [])
    if contributors:
        count = len(contributors)
        return (
            f"Collaborated with {count} external contributor(s) through scoped implementation plans, review cycles, and shared coding standards. "
            "Improved team throughput and kept quality consistent across parallel changes."
        )

    return (
        "Worked in a collaborative codebase with clear conventions and shared ownership boundaries. "
        "Kept delivery predictable by aligning implementation details with team expectations."
    )


def bullet_leadership() -> str:
    return (
        "Led technical direction for selected features by breaking work into clear milestones and unblocking contributors during execution. "
        "Improved delivery predictability and reduced cycle time for high-priority changes."
    )


def bullet_communication() -> str:
    return (
        "Communicated tradeoffs, status, and release implications in concise updates to keep collaborators aligned on priorities and risks. "
        "Enabled faster decisions and smoother handoffs across the team."
    )


def build_bullets(repo: dict[str, Any], collaborative_rank: int) -> list[str]:
    bullets = [
        bullet_delivery(repo),
        bullet_architecture(repo),
        bullet_quality(repo),
    ]

    if repo.get("collaborative"):
        bullets.append(bullet_collaboration(repo))
        bullets.append(bullet_leadership())
        if collaborative_rank % 3 == 0:
            bullets.append(bullet_communication())

    return bullets[:6]


def render_repo_section(repo: dict[str, Any], collaborative_rank: int) -> str:
    marker = " [Collaborative]" if repo.get("collaborative") else ""
    summary = build_summary(repo)
    bullets = build_bullets(repo, collaborative_rank)

    lines = [f"{repo['name']}{marker}", summary]
    for bullet in bullets:
        lines.append(f"- {bullet}")
    return "\n".join(lines)


def generate_text(scan: dict[str, Any], include_unselected: bool, max_repos: int) -> str:
    repos = scan.get("repos", [])

    if not include_unselected:
        repos = [repo for repo in repos if repo.get("selected")]

    repos = sorted(repos, key=lambda repo: repo.get("last_commit_date", ""), reverse=True)
    if max_repos:
        repos = repos[:max_repos]

    if not repos:
        return "No qualifying repositories were found for the provided scan criteria.\n"

    sections = []
    collaborative_rank = 0

    for repo in repos:
        if repo.get("collaborative"):
            collaborative_rank += 1
        sections.append(render_repo_section(repo, collaborative_rank))

    return "\n\n".join(sections).strip() + "\n"


def main() -> int:
    args = parse_args()
    scan = load_scan(args.scan_json)
    text = generate_text(scan, args.include_unselected, args.max_repos)

    if args.output:
        Path(args.output).expanduser().write_text(text)
        print(f"[OK] Wrote resume line items: {args.output}")
    else:
        print(text, end="")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
