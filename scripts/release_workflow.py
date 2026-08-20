from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

import release_version


ROOT = Path(__file__).resolve().parent.parent
ACCOUNTING_STATUSES = {"preserved", "in-progress", "archived", "merged", "safe-to-delete"}


class ReleaseWorkflowError(RuntimeError):
    pass


@dataclass(frozen=True)
class PullRequestSnapshot:
    number: int
    url: str
    state: str
    head_ref: str
    head_sha: str
    review_decision: str
    comments: int
    checks: tuple[tuple[str, str], ...]

    @property
    def phase(self) -> str:
        buckets = {bucket for _, bucket in self.checks}
        if self.state == "MERGED":
            return "merged"
        if not self.checks:
            return "awaiting-github-state"
        if buckets & {"fail", "cancel"}:
            return "failed-checks"
        if "pending" in buckets:
            return "awaiting-pr-checks"
        if self.review_decision == "CHANGES_REQUESTED":
            return "changes-requested"
        if self.comments:
            return "comments-require-review"
        return "ready-to-advance"


def run(args: list[str], *, cwd: Path = ROOT, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        args, cwd=cwd, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    if check and result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise ReleaseWorkflowError(f"`{' '.join(args)}` failed in {cwd}: {detail}")
    return result


def git(args: list[str], *, cwd: Path = ROOT, check: bool = True) -> subprocess.CompletedProcess[str]:
    return run(["git", *args], cwd=cwd, check=check)


def gh(args: list[str], *, cwd: Path = ROOT, check: bool = True) -> subprocess.CompletedProcess[str]:
    return run(["gh", *args], cwd=cwd, check=check)


def normalized_version(value: str) -> str:
    try:
        return release_version.validate_semver(value.removeprefix("v"))
    except release_version.VersionToolError as error:
        raise ReleaseWorkflowError(str(error)) from error


def release_tag(version: str) -> str:
    return f"v{version}"


def current_branch(cwd: Path = ROOT) -> str:
    return git(["branch", "--show-current"], cwd=cwd).stdout.strip()


def ensure_clean(cwd: Path = ROOT) -> None:
    if git(["status", "--porcelain"], cwd=cwd).stdout.strip():
        raise ReleaseWorkflowError(f"Release workflow requires a clean worktree: {cwd}")


def ensure_feature_branch() -> str:
    branch = current_branch()
    if not branch or branch == "main":
        raise ReleaseWorkflowError(
            "Release prepare/inspect/advance must run from a named feature worktree, not main."
        )
    return branch


def release_notes_path(version: str, root: Path = ROOT) -> Path:
    path = root / "docs" / "releases" / f"v{version}.md"
    if not path.is_file():
        raise ReleaseWorkflowError(
            f"Release notes are required at {path.relative_to(root)} before release preparation."
        )
    return path


def find_main_worktree() -> Path:
    output = git(["worktree", "list", "--porcelain"]).stdout
    worktree: Path | None = None
    for line in output.splitlines():
        if line.startswith("worktree "):
            worktree = Path(line.removeprefix("worktree "))
        elif line == "branch refs/heads/main" and worktree is not None:
            return worktree
    raise ReleaseWorkflowError(
        "No worktree owns local main. Restore the clean Socket main checkout before advancing."
    )


def remote_main_sha() -> str:
    output = git(["ls-remote", "origin", "refs/heads/main"]).stdout.strip()
    if not output:
        raise ReleaseWorkflowError("origin/main is not readable.")
    return output.split()[0]


def parse_accounting(values: list[str]) -> dict[str, str]:
    accounting: dict[str, str] = {}
    for value in values:
        branch, separator, status = value.partition("=")
        if not separator or not branch or status not in ACCOUNTING_STATUSES:
            allowed = ", ".join(sorted(ACCOUNTING_STATUSES))
            raise ReleaseWorkflowError(
                f"Invalid branch accounting {value!r}; use BRANCH=STATUS where STATUS is one of: {allowed}."
            )
        accounting[branch] = status
    return accounting


def branch_accounting(main_root: Path, supplied: dict[str, str]) -> dict[str, str]:
    lines = git(
        ["branch", "--no-merged", "main", "--format=%(refname:short)"], cwd=main_root
    ).stdout.splitlines()
    branches = sorted(line.strip() for line in lines if line.strip() and line.strip() != "main")
    missing = [branch for branch in branches if branch not in supplied]
    unknown = sorted(set(supplied) - set(branches))
    if missing:
        examples = " ".join(
            f"--branch-accounting {branch}=in-progress" for branch in missing
        )
        raise ReleaseWorkflowError(
            "Branch accounting is incomplete for: "
            + ", ".join(missing)
            + f". Re-run with explicit classifications, for example: {examples}"
        )
    if unknown:
        raise ReleaseWorkflowError(
            "Branch accounting named branches that are already contained by main or absent locally: "
            + ", ".join(unknown)
        )
    return {branch: supplied[branch] for branch in branches}


def pr_number_for_branch(branch: str) -> int | None:
    result = gh(
        [
            "pr", "list", "--state", "all", "--head", branch, "--base", "main",
            "--limit", "1", "--json", "number",
        ]
    )
    values = json.loads(result.stdout)
    return int(values[0]["number"]) if values else None


def snapshot_pr(number: int) -> PullRequestSnapshot:
    data = json.loads(
        gh(
            [
                "pr", "view", str(number), "--json",
                "number,url,state,headRefName,headRefOid,reviewDecision,comments,reviews",
            ]
        ).stdout
    )
    checks_result = gh(["pr", "checks", str(number), "--json", "name,bucket"], check=False)
    checks: list[tuple[str, str]] = []
    if checks_result.stdout.strip():
        checks = [
            (str(item["name"]), str(item["bucket"]))
            for item in json.loads(checks_result.stdout)
        ]
    comments = len(data.get("comments") or []) + len(
        [review for review in data.get("reviews") or [] if review.get("state") == "COMMENTED"]
    )
    return PullRequestSnapshot(
        number=int(data["number"]),
        url=str(data["url"]),
        state=str(data["state"]),
        head_ref=str(data["headRefName"]),
        head_sha=str(data["headRefOid"]),
        review_decision=str(data.get("reviewDecision") or ""),
        comments=comments,
        checks=tuple(checks),
    )


def continuation_packet(snapshot: PullRequestSnapshot, version: str) -> str:
    return json.dumps(
        {
            "schema": "socket-release-continuation/v1",
            "operation": "socket-release",
            "repository": "gaelic-ghost/socket",
            "release_tag": release_tag(version),
            "branch": snapshot.head_ref,
            "head_commit": snapshot.head_sha,
            "pr_number": snapshot.number,
            "phase": snapshot.phase,
            "minimum_delay_minutes": 5,
            "resume_command": f"scripts/release.sh inspect {version}",
            "advance_command": f"scripts/release.sh advance {version}",
        },
        sort_keys=True,
    )


def print_snapshot(snapshot: PullRequestSnapshot, version: str) -> None:
    checks = ", ".join(f"{name}:{bucket}" for name, bucket in snapshot.checks) or "none"
    print(
        f"PR #{snapshot.number}: phase={snapshot.phase}; checks={checks}; "
        f"review={snapshot.review_decision or 'none'}; comments={snapshot.comments}; {snapshot.url}"
    )
    if snapshot.phase not in {"ready-to-advance", "merged"}:
        print(continuation_packet(snapshot, version))


def ensure_version_matches(version: str) -> list[release_version.VersionTarget]:
    targets = release_version.discover_targets(ROOT)
    try:
        release_version.ensure_versions_match_release(targets, version)
    except release_version.VersionToolError as error:
        raise ReleaseWorkflowError(str(error)) from error
    return targets


def ensure_next_stable_version(
    targets: list[release_version.VersionTarget], version: str
) -> None:
    allowed = {
        release_version.determine_target_version(targets, mode, None)
        for mode in ("patch", "minor", "major")
    }
    if version not in allowed:
        rendered = ", ".join(sorted(allowed))
        raise ReleaseWorkflowError(
            f"Requested version {version} is not the next patch, minor, or major release. "
            f"Choose one of: {rendered}."
        )


def create_or_update_pr(branch: str, version: str) -> int:
    title = f"release: prepare Socket {release_tag(version)}"
    body = (
        "## Summary\n\n"
        f"- prepares Socket {release_tag(version)} through the single protected-main release workflow\n"
        "- includes the canonical Swift workspace, native local-server, Soto, and GitHub-only deployment changes\n"
        "- consolidates Socket release automation and guidance\n\n"
        "## Verification\n\n"
        "- `uv run scripts/validate_socket.py --profile full`\n"
        f"- `scripts/release.sh prepare {version}`\n"
    )
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md") as body_file:
        body_file.write(body)
        body_file.flush()
        number = pr_number_for_branch(branch)
        if number is None:
            gh(
                [
                    "pr", "create", "--base", "main", "--head", branch,
                    "--title", title, "--body-file", body_file.name,
                    "--label", "needs-triage",
                ]
            )
            number = pr_number_for_branch(branch)
            if number is None:
                raise ReleaseWorkflowError("GitHub did not return the release PR after creation.")
        else:
            print(f"Keeping the existing release PR #{number} body and reviewer-added content.")
    return number


def run_full_validation(root: Path = ROOT) -> None:
    result = subprocess.run(
        ["uv", "run", "scripts/validate_socket.py", "--profile", "full"],
        cwd=root,
        check=False,
    )
    if result.returncode != 0:
        raise ReleaseWorkflowError("Full Socket validation failed.")


def prepare(version: str) -> int:
    branch = ensure_feature_branch()
    ensure_clean()
    release_notes_path(version)
    targets = release_version.discover_targets(ROOT)
    current_versions = release_version.read_versions(targets)
    if current_versions != [version]:
        ensure_next_stable_version(targets, version)
    try:
        changed, _ = release_version.apply_version(ROOT, targets, version)
    except release_version.VersionToolError as error:
        raise ReleaseWorkflowError(str(error)) from error
    if not changed:
        commit = git(
            [
                "log", "-1", "--format=%H", "--fixed-strings", "--grep",
                f"release: prepare Socket {release_tag(version)}",
            ]
        ).stdout.strip()
        if not commit:
            raise ReleaseWorkflowError(
                f"Version surfaces already equal {version}, but the branch has no matching release-preparation commit."
            )
    else:
        git(["add", *changed])
        git(["commit", "-m", f"release: prepare Socket {release_tag(version)}"])
    run_full_validation()
    ensure_clean()
    git(["push", "-u", "origin", branch])
    remote_output = git(["ls-remote", "origin", f"refs/heads/{branch}"]).stdout.split()
    remote_sha = remote_output[0] if remote_output else ""
    head_sha = git(["rev-parse", "HEAD"]).stdout.strip()
    if remote_sha != head_sha:
        raise ReleaseWorkflowError("The release branch is not visible at the expected commit on origin.")
    number = create_or_update_pr(branch, version)
    print_snapshot(snapshot_pr(number), version)
    return 0


def inspect(version: str) -> int:
    branch = ensure_feature_branch()
    ensure_clean()
    ensure_version_matches(version)
    number = pr_number_for_branch(branch)
    if number is None:
        raise ReleaseWorkflowError(
            f"No release PR exists for {branch}; run `scripts/release.sh prepare {version}` first."
        )
    print_snapshot(snapshot_pr(number), version)
    return 0


def append_release_evidence(
    notes: str,
    evidence: release_version.ReleaseEvidence,
    accounting: list[str],
) -> str:
    lines = "\n".join(f"- {line}" for line in accounting) or "- No child synchronization was required."
    return (
        notes.rstrip()
        + "\n\n## Release evidence\n\n"
        + release_version.render_evidence_summary(evidence)
        + "\n## Child synchronization accounting\n\n"
        + lines
        + "\n"
    )


def advance(version: str, accounting_values: list[str], review_comments_addressed: bool) -> int:
    branch = ensure_feature_branch()
    ensure_clean()
    ensure_version_matches(version)
    number = pr_number_for_branch(branch)
    if number is None:
        raise ReleaseWorkflowError(f"No release PR exists for {branch}.")
    snapshot = snapshot_pr(number)
    if snapshot.phase not in {"ready-to-advance", "merged"}:
        print_snapshot(snapshot, version)
        if snapshot.phase != "comments-require-review" or not review_comments_addressed:
            raise ReleaseWorkflowError(
                f"Release PR #{number} is not ready to advance: {snapshot.phase}."
            )
    current_head = git(["rev-parse", "HEAD"]).stdout.strip()
    if snapshot.head_ref != branch or snapshot.head_sha != current_head:
        raise ReleaseWorkflowError(
            "Release PR branch or commit identity changed; inspect and reconcile before advancing."
        )
    if snapshot.state != "MERGED":
        gh(["pr", "merge", str(number), "--auto", "--merge", "--delete-branch"])
        merged = snapshot_pr(number)
        if merged.state != "MERGED":
            print_snapshot(merged, version)
            return 0

    main_root = find_main_worktree()
    ensure_clean(main_root)
    git(["fetch", "origin", "main", "--prune"], cwd=main_root)
    git(["pull", "--ff-only", "origin", "main"], cwd=main_root)
    main_head = git(["rev-parse", "HEAD"], cwd=main_root).stdout.strip()
    if main_head != remote_main_sha():
        raise ReleaseWorkflowError(
            "Local main does not match the current origin/main after fast-forward."
        )
    targets = release_version.discover_targets(main_root)
    release_version.ensure_versions_match_release(targets, version)
    notes_path = release_notes_path(version, main_root)
    supplied = parse_accounting(accounting_values)
    accounted_branches = branch_accounting(main_root, supplied)
    changed_files = release_version.changed_files_since_previous_release(main_root)
    child_accounting = release_version.ensure_subtree_gates(
        main_root,
        changed_files,
        release_version.version_only_paths(targets),
    )

    run_full_validation(main_root)
    release_version.ensure_clean_checkout(main_root)
    release_version.ensure_main_matches_origin(main_root)
    evidence = release_version.capture_release_evidence(
        main_root, release_version.evidence_path(main_root)
    )
    tag = release_tag(version)
    local_tag = git(["tag", "-l", tag], cwd=main_root).stdout.strip()
    remote_tag_result = git(
        ["ls-remote", "origin", f"refs/tags/{tag}^{{}}"], cwd=main_root
    ).stdout.strip()
    if local_tag:
        local_tag_commit = git(["rev-list", "-n", "1", tag], cwd=main_root).stdout.strip()
        if local_tag_commit != main_head:
            raise ReleaseWorkflowError(f"Local tag {tag} does not point at reviewed main {main_head}.")
    if remote_tag_result and remote_tag_result.split()[0] != main_head:
        raise ReleaseWorkflowError(f"Remote tag {tag} does not point at reviewed main {main_head}.")
    if not local_tag and not remote_tag_result:
        git(["tag", "-a", tag, "-m", f"Socket {tag}"], cwd=main_root)
        local_tag = tag
    if local_tag and not remote_tag_result:
        git(["push", "origin", tag], cwd=main_root)
    remote_tag = git(
        ["ls-remote", "origin", f"refs/tags/{tag}^{{}}"], cwd=main_root
    ).stdout.strip()
    if not remote_tag or remote_tag.split()[0] != main_head:
        raise ReleaseWorkflowError(
            f"Annotated tag {tag} is not visible on origin at reviewed main."
        )

    if gh(["release", "view", tag], cwd=main_root, check=False).returncode != 0:
        notes = append_release_evidence(
            notes_path.read_text(encoding="utf-8"), evidence, child_accounting
        )
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md") as notes_file:
            notes_file.write(notes)
            notes_file.flush()
            gh(
                [
                    "release", "create", tag, "--verify-tag", "--title",
                    f"Socket {tag}", "--notes-file", notes_file.name,
                ],
                cwd=main_root,
            )
    release_data = json.loads(
        gh(
            ["release", "view", tag, "--json", "tagName,isPrerelease,url"],
            cwd=main_root,
        ).stdout
    )
    if release_data["tagName"] != tag or release_data["isPrerelease"]:
        raise ReleaseWorkflowError(
            f"GitHub release metadata for {tag} does not match the stable major release."
        )
    print("Branch accounting:")
    if accounted_branches:
        for accounted_branch, status in accounted_branches.items():
            print(f"- {accounted_branch}: {status}")
    else:
        print("- No local branches remain outside main.")
    release_version.refresh_socket_marketplace_cache(main_root)
    print(f"Socket {tag} released from {main_head}: {release_data['url']}")
    return 0


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run Socket's single protected-main release workflow."
    )
    subparsers = parser.add_subparsers(dest="operation", required=True)
    subparsers.add_parser("inventory", help="List maintained Socket version surfaces.")
    for operation in ("prepare", "inspect"):
        child = subparsers.add_parser(operation)
        child.add_argument("version")
    advance_parser = subparsers.add_parser("advance")
    advance_parser.add_argument("version")
    advance_parser.add_argument("--branch-accounting", action="append", default=[])
    advance_parser.add_argument("--review-comments-addressed", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    if args.operation == "inventory":
        return release_version.render_inventory(release_version.discover_targets(ROOT))
    version = normalized_version(args.version)
    if args.operation == "prepare":
        return prepare(version)
    if args.operation == "inspect":
        return inspect(version)
    return advance(version, args.branch_accounting, args.review_comments_addressed)


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv[1:]))
    except (ReleaseWorkflowError, release_version.VersionToolError) as error:
        print(f"socket-release: {error}", file=sys.stderr)
        raise SystemExit(1)
