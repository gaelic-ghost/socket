#!/usr/bin/env python3
"""Scan local git repositories and select resume-qualified projects.

Selection criteria:
- Repository is under the target root.
- At least one remote points to the specified GitHub owner(s).
- Repository has at least one git tag.
- Repository is not a fork (via GitHub metadata when enabled).

This script is read-only. It does not modify repositories.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SKIP_DIRS = {
    ".git",
    "node_modules",
    ".venv",
    "venv",
    "dist",
    "build",
    ".next",
    ".cache",
}

LANGUAGE_EXTENSIONS = {
    ".py": "Python",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".js": "JavaScript",
    ".jsx": "JavaScript",
    ".go": "Go",
    ".rs": "Rust",
    ".swift": "Swift",
    ".java": "Java",
    ".kt": "Kotlin",
    ".sql": "SQL",
    ".tf": "Terraform",
    ".sh": "Shell",
    ".yml": "YAML",
    ".yaml": "YAML",
    ".json": "JSON",
    ".html": "HTML",
    ".css": "CSS",
    ".md": "Markdown",
}

GITHUB_PATTERNS = [
    re.compile(r"^git@github\.com:(?P<owner>[^/]+)/(?P<repo>[^/]+?)(?:\.git)?$"),
    re.compile(r"^https://github\.com/(?P<owner>[^/]+)/(?P<repo>[^/]+?)(?:\.git)?$"),
    re.compile(r"^ssh://git@github\.com/(?P<owner>[^/]+)/(?P<repo>[^/]+?)(?:\.git)?$"),
]


@dataclass
class GitHubRemote:
    remote: str
    url: str
    owner: str
    repo: str


def run(cmd: list[str], cwd: Path | None = None) -> tuple[int, str, str]:
    proc = subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        text=True,
        capture_output=True,
        check=False,
    )
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scan repos and select resume targets.")
    parser.add_argument(
        "--root",
        default="~/Workspace",
        help="Root directory to scan (default: ~/Workspace)",
    )
    parser.add_argument(
        "--github-owner",
        action="append",
        default=[],
        help="GitHub owner/user to treat as 'my GitHub'. Repeatable.",
    )
    parser.add_argument(
        "--fork-check",
        choices=["github", "none"],
        default="github",
        help="How to classify forks: github API lookup or skip lookup (default: github)",
    )
    parser.add_argument(
        "--max-repos",
        type=int,
        default=0,
        help="Optional cap on discovered repos (0 means no cap).",
    )
    parser.add_argument(
        "--output",
        default="",
        help="Write JSON output to this file. Defaults to stdout.",
    )
    return parser.parse_args()


def normalize_owner_list(raw: list[str]) -> list[str]:
    owners: list[str] = []
    seen = set()
    for item in raw:
        for piece in item.split(","):
            owner = piece.strip()
            if owner and owner not in seen:
                owners.append(owner)
                seen.add(owner)
    return owners


def infer_owners(explicit: list[str]) -> list[str]:
    if explicit:
        return explicit

    inferred: list[str] = []
    seen = set()

    for env_key in ("GITHUB_USER", "GH_USERNAME", "GITHUB_OWNER"):
        value = os.environ.get(env_key, "").strip()
        if value and value not in seen:
            inferred.append(value)
            seen.add(value)

    code, out, _ = run(["gh", "api", "user", "--jq", ".login"])
    if code == 0 and out and out not in seen:
        inferred.append(out)
        seen.add(out)

    return inferred


def discover_git_repos(root: Path, max_repos: int = 0) -> list[Path]:
    repos: list[Path] = []
    for current_root, dirs, files in os.walk(root):
        current = Path(current_root)

        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]

        if ".git" in dirs or ".git" in files:
            repos.append(current)
            dirs[:] = []
            if max_repos and len(repos) >= max_repos:
                break

    return sorted(repos)


def parse_github_remote(url: str) -> tuple[str, str] | None:
    clean = url.strip()
    for pattern in GITHUB_PATTERNS:
        match = pattern.match(clean)
        if match:
            owner = match.group("owner")
            repo = match.group("repo")
            return owner, repo
    return None


def get_github_remotes(repo: Path) -> list[GitHubRemote]:
    code, out, _ = run(["git", "-C", str(repo), "remote", "-v"])
    if code != 0:
        return []

    remotes: list[GitHubRemote] = []
    seen = set()

    for line in out.splitlines():
        parts = line.split()
        if len(parts) < 3:
            continue
        remote_name, remote_url, remote_kind = parts[0], parts[1], parts[2]
        if remote_kind != "(fetch)":
            continue
        parsed = parse_github_remote(remote_url)
        if not parsed:
            continue
        owner, repo_name = parsed
        key = (remote_name, remote_url, owner, repo_name)
        if key in seen:
            continue
        seen.add(key)
        remotes.append(
            GitHubRemote(
                remote=remote_name,
                url=remote_url,
                owner=owner,
                repo=repo_name,
            )
        )

    return remotes


def get_tags(repo: Path) -> list[str]:
    code, out, _ = run(["git", "-C", str(repo), "tag", "--list"])
    if code != 0 or not out:
        return []
    return [line.strip() for line in out.splitlines() if line.strip()]


def get_latest_tag(repo: Path) -> str:
    code, out, _ = run(["git", "-C", str(repo), "describe", "--tags", "--abbrev=0"])
    if code == 0 and out:
        return out
    tags = get_tags(repo)
    return tags[-1] if tags else ""


def get_default_branch(repo: Path) -> str:
    code, out, _ = run(["git", "-C", str(repo), "rev-parse", "--abbrev-ref", "HEAD"])
    if code == 0 and out:
        return out
    return "HEAD"


def get_last_commit_date(repo: Path) -> str:
    code, out, _ = run(["git", "-C", str(repo), "log", "-1", "--format=%cI"])
    if code == 0 and out:
        return out
    return ""


def is_fork_via_github(owner: str, repo: str) -> tuple[str, str]:
    code, out, err = run(["gh", "repo", "view", f"{owner}/{repo}", "--json", "isFork", "--jq", ".isFork"])
    if code != 0:
        reason = err or "gh repo view failed"
        return "unknown", reason
    normalized = out.strip().lower()
    if normalized == "true":
        return "fork", "GitHub repo metadata reports isFork=true"
    if normalized == "false":
        return "not_fork", "GitHub repo metadata reports isFork=false"
    return "unknown", f"Unexpected gh output: {out!r}"


def gather_self_identities() -> dict[str, set[str]]:
    names: set[str] = set()
    emails: set[str] = set()

    code, out, _ = run(["git", "config", "--global", "--get", "user.name"])
    if code == 0 and out:
        names.add(out.strip().lower())

    code, out, _ = run(["git", "config", "--global", "--get", "user.email"])
    if code == 0 and out:
        emails.add(out.strip().lower())

    gh_owners = infer_owners([])
    for owner in gh_owners:
        names.add(owner.lower())
        emails.add(f"{owner.lower()}@users.noreply.github.com")

    return {"names": names, "emails": emails}


def parse_shortlog(repo: Path) -> list[dict[str, Any]]:
    code, out, _ = run(["git", "-C", str(repo), "shortlog", "-sne", "--all"])
    if code != 0 or not out:
        return []

    contributors: list[dict[str, Any]] = []
    pattern = re.compile(r"^\s*(\d+)\s+(.+?)\s+<(.+)>\s*$")

    for line in out.splitlines():
        match = pattern.match(line)
        if not match:
            continue
        commits = int(match.group(1))
        name = match.group(2).strip()
        email = match.group(3).strip()
        contributors.append({"name": name, "email": email, "commits": commits})

    return contributors


def classify_collaboration(repo: Path, self_id: dict[str, set[str]]) -> tuple[bool, list[str], list[dict[str, Any]]]:
    reasons: list[str] = []
    contributors = parse_shortlog(repo)

    non_self = []
    for contributor in contributors:
        name = contributor["name"].lower()
        email = contributor["email"].lower()
        if name in self_id["names"] or email in self_id["emails"]:
            continue
        non_self.append(contributor)

    if non_self:
        reasons.append("multiple contributors")

    if (repo / "AGENTS.md").exists():
        reasons.append("AGENTS.md present")

    return bool(reasons), reasons, non_self


def detect_languages(repo: Path) -> list[dict[str, Any]]:
    counts: dict[str, int] = {}

    for current_root, dirs, files in os.walk(repo):
        current = Path(current_root)
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]

        if current != repo and ".git" in dirs:
            dirs[:] = []
            continue

        for filename in files:
            path = current / filename
            suffix = path.suffix.lower()
            lang = LANGUAGE_EXTENSIONS.get(suffix)
            if not lang:
                continue
            counts[lang] = counts.get(lang, 0) + 1

    ranked = sorted(counts.items(), key=lambda item: item[1], reverse=True)
    return [{"language": language, "files": count} for language, count in ranked[:8]]


def detect_tech_markers(repo: Path) -> list[str]:
    markers = []
    marker_map = [
        ("package.json", "Node.js"),
        ("pnpm-lock.yaml", "pnpm"),
        ("tsconfig.json", "TypeScript"),
        ("astro.config.mjs", "Astro"),
        ("next.config.js", "Next.js"),
        ("requirements.txt", "Python"),
        ("pyproject.toml", "Python"),
        ("Dockerfile", "Docker"),
        ("docker-compose.yml", "Docker Compose"),
        ("docker-compose.yaml", "Docker Compose"),
        ("go.mod", "Go"),
        ("Cargo.toml", "Rust"),
        ("Package.swift", "Swift"),
        (".github/workflows", "GitHub Actions"),
        ("terraform", "Terraform"),
    ]

    for relative, label in marker_map:
        if (repo / relative).exists():
            markers.append(label)

    pyproject = repo / "pyproject.toml"
    if pyproject.exists():
        text = pyproject.read_text(errors="ignore").lower()
        if "fastapi" in text and "FastAPI" not in markers:
            markers.append("FastAPI")
        if "uvicorn" in text and "uvicorn" not in markers:
            markers.append("uvicorn")
        if "pydantic" in text and "Pydantic" not in markers:
            markers.append("Pydantic")

    package_json = repo / "package.json"
    if package_json.exists():
        text = package_json.read_text(errors="ignore").lower()
        if '"react"' in text and "React" not in markers:
            markers.append("React")
        if '"astro"' in text and "Astro" not in markers:
            markers.append("Astro")

    return markers


def build_repo_record(repo: Path, owners: list[str], fork_check: str, self_id: dict[str, set[str]]) -> dict[str, Any]:
    github_remotes = get_github_remotes(repo)
    remote_owners = sorted({r.owner for r in github_remotes})

    owner_match = bool(set(remote_owners).intersection(set(owners))) if owners else False
    tags = get_tags(repo)

    fork_status = "skipped"
    fork_reason = "fork check skipped"
    selected = True
    exclusion_reasons: list[str] = []

    preferred_remote = github_remotes[0] if github_remotes else None

    if not github_remotes:
        selected = False
        exclusion_reasons.append("no GitHub remote")

    if not owners:
        selected = False
        exclusion_reasons.append("could not infer GitHub owner; pass --github-owner")
    elif not owner_match:
        selected = False
        exclusion_reasons.append("no GitHub remote owned by configured owner(s)")

    if not tags:
        selected = False
        exclusion_reasons.append("no git tags found")

    if fork_check == "github" and preferred_remote is not None:
        fork_status, fork_reason = is_fork_via_github(preferred_remote.owner, preferred_remote.repo)
        if fork_status == "fork":
            selected = False
            exclusion_reasons.append("repository is a fork")
        elif fork_status == "unknown":
            selected = False
            exclusion_reasons.append("fork status unknown (gh lookup failed)")
    elif fork_check == "none":
        fork_status = "unchecked"
        fork_reason = "fork check disabled"

    collaborative, collaboration_reasons, external_contributors = classify_collaboration(repo, self_id)

    return {
        "name": repo.name,
        "path": str(repo),
        "default_branch": get_default_branch(repo),
        "last_commit_date": get_last_commit_date(repo),
        "github_remotes": [r.__dict__ for r in github_remotes],
        "remote_owners": remote_owners,
        "owner_match": owner_match,
        "tag_count": len(tags),
        "latest_tag": get_latest_tag(repo),
        "fork_status": fork_status,
        "fork_reason": fork_reason,
        "selected": selected,
        "exclusion_reasons": exclusion_reasons,
        "collaborative": collaborative,
        "collaboration_reasons": collaboration_reasons,
        "external_contributors": external_contributors,
        "languages": detect_languages(repo),
        "tech_markers": detect_tech_markers(repo),
    }


def main() -> int:
    args = parse_args()
    root = Path(args.root).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        print(f"[ERROR] Scan root does not exist: {root}", file=sys.stderr)
        return 1

    owners = infer_owners(normalize_owner_list(args.github_owner))
    self_id = gather_self_identities()

    repos = discover_git_repos(root, max_repos=args.max_repos)

    records = [build_repo_record(repo, owners, args.fork_check, self_id) for repo in repos]

    selected_count = sum(1 for record in records if record["selected"])
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "scan_root": str(root),
        "github_owners": owners,
        "fork_check": args.fork_check,
        "repo_count": len(records),
        "selected_repo_count": selected_count,
        "repos": records,
    }

    output = json.dumps(payload, indent=2)
    if args.output:
        Path(args.output).expanduser().write_text(output + "\n")
        print(f"[OK] Wrote scan report: {args.output}")
    else:
        print(output)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
