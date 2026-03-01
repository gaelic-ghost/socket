#!/usr/bin/env python3
"""Read-only cleanup audit for repositories under a workspace root."""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from copy import deepcopy
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

try:
    import yaml
except ImportError:  # pragma: no cover - runtime dependency check
    yaml = None

DEFAULT_DIR_RULES: Dict[str, Tuple[str, int]] = {
    "dist": ("build_output", 10),
    "build": ("build_output", 10),
    ".next": ("build_output", 10),
    ".nuxt": ("build_output", 10),
    ".turbo": ("build_output", 8),
    "target": ("build_output", 10),
    "out": ("build_output", 8),
    "node_modules": ("dependency_artifact", 16),
    ".venv": ("dependency_artifact", 14),
    "venv": ("dependency_artifact", 14),
    ".gradle": ("dependency_artifact", 16),
    ".m2": ("dependency_artifact", 12),
    ".cache": ("tool_cache", 8),
    ".parcel-cache": ("tool_cache", 8),
    ".ruff_cache": ("tool_cache", 6),
    ".mypy_cache": ("tool_cache", 6),
    ".pytest_cache": ("tool_cache", 6),
    "__pycache__": ("tool_cache", 5),
}

DEFAULT_FILE_EXT_RULES: Dict[str, Tuple[str, int]] = {
    ".log": ("transient_file", 12),
    ".tmp": ("transient_file", 10),
    ".temp": ("transient_file", 10),
    ".cache": ("transient_file", 10),
    ".zip": ("archive", 10),
    ".tar": ("archive", 10),
    ".tgz": ("archive", 10),
    ".gz": ("archive", 8),
    ".bz2": ("archive", 8),
    ".xz": ("archive", 8),
}

DEFAULT_SETTINGS: Dict[str, Any] = {
    "workspaceRoot": "~/Workspace",
    "minMb": 50.0,
    "staleDays": 90,
    "maxFindings": 200,
    "severityCutoffs": {
        "medium": 45,
        "high": 70,
        "critical": 85,
    },
    "dirRuleOverrides": {},
    "fileExtRuleOverrides": {},
}

GIB = 1024**3
MIB = 1024**2


@dataclass
class Finding:
    severity: str
    score: int
    repo: str
    directory: str
    category: str
    size_bytes: int
    size_human: str
    why_flagged: str
    suggested_cleanup: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scan repositories in a workspace for cleanup chores (read-only)."
    )
    parser.add_argument(
        "--workspace",
        default=None,
        help="Workspace root containing repositories (CLI overrides config)",
    )
    parser.add_argument(
        "--min-mb",
        type=float,
        default=None,
        help="Ignore findings smaller than this size in MiB (CLI overrides config)",
    )
    parser.add_argument(
        "--stale-days",
        type=int,
        default=None,
        help="Boost score when artifacts are older than this many days (CLI overrides config)",
    )
    parser.add_argument(
        "--max-findings",
        type=int,
        default=None,
        help="Maximum findings to include in output (CLI overrides config)",
    )
    parser.add_argument(
        "--config",
        default="",
        help=(
            "Optional path to customization.yaml. Default resolution uses "
            "config/customization.yaml then config/customization.template.yaml"
        ),
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print JSON output instead of text report",
    )
    return parser.parse_args()


def require_yaml() -> None:
    if yaml is None:
        raise RuntimeError(
            "Missing dependency: PyYAML. Run with `uv run --with pyyaml python "
            "scripts/scan_workspace_cleanup.py ...`"
        )


def load_yaml_dict(path: Path) -> Dict[str, Any]:
    require_yaml()
    with path.open("r", encoding="utf-8") as handle:
        payload = yaml.safe_load(handle) or {}
    if not isinstance(payload, dict):
        raise ValueError(f"Expected a YAML mapping in {path}")
    return payload


def deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    merged: Dict[str, Any] = deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def resolve_config(args_config: str) -> tuple[Dict[str, Any], Path, str]:
    script_path = Path(__file__).resolve()
    skill_root = script_path.parent.parent
    template_path = skill_root / "config" / "customization.template.yaml"
    active_path = (
        Path(args_config).expanduser().resolve()
        if args_config
        else (skill_root / "config" / "customization.yaml")
    )

    settings = deepcopy(DEFAULT_SETTINGS)

    if template_path.exists():
        template_payload = load_yaml_dict(template_path)
        template_settings = template_payload.get("settings")
        if isinstance(template_settings, dict):
            settings = deep_merge(settings, template_settings)

    source = "hardcoded-defaults"
    if template_path.exists():
        source = str(template_path)

    if active_path.exists():
        active_payload = load_yaml_dict(active_path)
        active_settings = active_payload.get("settings")
        if isinstance(active_settings, dict):
            settings = deep_merge(settings, active_settings)
        source = str(active_path)

    return settings, active_path, source


def normalize_rule_overrides(
    defaults: Dict[str, Tuple[str, int]],
    overrides: Any,
    extension_keys: bool = False,
) -> Dict[str, Tuple[str, int]]:
    rules = dict(defaults)
    if not isinstance(overrides, dict):
        return rules

    for raw_key, raw_value in overrides.items():
        if not isinstance(raw_key, str) or not isinstance(raw_value, dict):
            continue
        category = raw_value.get("category")
        weight = raw_value.get("weight")
        if not isinstance(category, str) or not isinstance(weight, (int, float)):
            continue
        key = raw_key.lower().strip()
        if extension_keys and key and not key.startswith("."):
            key = f".{key}"
        if not key:
            continue
        rules[key] = (category, int(weight))

    return rules


def normalize_cutoffs(raw: Any) -> Dict[str, int]:
    cutoffs = dict(DEFAULT_SETTINGS["severityCutoffs"])
    if isinstance(raw, dict):
        for key in ("medium", "high", "critical"):
            value = raw.get(key)
            if isinstance(value, (int, float)):
                cutoffs[key] = int(value)

    if not (cutoffs["medium"] < cutoffs["high"] < cutoffs["critical"]):
        return dict(DEFAULT_SETTINGS["severityCutoffs"])

    return cutoffs


def human_bytes(num_bytes: int) -> str:
    units = ["B", "KiB", "MiB", "GiB", "TiB"]
    value = float(num_bytes)
    unit = units[0]
    for unit in units:
        if value < 1024.0 or unit == units[-1]:
            break
        value /= 1024.0
    if unit == "B":
        return f"{int(value)} {unit}"
    return f"{value:.1f} {unit}"


def find_repositories(workspace_root: Path) -> List[Path]:
    repos: List[Path] = []
    for root, dirs, _ in os.walk(workspace_root, topdown=True):
        root_path = Path(root)
        if ".git" in dirs or (root_path / ".git").is_file():
            repos.append(root_path)
            dirs[:] = []
            continue
        dirs[:] = [d for d in dirs if d not in {".git", ".svn", ".hg"}]
    return sorted(set(repos))


def dir_size_and_latest_mtime(path: Path) -> Tuple[int, float]:
    total = 0
    latest = path.stat().st_mtime if path.exists() else 0.0
    for root, dirs, files in os.walk(path, topdown=True, followlinks=False):
        dirs[:] = [d for d in dirs if d not in {".git"}]
        for filename in files:
            file_path = Path(root) / filename
            try:
                stat_result = file_path.stat()
            except OSError:
                continue
            total += stat_result.st_size
            if stat_result.st_mtime > latest:
                latest = stat_result.st_mtime
    return total, latest


def file_rule_for(path: Path, file_ext_rules: Dict[str, Tuple[str, int]]) -> Tuple[str, int] | None:
    suffix = path.suffix.lower()
    if suffix in file_ext_rules:
        return file_ext_rules[suffix]
    return None


def base_size_score(size_bytes: int) -> int:
    if size_bytes >= 5 * GIB:
        return 84
    if size_bytes >= 2 * GIB:
        return 72
    if size_bytes >= 1 * GIB:
        return 60
    if size_bytes >= 200 * MIB:
        return 42
    return 26


