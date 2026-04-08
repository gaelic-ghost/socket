from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


EXACT_NO_FINDINGS = "No findings."


@dataclass
class ScriptResult:
    name: str
    report: dict[str, Any] | None
    error: str | None = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit and coordinate bounded maintenance for a plugin-development repository"
    )
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--plugin-name")
    parser.add_argument("--workflow", choices=("audit-only", "apply-safe-fixes"), default="audit-only")
    parser.add_argument("--doc-scope", choices=("readme", "roadmap", "all"), default="all")
    parser.add_argument("--source-plugin-root")
    parser.add_argument("--install-scope", choices=("personal", "repo"), default="repo")
    parser.add_argument("--target-repo-root")
    parser.add_argument("--install-mode", choices=("copy", "symlink"), default="copy")
    parser.add_argument("--apply-install-repairs", action="store_true")
    parser.add_argument("--print-md", action="store_true")
    parser.add_argument("--print-json", action="store_true")
    parser.add_argument("--fail-on-issues", action="store_true")
    return parser.parse_args()


def _skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _skills_root() -> Path:
    return _skill_root().parent


def _repo_root(path: str) -> Path:
    return Path(path).expanduser().resolve()


def _run_json_script(name: str, script_path: Path, args: list[str]) -> ScriptResult:
    command = [sys.executable, str(script_path), *args]
    try:
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError as exc:
        return ScriptResult(name=name, report=None, error=f"{name} could not be started: {exc}")

    stdout = completed.stdout.strip()
    stderr = completed.stderr.strip()
    if not stdout:
        detail = stderr or f"{name} returned no output."
        return ScriptResult(name=name, report=None, error=detail)
    try:
        report = json.loads(stdout)
    except json.JSONDecodeError:
        detail = stderr or f"{name} did not return valid JSON."
        return ScriptResult(name=name, report=None, error=detail)

    if completed.returncode != 0 and not stderr:
        return ScriptResult(name=name, report=report, error=f"{name} exited with status {completed.returncode}.")
    if completed.returncode != 0 and stderr:
        return ScriptResult(name=name, report=report, error=f"{name} exited with status {completed.returncode}: {stderr}")
    return ScriptResult(name=name, report=report)


def run_validator(repo_root: Path, plugin_name: str | None) -> ScriptResult:
    script = _skills_root() / "validate-plugin-install-surfaces" / "scripts" / "validate_plugin_install_surfaces.py"
    args = ["--repo-root", str(repo_root), "--print-json"]
    if plugin_name:
        args.extend(["--plugin-name", plugin_name])
    return _run_json_script("validate-plugin-install-surfaces", script, args)


def run_docs(repo_root: Path, doc_scope: str, apply_fixes: bool) -> ScriptResult:
    script = _skills_root() / "maintain-plugin-docs" / "scripts" / "maintain_plugin_docs.py"
    args = [
        "--workspace",
        str(repo_root.parent),
        "--repo-glob",
        repo_root.name,
        "--doc-scope",
        doc_scope,
        "--print-json",
    ]
    if apply_fixes:
        args.append("--apply-fixes")
    return _run_json_script("maintain-plugin-docs", script, args)


def run_install(source_plugin_root: Path, install_scope: str, target_repo_root: Path, install_mode: str, apply_repairs: bool) -> ScriptResult:
    script = _skills_root() / "install-plugin-to-socket" / "scripts" / "install_plugin_to_socket.py"
    args = [
        "--source-plugin-root",
        str(source_plugin_root),
        "--scope",
        install_scope,
        "--repo-root",
        str(target_repo_root),
        "--install-mode",
        install_mode,
        "--action",
        "repair" if apply_repairs else "verify",
        "--run-mode",
        "apply" if apply_repairs else "check-only",
    ]
    return _run_json_script("install-plugin-to-socket", script, args)


def _count_validator_findings(report: dict[str, Any] | None) -> int:
    if not report:
        return 0
    return sum(len(report.get(key, [])) for key in ("metadata_findings", "install_surface_findings", "mirror_findings"))


def _count_docs_findings(report: dict[str, Any] | None) -> int:
    if not report:
        return 0
    return sum(len(report.get(key, [])) for key in ("readme_findings", "roadmap_findings", "cross_doc_findings"))


def _count_install_findings(report: dict[str, Any] | None) -> int:
    if not report:
        return 0
    return len(report.get("findings", []))


