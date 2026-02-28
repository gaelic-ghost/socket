#!/usr/bin/env python3
"""Two-pass docs alignment audit and safe-fix maintainer for multi-repo workspaces."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

DOC_BASENAMES = {"README.md", "ROADMAP.md", "CONTRIBUTING.md"}
DOC_EXT = ".md"


@dataclass
class Issue:
    issue_id: str
    category: str
    severity: str
    language_scope: str
    doc_file: str
    evidence: str
    recommended_fix: str
    auto_fixable: bool
    fixed: bool = False

    def to_dict(self) -> Dict[str, object]:
        return {
            "issue_id": self.issue_id,
            "category": self.category,
            "severity": self.severity,
            "language_scope": self.language_scope,
            "doc_file": self.doc_file,
            "evidence": self.evidence,
            "recommended_fix": self.recommended_fix,
            "auto_fixable": self.auto_fixable,
            "fixed": self.fixed,
        }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit and optionally apply safe documentation alignment fixes across repositories."
    )
    parser.add_argument("--workspace", required=True, help="Workspace root to scan")
    parser.add_argument("--exclude", action="append", default=[], help="Path to exclude (repeatable)")
    parser.add_argument("--exclude-file", help="File with newline-separated paths to exclude")
    parser.add_argument("--apply-fixes", action="store_true", help="Apply safe targeted fixes")
    parser.add_argument("--max-repos", type=int, default=0, help="Optional cap on discovered repos")
    parser.add_argument("--json-out", help="Write JSON report to this path")
    parser.add_argument("--md-out", help="Write Markdown report to this path")
    parser.add_argument("--print-json", action="store_true", help="Print JSON report to stdout")
    parser.add_argument("--print-md", action="store_true", help="Print Markdown report to stdout")
    parser.add_argument(
        "--fail-on-issues",
        action="store_true",
        help="Exit non-zero when unresolved issues remain after checks/fixes",
    )
    return parser.parse_args()


def read_excludes(args: argparse.Namespace) -> List[Path]:
    excludes: List[Path] = []
    raw_paths: List[str] = list(args.exclude)

    if args.exclude_file:
        file_path = Path(args.exclude_file).expanduser()
        if file_path.exists():
            for line in file_path.read_text(encoding="utf-8").splitlines():
                candidate = line.strip()
                if candidate and not candidate.startswith("#"):
                    raw_paths.append(candidate)

    seen: set[str] = set()
    for raw in raw_paths:
        resolved = Path(raw).expanduser().resolve()
        key = str(resolved)
        if key not in seen:
            excludes.append(resolved)
            seen.add(key)
    return excludes


def path_is_excluded(path: Path, excludes: Sequence[Path]) -> bool:
    try:
        resolved = path.resolve()
    except OSError:
        return False
    for excluded in excludes:
        try:
            resolved.relative_to(excluded)
            return True
        except ValueError:
            continue
    return False


def discover_repos(workspace: Path, excludes: Sequence[Path], max_repos: int) -> List[Path]:
    repos: List[Path] = []

    for root, dirs, _files in os.walk(workspace, topdown=True):
        root_path = Path(root)

        if path_is_excluded(root_path, excludes):
            dirs[:] = []
            continue

        dirs[:] = [
            d
            for d in dirs
            if d not in {".git", ".hg", ".svn"} and not path_is_excluded(root_path / d, excludes)
        ]

        is_repo = (root_path / ".git").exists()
        if is_repo:
            repos.append(root_path)
            dirs[:] = []
            if max_repos > 0 and len(repos) >= max_repos:
                break

    return sorted(set(repos))


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="ignore")


def detect_signals(repo: Path) -> Dict[str, object]:
    package_json = repo / "package.json"
    signals: Dict[str, object] = {
        "swift": (repo / "Package.swift").exists() or bool(list(repo.glob("*.xcodeproj"))) or bool(list(repo.glob("*.xcworkspace"))),
        "rust": (repo / "Cargo.toml").exists(),
        "python": (repo / "pyproject.toml").exists()
        or (repo / "uv.lock").exists()
        or (repo / ".python-version").exists()
        or bool(list(repo.glob("requirements*.txt"))),
        "js": package_json.exists(),
        "ts": (repo / "tsconfig.json").exists(),
        "prefer_uv": (repo / "uv.lock").exists(),
        "has_tests": (repo / "tests").exists() or (repo / "test").exists(),
        "canonical_js_manager": infer_js_manager(repo),
    }
    return signals


def infer_js_manager(repo: Path) -> str:
    if (repo / "pnpm-lock.yaml").exists():
        return "pnpm"
    if (repo / "package-lock.json").exists():
        return "npm"
    if (repo / "yarn.lock").exists():
        return "yarn"
    return "unknown"


def collect_doc_files(repo: Path) -> List[Path]:
    docs: List[Path] = []
    for base in DOC_BASENAMES:
        candidate = repo / base
        if candidate.is_file():
            docs.append(candidate)

    docs_dir = repo / "docs"
    if docs_dir.exists():
        docs.extend(sorted(p for p in docs_dir.rglob("*.md") if p.is_file()))

    setup_docs = [
        p
        for p in repo.glob("*.md")
        if p.is_file() and p.name.lower().startswith(("setup", "install", "getting-started"))
    ]
    docs.extend(sorted(setup_docs))

    return sorted(set(docs))


def quickstart_for_signals(signals: Dict[str, object]) -> Optional[str]:
    if signals["js"] and signals["canonical_js_manager"] != "unknown":
        mgr = str(signals["canonical_js_manager"])
        if mgr == "pnpm":
            return "## Development Quickstart\n\n```bash\npnpm install\npnpm run test\n```\n"
        if mgr == "npm":
            return "## Development Quickstart\n\n```bash\nnpm install\nnpm run test\n```\n"
        if mgr == "yarn":
            return "## Development Quickstart\n\n```bash\nyarn install\nyarn test\n```\n"
    if signals["python"] and signals["prefer_uv"]:
        return "## Development Quickstart\n\n```bash\nuv sync\nuv run pytest\n```\n"
    if signals["rust"]:
        return "## Development Quickstart\n\n```bash\ncargo build\ncargo test\n```\n"
    if signals["swift"]:
        return "## Development Quickstart\n\n```bash\nswift build\nswift test\n```\n"
    return None


def has_quickstart(texts: Iterable[str]) -> bool:
    lowered = "\n".join(texts).lower()
    return "development quickstart" in lowered or "getting started" in lowered


def id_for(repo: Path, category: str, doc_file: Path, index: int) -> str:
    seed = f"{repo}:{category}:{doc_file}:{index}"
    digest = abs(hash(seed)) % 100000
    return f"{category}-{digest:05d}"


def detect_issues(repo: Path, signals: Dict[str, object], docs: List[Path]) -> List[Issue]:
    issues: List[Issue] = []
    docs_text: Dict[Path, str] = {doc: read_text(doc) for doc in docs}

    canonical_mgr = str(signals["canonical_js_manager"])
    if signals["js"] and canonical_mgr != "unknown":
        for idx, (doc, text) in enumerate(docs_text.items(), start=1):
            lowered = text.lower()
            wrong = False
            evidence = ""
            has_npm_install = bool(re.search(r"\bnpm\s+install\b", lowered))
            has_npm_run = bool(re.search(r"\bnpm\s+run\b", lowered))
            has_pnpm = bool(re.search(r"\bpnpm\b", lowered))
            if canonical_mgr == "pnpm" and (has_npm_install or has_npm_run):
                wrong = True
                evidence = "Doc uses npm commands while lockfile indicates pnpm."
            elif canonical_mgr == "npm" and has_pnpm:
                wrong = True
                evidence = "Doc uses pnpm commands while lockfile indicates npm."
            elif canonical_mgr == "yarn" and (has_npm_install or has_npm_run or has_pnpm):
                wrong = True
                evidence = "Doc uses npm/pnpm commands while lockfile indicates yarn."

            if wrong:
                issues.append(
                    Issue(
                        issue_id=id_for(repo, "js-package-manager-mismatch", doc, idx),
                        category="js-package-manager-mismatch",
                        severity="high",
                        language_scope="js-ts",
                        doc_file=str(doc),
                        evidence=evidence,
                        recommended_fix=f"Replace command examples to use {canonical_mgr} consistently.",
                        auto_fixable=True,
                    )
                )

    if signals["python"] and signals["prefer_uv"]:
        for idx, (doc, text) in enumerate(docs_text.items(), start=1):
            lowered = text.lower()
            if "pip install" in lowered or "python -m pip" in lowered:
                issues.append(
                    Issue(
                        issue_id=id_for(repo, "python-uv-mismatch", doc, idx),
                        category="python-uv-mismatch",
                        severity="high",
                        language_scope="python",
                        doc_file=str(doc),
                        evidence="uv.lock exists but docs use pip install commands.",
                        recommended_fix="Use uv sync and uv run equivalents in docs.",
                        auto_fixable=True,
                    )
                )

    all_text = "\n".join(docs_text.values()).lower()
    readme = repo / "README.md"

    if signals["rust"]:
        if "cargo build" not in all_text:
            issues.append(
                Issue(
                    issue_id=id_for(repo, "rust-missing-build", readme, 1),
                    category="rust-missing-build",
                    severity="medium",
                    language_scope="rust",
                    doc_file=str(readme),
                    evidence="Rust repo detected, but cargo build guidance is missing in docs.",
                    recommended_fix="Add cargo build to Development Quickstart.",
                    auto_fixable=readme.is_file(),
                )
            )
        if signals["has_tests"] and "cargo test" not in all_text:
            issues.append(
                Issue(
                    issue_id=id_for(repo, "rust-missing-test", readme, 2),
                    category="rust-missing-test",
                    severity="medium",
                    language_scope="rust",
                    doc_file=str(readme),
                    evidence="Rust tests likely present, but cargo test guidance is missing.",
                    recommended_fix="Add cargo test to Development Quickstart.",
                    auto_fixable=readme.is_file(),
                )
            )

    if signals["swift"]:
        if "swift build" not in all_text:
            issues.append(
                Issue(
                    issue_id=id_for(repo, "swift-missing-build", readme, 1),
                    category="swift-missing-build",
                    severity="medium",
                    language_scope="swift",
                    doc_file=str(readme),
                    evidence="Swift project detected, but swift build guidance is missing.",
                    recommended_fix="Add swift build to Development Quickstart.",
                    auto_fixable=readme.is_file(),
                )
            )
        if "swift test" not in all_text:
            issues.append(
                Issue(
                    issue_id=id_for(repo, "swift-missing-test", readme, 2),
                    category="swift-missing-test",
                    severity="medium",
                    language_scope="swift",
                    doc_file=str(readme),
                    evidence="Swift project detected, but swift test guidance is missing.",
                    recommended_fix="Add swift test to Development Quickstart.",
                    auto_fixable=readme.is_file(),
                )
            )

    if signals["js"] or signals["python"] or signals["rust"] or signals["swift"]:
        if not has_quickstart(docs_text.values()) and readme.is_file():
            block = quickstart_for_signals(signals)
            if block:
                issues.append(
                    Issue(
                        issue_id=id_for(repo, "missing-quickstart", readme, 3),
                        category="missing-quickstart",
                        severity="medium",
                        language_scope="common",
                        doc_file=str(readme),
                        evidence="No quickstart section found in markdown docs.",
                        recommended_fix="Add concise Development Quickstart section.",
                        auto_fixable=True,
                    )
                )

    return issues


def rewrite_js_commands(text: str, canonical: str) -> Tuple[str, int]:
    before = text
    if canonical == "pnpm":
        text = re.sub(r"(?m)^\s*npm\s+install\s*$", "pnpm install", text)
        text = re.sub(r"(?m)^\s*npm\s+run\s+([a-zA-Z0-9:_-]+)\s*$", r"pnpm run \1", text)
    elif canonical == "npm":
        text = re.sub(r"(?m)^\s*pnpm\s+install\s*$", "npm install", text)
        text = re.sub(r"(?m)^\s*pnpm\s+run\s+([a-zA-Z0-9:_-]+)\s*$", r"npm run \1", text)
        text = re.sub(r"(?m)^\s*pnpm\s+([a-zA-Z0-9:_-]+)\s*$", r"npm run \1", text)
    elif canonical == "yarn":
        text = re.sub(r"(?m)^\s*npm\s+install\s*$", "yarn install", text)
        text = re.sub(r"(?m)^\s*npm\s+run\s+([a-zA-Z0-9:_-]+)\s*$", r"yarn \1", text)
        text = re.sub(r"(?m)^\s*pnpm\s+install\s*$", "yarn install", text)
        text = re.sub(r"(?m)^\s*pnpm\s+run\s+([a-zA-Z0-9:_-]+)\s*$", r"yarn \1", text)
    changes = 0 if text == before else 1
    return text, changes


def rewrite_uv_commands(text: str) -> Tuple[str, int]:
    before = text
    text = re.sub(r"(?m)^\s*(python\s+-m\s+pip|pip3?|uv\s+pip)\s+install\s+-r\s+requirements[^\n]*$", "uv sync", text)
    text = re.sub(r"(?m)^\s*(python\s+-m\s+pip|pip3?)\s+install\s+\.$", "uv sync", text)
    text = re.sub(r"(?m)^\s*(python\s+-m\s+pip|pip3?)\s+install\s+", "uv run pip install ", text)
    changes = 0 if text == before else 1
    return text, changes


def insert_quickstart(text: str, quickstart_block: str) -> Tuple[str, int]:
    if not quickstart_block:
        return text, 0
    lowered = text.lower()
    if "development quickstart" in lowered:
        return text, 0
    if text.endswith("\n"):
        return text + "\n" + quickstart_block + "\n", 1
    return text + "\n\n" + quickstart_block + "\n", 1


def apply_issue_fix(repo: Path, issue: Issue, signals: Dict[str, object]) -> Tuple[bool, str, Optional[str]]:
    target = Path(issue.doc_file)
    if not target.is_file():
        return False, "skipped", "target doc file does not exist"

    text = read_text(target)
    new_text = text
    changed = 0

    if issue.category == "js-package-manager-mismatch":
        canonical = str(signals["canonical_js_manager"])
        if canonical == "unknown":
            return False, "skipped", "canonical package manager unknown"
        new_text, changed = rewrite_js_commands(text, canonical)
    elif issue.category == "python-uv-mismatch":
        new_text, changed = rewrite_uv_commands(text)
    elif issue.category in {
        "missing-quickstart",
        "rust-missing-build",
        "rust-missing-test",
        "swift-missing-build",
        "swift-missing-test",
    }:
        quickstart = quickstart_for_signals(signals)
        if not quickstart:
            return False, "skipped", "quickstart could not be inferred"
        new_text, changed = insert_quickstart(text, quickstart)
    else:
        return False, "skipped", "issue category has no safe autofix rule"

    if changed == 0:
        return False, "skipped", "no bounded replacement applied"

    target.write_text(new_text, encoding="utf-8")
    return True, "applied", None


def summarize_repo(repo: Path, issues: List[Issue]) -> Dict[str, object]:
    return {
        "repo": str(repo),
        "issue_count": len(issues),
        "issues": [i.to_dict() for i in issues],
    }


def render_markdown(
    run_context: Dict[str, object],
    repos_scanned: List[str],
    unaligned_repos: List[Dict[str, object]],
    fixes_applied: List[Dict[str, object]],
    post_fix_status: Dict[str, int],
    errors: List[Dict[str, str]],
) -> str:
    lines: List[str] = []

    lines.append("## Run Context")
    lines.append(f"- Timestamp: {run_context['timestamp_utc']}")
    lines.append(f"- Workspace: {run_context['workspace']}")
    lines.append(f"- Exclusions: {', '.join(run_context['exclusions']) if run_context['exclusions'] else '(none)'}")
    lines.append(f"- Apply fixes: {run_context['apply_fixes']}")
    lines.append(f"- Repos scanned: {run_context['repos_scanned_count']}")
    lines.append("")

    lines.append("## Discovery Summary")
    lines.append(f"- Project roots discovered: {len(repos_scanned)}")
    lines.append(f"- Repos with issues: {len(unaligned_repos)}")
    lines.append("")

    lines.append("## Unaligned Repositories")
    if not unaligned_repos:
        lines.append("- None")
    else:
        for repo in unaligned_repos:
            lines.append(f"- {repo['repo']} ({repo['issue_count']} issues)")
    lines.append("")

    lines.append("## Fixes Applied")
    if not fixes_applied:
        lines.append("- None")
    else:
        for fix in fixes_applied:
            lines.append(
                f"- [{fix['status']}] {fix['repo']} -> {fix['file']} ({fix['rule']})"
                + (f" | {fix['reason']}" if fix.get("reason") else "")
            )
    lines.append("")

    lines.append("## Remaining Issues")
    lines.append(f"- Unresolved: {post_fix_status['unresolved_issues']}")
    lines.append(f"- Resolved by fixes: {post_fix_status['resolved_issues']}")
    lines.append("")

    lines.append("## Modified Files (no commit)")
    modified = sorted({fix["file"] for fix in fixes_applied if fix["status"] == "applied"})
    if not modified:
        lines.append("- None")
    else:
        for file_path in modified:
            lines.append(f"- {file_path}")
    lines.append("")

    lines.append("## Errors/Warnings")
    if not errors:
        lines.append("- None")
    else:
        for error in errors:
            lines.append(f"- {error['repo']}: {error['message']}")

    return "\n".join(lines).strip() + "\n"


def main() -> int:
    args = parse_args()
    workspace = Path(args.workspace).expanduser().resolve()
    if not workspace.exists() or not workspace.is_dir():
        print(f"Workspace path does not exist or is not a directory: {workspace}", file=sys.stderr)
        return 1

    excludes = read_excludes(args)
    errors: List[Dict[str, str]] = []

    repos = discover_repos(workspace, excludes, args.max_repos)

    repo_issues: Dict[Path, List[Issue]] = {}
    repo_signals: Dict[Path, Dict[str, object]] = {}

    for repo in repos:
        try:
            signals = detect_signals(repo)
            docs = collect_doc_files(repo)
            repo_signals[repo] = signals
            repo_issues[repo] = detect_issues(repo, signals, docs)
        except Exception as exc:  # defensive
            errors.append({"repo": str(repo), "message": f"scan error: {exc}"})
            repo_issues[repo] = []

    initial_unresolved = sum(len(issues) for issues in repo_issues.values())

    fixes_applied: List[Dict[str, str]] = []
    touched_repos: set[Path] = set()

    if args.apply_fixes:
        for repo, issues in repo_issues.items():
            for issue in issues:
                if not issue.auto_fixable:
                    fixes_applied.append(
                        {
                            "repo": str(repo),
                            "file": issue.doc_file,
                            "rule": issue.category,
                            "status": "skipped",
                            "reason": "issue marked non-autofixable",
                        }
                    )
                    continue
                try:
                    changed, status, reason = apply_issue_fix(repo, issue, repo_signals[repo])
                    fixes_applied.append(
                        {
                            "repo": str(repo),
                            "file": issue.doc_file,
                            "rule": issue.category,
                            "status": status,
                            "reason": reason or "",
                        }
                    )
                    if changed:
                        issue.fixed = True
                        touched_repos.add(repo)
                except Exception as exc:  # defensive
                    fixes_applied.append(
                        {
                            "repo": str(repo),
                            "file": issue.doc_file,
                            "rule": issue.category,
                            "status": "error",
                            "reason": str(exc),
                        }
                    )
                    errors.append({"repo": str(repo), "message": f"fix error: {exc}"})

        for repo in touched_repos:
            try:
                signals = detect_signals(repo)
                docs = collect_doc_files(repo)
                repo_signals[repo] = signals
                repo_issues[repo] = detect_issues(repo, signals, docs)
            except Exception as exc:
                errors.append({"repo": str(repo), "message": f"post-fix rescan error: {exc}"})

    unresolved = sum(len(issues) for issues in repo_issues.values())

    unaligned_repos = [
        summarize_repo(repo, issues)
        for repo, issues in sorted(repo_issues.items(), key=lambda item: str(item[0]))
        if issues
    ]

    run_context = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "workspace": str(workspace),
        "exclusions": [str(p) for p in excludes],
        "mode": "apply-fixes" if args.apply_fixes else "audit-only",
        "apply_fixes": args.apply_fixes,
        "repos_scanned_count": len(repos),
        "unaligned_repos_count": len(unaligned_repos),
    }

    post_fix_status = {
        "unresolved_issues": unresolved,
        "resolved_issues": max(0, initial_unresolved - unresolved),
    }

    report = {
        "run_context": run_context,
        "repos_scanned": [str(repo) for repo in repos],
        "unaligned_repos": unaligned_repos,
        "fixes_applied": fixes_applied,
        "post_fix_status": post_fix_status,
        "errors": errors,
    }

    markdown = render_markdown(
        run_context=run_context,
        repos_scanned=report["repos_scanned"],
        unaligned_repos=unaligned_repos,
        fixes_applied=fixes_applied,
        post_fix_status=post_fix_status,
        errors=errors,
    )

    if args.json_out:
        Path(args.json_out).expanduser().write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if args.md_out:
        Path(args.md_out).expanduser().write_text(markdown, encoding="utf-8")
    if args.print_json:
        print(json.dumps(report, indent=2))
    if args.print_md:
        print(markdown)

    if args.fail_on_issues and unresolved > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