def severity_from_score(score: int, cutoffs: Dict[str, int]) -> str:
    if score >= cutoffs["critical"]:
        return "critical"
    if score >= cutoffs["high"]:
        return "high"
    if score >= cutoffs["medium"]:
        return "medium"
    return "low"


def sorted_findings(findings: Iterable[Finding]) -> List[Finding]:
    severity_rank = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    return sorted(
        findings,
        key=lambda f: (severity_rank[f.severity], -f.score, -f.size_bytes, f.repo, f.directory),
    )


def scan_repo(
    repo: Path,
    min_bytes: int,
    stale_days: int,
    now_ts: float,
    dir_rules: Dict[str, Tuple[str, int]],
    file_ext_rules: Dict[str, Tuple[str, int]],
    severity_cutoffs: Dict[str, int],
) -> List[Finding]:
    findings: List[Finding] = []

    for root, dirs, files in os.walk(repo, topdown=True, followlinks=False):
        root_path = Path(root)

        for dirname in list(dirs):
            rule = dir_rules.get(dirname)
            if not rule:
                continue

            candidate = root_path / dirname
            size_bytes, latest_mtime = dir_size_and_latest_mtime(candidate)
            dirs.remove(dirname)
            if size_bytes < min_bytes:
                continue

            category, weight = rule
            score = base_size_score(size_bytes) + weight + age_bonus_with_now(latest_mtime, stale_days, now_ts)
            score = min(100, score)
            severity = severity_from_score(score, severity_cutoffs)
            findings.append(
                Finding(
                    severity=severity,
                    score=score,
                    repo=str(repo),
                    directory=str(candidate),
                    category=category,
                    size_bytes=size_bytes,
                    size_human=human_bytes(size_bytes),
                    why_flagged=(
                        f"Matched directory pattern '{dirname}' with {human_bytes(size_bytes)} of removable artifacts."
                    ),
                    suggested_cleanup=(
                        "Review and remove/rebuild this artifact directory if not needed for active work."
                    ),
                )
            )

        for filename in files:
            candidate_file = root_path / filename
            rule = file_rule_for(candidate_file, file_ext_rules)
            if not rule:
                continue
            try:
                stat_result = candidate_file.stat()
            except OSError:
                continue
            if stat_result.st_size < min_bytes:
                continue

            category, weight = rule
            score = base_size_score(stat_result.st_size) + weight + age_bonus_with_now(
                stat_result.st_mtime, stale_days, now_ts
            )
            score = min(100, score)
            severity = severity_from_score(score, severity_cutoffs)

            findings.append(
                Finding(
                    severity=severity,
                    score=score,
                    repo=str(repo),
                    directory=str(candidate_file),
                    category=category,
                    size_bytes=stat_result.st_size,
                    size_human=human_bytes(stat_result.st_size),
                    why_flagged=(
                        f"Large transient or archive file '{candidate_file.name}' at {human_bytes(stat_result.st_size)}."
                    ),
                    suggested_cleanup=(
                        "Remove or relocate if this file is not needed for current development tasks."
                    ),
                )
            )

    return findings


def age_bonus_with_now(latest_mtime: float, stale_days: int, now_ts: float) -> int:
    if latest_mtime <= 0:
        return 0
    age_seconds = max(0.0, now_ts - latest_mtime)
    age_days = age_seconds / 86400.0
    if age_days >= stale_days * 2:
        return 10
    if age_days >= stale_days:
        return 6
    if age_days >= stale_days / 2:
        return 3
    return 0


def summarize_by_repo(findings: List[Finding]) -> List[dict]:
    summary: Dict[str, dict] = {}
    for finding in findings:
        row = summary.setdefault(
            finding.repo,
            {
                "repo": finding.repo,
                "total_size_bytes": 0,
                "total_size_human": "0 B",
                "critical": 0,
                "high": 0,
                "medium": 0,
                "low": 0,
                "findings": 0,
            },
        )
        row["total_size_bytes"] += finding.size_bytes
        row[finding.severity] += 1
        row["findings"] += 1

    rows = list(summary.values())
    for row in rows:
        row["total_size_human"] = human_bytes(row["total_size_bytes"])

    rows.sort(key=lambda item: (-item["total_size_bytes"], -item["critical"], -item["high"], item["repo"]))
    return rows