def _build_owner_assignments(
    validator_report: dict[str, Any] | None,
    docs_report: dict[str, Any] | None,
    install_report: dict[str, Any] | None,
    install_attempted: bool,
    install_requested: bool,
    source_plugin_root: Path | None,
) -> dict[str, Any]:
    assignments: dict[str, Any] = {
        "validate-plugin-install-surfaces": {
            "role": "audit-only packaging and install-surface validation",
            "finding_count": _count_validator_findings(validator_report),
        },
        "maintain-plugin-docs": {
            "role": "README and ROADMAP maintenance",
            "finding_count": _count_docs_findings(docs_report),
        },
        "install-plugin-to-socket": {
            "role": "bounded local Codex install lifecycle repair",
            "finding_count": _count_install_findings(install_report),
            "attempted": install_attempted,
        },
    }
    if install_requested and source_plugin_root is None:
        assignments["install-plugin-to-socket"]["deferred_reason"] = (
            "Install repair was requested, but `--source-plugin-root` was not provided."
        )
    return assignments


def _build_deferred_findings(
    workflow: str,
    apply_install_repairs: bool,
    source_plugin_root: Path | None,
    install_result: ScriptResult | None,
) -> list[dict[str, str]]:
    deferred: list[dict[str, str]] = []
    if workflow == "apply-safe-fixes" and apply_install_repairs and source_plugin_root is None:
        deferred.append(
            {
                "owner": "install-plugin-to-socket",
                "reason": "Install repair was requested without `--source-plugin-root`, so local install repair was skipped.",
            }
        )
    if install_result is not None and install_result.error is not None:
        deferred.append(
            {
                "owner": install_result.name,
                "reason": install_result.error,
            }
        )
    return deferred


def build_report(
    repo_root: Path,
    workflow: str,
    doc_scope: str,
    plugin_name: str | None,
    source_plugin_root: Path | None,
    target_repo_root: Path,
    install_scope: str,
    install_mode: str,
    apply_install_repairs: bool,
    initial_validator_result: ScriptResult,
    validator_result: ScriptResult,
    docs_result: ScriptResult,
    install_result: ScriptResult | None,
) -> dict[str, Any]:
    initial_validator_report = initial_validator_result.report or {}
    validator_report = validator_result.report or {}
    docs_report = docs_result.report or {}
    install_report = install_result.report if install_result is not None and install_result.report is not None else {}

    fixes_applied: list[dict[str, Any]] = []
    if docs_report.get("fixes_applied"):
        fixes_applied.extend(docs_report["fixes_applied"])
    if install_report.get("apply_actions"):
        fixes_applied.extend(
            {
                "repo": target_repo_root.name,
                "file": action.get("path", ""),
                "rule": action.get("action", "install-action"),
                "status": "applied",
            }
            for action in install_report["apply_actions"]
        )

    errors: list[str] = []
    for result in (validator_result, docs_result, install_result):
        if result is not None and result.error is not None:
            errors.append(result.error)

    initial_issues = _count_validator_findings(initial_validator_report) + _count_docs_findings(docs_report)
    if install_result is not None and workflow == "audit-only":
        initial_issues += _count_install_findings(install_report)
    if install_result is not None and workflow == "apply-safe-fixes":
        initial_issues += _count_install_findings(install_report)

    deferred_findings = _build_deferred_findings(
        workflow=workflow,
        apply_install_repairs=apply_install_repairs,
        source_plugin_root=source_plugin_root,
        install_result=install_result,
    )

    unresolved_issues = _count_validator_findings(validator_report) + _count_docs_findings(docs_report)
    if install_result is not None:
        unresolved_issues += _count_install_findings(install_report)
    unresolved_issues += len(deferred_findings)

    return {
        "run_context": {
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "repo_root": str(repo_root),
            "doc_scope": doc_scope,
            "workflow": workflow,
            "apply_install_repairs": apply_install_repairs,
        },
        "repo_root": str(repo_root),
        "workflow": workflow,
        "owner_assignments": _build_owner_assignments(
            validator_report=validator_result.report,
            docs_report=docs_result.report,
            install_report=install_result.report if install_result is not None else None,
            install_attempted=install_result is not None,
            install_requested=apply_install_repairs,
            source_plugin_root=source_plugin_root,
        ),
        "validation_findings": {
            "metadata": validator_report.get("metadata_findings", []),
            "install_surface": validator_report.get("install_surface_findings", []),
            "mirror": validator_report.get("mirror_findings", []),
        },
        "docs_findings": {
            "readme": docs_report.get("readme_findings", []),
            "roadmap": docs_report.get("roadmap_findings", []),
            "cross_doc": docs_report.get("cross_doc_findings", []),
        },
        "install_findings": install_report.get("findings", []),
        "fixes_applied": fixes_applied,
        "deferred_findings": deferred_findings,
        "post_fix_status": {
            "initial_issues": initial_issues,
            "unresolved_issues": unresolved_issues,
            "resolved_issues": max(0, initial_issues - unresolved_issues),
        },
        "errors": errors,
        "plugin_name": plugin_name,
        "source_plugin_root": str(source_plugin_root) if source_plugin_root is not None else None,
        "target_repo_root": str(target_repo_root),
        "install_scope": install_scope,
        "install_mode": install_mode,
    }


def summarize_markdown(report: dict[str, Any]) -> str:
    lines = [
        "## Run Context",
        f"- Repo root: {report['repo_root']}",
        f"- Workflow: {report['workflow']}",
        f"- Doc scope: {report['run_context']['doc_scope']}",
        f"- Apply install repairs: {report['run_context']['apply_install_repairs']}",
        "",
        "## Owner Assignments",
    ]
    for owner, payload in report["owner_assignments"].items():
        lines.append(f"- {owner}: {payload['role']} ({payload['finding_count']} findings)")
        if payload.get("deferred_reason"):
            lines.append(f"  Deferred: {payload['deferred_reason']}")

    sections = (
        ("Validation Findings", report["validation_findings"]["metadata"] + report["validation_findings"]["install_surface"] + report["validation_findings"]["mirror"]),
        ("Docs Findings", report["docs_findings"]["readme"] + report["docs_findings"]["roadmap"] + report["docs_findings"]["cross_doc"]),
        ("Install Findings", report["install_findings"]),
        ("Deferred Findings", report["deferred_findings"]),
    )
    for title, items in sections:
        lines.extend(["", f"## {title}"])
        if not items:
            lines.append("- None")
            continue
        for item in items:
            message = item.get("message") or item.get("reason") or str(item)
            path = item.get("path") or item.get("owner") or "<unknown>"
            lines.append(f"- {path}: {message}")

    lines.extend(["", "## Fixes Applied"])
    if not report["fixes_applied"]:
        lines.append("- None")
    else:
        for item in report["fixes_applied"]:
            lines.append(f"- [{item['status']}] {item['repo']} -> {item['file']} ({item['rule']})")

    lines.extend(
        [
            "",
            "## Post-Fix Status",
            f"- Initial issues: {report['post_fix_status']['initial_issues']}",
            f"- Unresolved issues: {report['post_fix_status']['unresolved_issues']}",
            f"- Resolved issues: {report['post_fix_status']['resolved_issues']}",
            "",
            "## Errors",
        ]
    )
    if not report["errors"]:
        lines.append("- None")
    else:
        for item in report["errors"]:
            lines.append(f"- {item}")

    return "\n".join(lines).strip() + "\n"


def main() -> int:
    args = parse_args()
    repo_root = _repo_root(args.repo_root)
    if not repo_root.exists() or not repo_root.is_dir():
        print("Repository root does not exist or is not a directory.", file=sys.stderr)
        return 1

    source_plugin_root = _repo_root(args.source_plugin_root) if args.source_plugin_root else None
    target_repo_root = _repo_root(args.target_repo_root) if args.target_repo_root else repo_root

    validator_result = run_validator(repo_root, args.plugin_name)
    initial_validator_result = validator_result
    docs_result = run_docs(repo_root, args.doc_scope, apply_fixes=args.workflow == "apply-safe-fixes")

    install_result: ScriptResult | None = None
    if source_plugin_root is not None:
        install_result = run_install(
            source_plugin_root=source_plugin_root,
            install_scope=args.install_scope,
            target_repo_root=target_repo_root,
            install_mode=args.install_mode,
            apply_repairs=args.workflow == "apply-safe-fixes" and args.apply_install_repairs,
        )

    if args.workflow == "apply-safe-fixes":
        validator_result = run_validator(repo_root, args.plugin_name)

    report = build_report(
        repo_root=repo_root,
        workflow=args.workflow,
        doc_scope=args.doc_scope,
        plugin_name=args.plugin_name,
        source_plugin_root=source_plugin_root,
        target_repo_root=target_repo_root,
        install_scope=args.install_scope,
        install_mode=args.install_mode,
        apply_install_repairs=args.apply_install_repairs,
        initial_validator_result=initial_validator_result,
        validator_result=validator_result,
        docs_result=docs_result,
        install_result=install_result,
    )

    has_findings = any(
        (
            report["validation_findings"]["metadata"],
            report["validation_findings"]["install_surface"],
            report["validation_findings"]["mirror"],
            report["docs_findings"]["readme"],
            report["docs_findings"]["roadmap"],
            report["docs_findings"]["cross_doc"],
            report["install_findings"],
            report["deferred_findings"],
            report["fixes_applied"],
            report["errors"],
        )
    )
    markdown = summarize_markdown(report)
    json_report = json.dumps(report, indent=2, sort_keys=True)

    if args.print_md:
        if not has_findings:
            print(EXACT_NO_FINDINGS)
        else:
            print(markdown, end="")
    if args.print_json:
        print(json_report)
    if not args.print_md and not args.print_json:
        print(json_report)

    if args.fail_on_issues and has_findings:
        return 1
    return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