def text_report(findings: List[Finding], repo_summary: List[dict], scanned_repo_count: int, workspace: Path) -> str:
    lines: List[str] = []
    lines.append("Workspace Cleanup Audit (read-only)")
    lines.append(f"Workspace: {workspace}")
    lines.append(f"Repositories scanned: {scanned_repo_count}")
    lines.append(f"Findings: {len(findings)}")
    lines.append("")

    if findings:
        lines.append("Ranked Findings")
        for idx, finding in enumerate(findings, start=1):
            lines.append(
                f"{idx}. [{finding.severity.upper()}] score={finding.score} size={finding.size_human} "
                f"category={finding.category}"
            )
            lines.append(f"   repo: {finding.repo}")
            lines.append(f"   directory: {finding.directory}")
            lines.append(f"   reason: {finding.why_flagged}")
            lines.append(f"   cleanup: {finding.suggested_cleanup}")
        lines.append("")
    else:
        lines.append("No findings above threshold.")
        lines.append("")

    lines.append("Repo Summary")
    if repo_summary:
        for row in repo_summary:
            lines.append(
                f"- {row['repo']}: {row['total_size_human']} across {row['findings']} findings "
                f"(critical={row['critical']}, high={row['high']}, medium={row['medium']}, low={row['low']})"
            )
    else:
        lines.append("- No flagged repositories.")
    return "\n".join(lines)


def main() -> int:
    args = parse_args()

    try:
        settings, active_config_path, config_source = resolve_config(args.config)
    except Exception as exc:
        print(f"Failed to resolve configuration: {exc}", file=sys.stderr)
        return 2

    workspace_raw = args.workspace if args.workspace is not None else settings.get("workspaceRoot", "~/Workspace")
    min_mb_raw = args.min_mb if args.min_mb is not None else settings.get("minMb", 50.0)
    stale_days_raw = args.stale_days if args.stale_days is not None else settings.get("staleDays", 90)
    max_findings_raw = args.max_findings if args.max_findings is not None else settings.get("maxFindings", 200)

    try:
        min_mb = float(min_mb_raw)
        stale_days = int(stale_days_raw)
        max_findings = int(max_findings_raw)
    except (TypeError, ValueError) as exc:
        print(f"Invalid numeric config value: {exc}", file=sys.stderr)
        return 2

    workspace = Path(str(workspace_raw)).expanduser().resolve()
    if not workspace.exists() or not workspace.is_dir():
        print(f"Workspace path does not exist or is not a directory: {workspace}", file=sys.stderr)
        return 2

    min_bytes = int(min_mb * MIB)
    now_ts = time.time()

    dir_rules = normalize_rule_overrides(DEFAULT_DIR_RULES, settings.get("dirRuleOverrides"))
    file_ext_rules = normalize_rule_overrides(
        DEFAULT_FILE_EXT_RULES,
        settings.get("fileExtRuleOverrides"),
        extension_keys=True,
    )
    severity_cutoffs = normalize_cutoffs(settings.get("severityCutoffs"))

    repos = find_repositories(workspace)
    all_findings: List[Finding] = []
    for repo in repos:
        all_findings.extend(
            scan_repo(
                repo,
                min_bytes=min_bytes,
                stale_days=stale_days,
                now_ts=now_ts,
                dir_rules=dir_rules,
                file_ext_rules=file_ext_rules,
                severity_cutoffs=severity_cutoffs,
            )
        )

    ranked = sorted_findings(all_findings)[:max_findings]
    repo_summary = summarize_by_repo(ranked)

    payload = {
        "workspace": str(workspace),
        "scanned_repo_count": len(repos),
        "config_source": config_source,
        "active_config_path": str(active_config_path),
        "findings": [asdict(item) for item in ranked],
        "repo_summary": repo_summary,
    }

    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print(text_report(ranked, repo_summary, len(repos), workspace))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
