#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# ///
"""Prepare and open the single documented Swift Package Index add-package flow."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path


PACKAGE_LIST_ADD_FORM_URL = (
    "https://raw.githubusercontent.com/SwiftPackageIndex/PackageList/"
    "main/.github/ISSUE_TEMPLATE/add_package.yml"
)
PACKAGE_LIST_ISSUE_FORM_URL = "https://github.com/SwiftPackageIndex/PackageList/issues/new"
SPI_PACKAGE_BASE_URL = "https://swiftpackageindex.com"
ZEN_BROWSER_BUNDLE_ID = "app.zen-browser.zen"
ZEN_BROWSER_APP_NAME = "Zen"
SEMVER_TAG_RE = re.compile(r"^v?\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$")


class SPIAddPackageError(RuntimeError):
    """Raised when the package cannot safely proceed to the SPI issue form."""


@dataclass(frozen=True)
class PackageIdentity:
    owner: str
    repository: str
    git_url: str

    @property
    def spi_url(self) -> str:
        return f"{SPI_PACKAGE_BASE_URL}/{self.owner}/{self.repository}"


@dataclass(frozen=True)
class ReadinessResult:
    package_root: Path
    identity: PackageIdentity
    semver_tags: tuple[str, ...]
    indexed_state: str
    checked_steps: tuple[str, ...]
    skipped_steps: tuple[str, ...]


def run_command(
    args: list[str],
    *,
    cwd: Path,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        args,
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )
    if check and result.returncode != 0:
        stderr = result.stderr.strip()
        stdout = result.stdout.strip()
        details = stderr or stdout or f"exit status {result.returncode}"
        raise SPIAddPackageError(
            f"Command failed while preparing SPI submission: {' '.join(args)}\n{details}"
        )
    return result


def normalize_github_url(remote_url: str) -> PackageIdentity:
    candidate = remote_url.strip()
    if candidate.startswith("git@github.com:"):
        candidate = "https://github.com/" + candidate.removeprefix("git@github.com:")
    if candidate.startswith("ssh://git@github.com/"):
        candidate = "https://github.com/" + candidate.removeprefix("ssh://git@github.com/")
    if candidate.startswith("http://github.com/"):
        candidate = "https://github.com/" + candidate.removeprefix("http://github.com/")
    if candidate.startswith("https://www.github.com/"):
        candidate = "https://github.com/" + candidate.removeprefix("https://www.github.com/")

    parsed = urllib.parse.urlparse(candidate)
    if parsed.scheme != "https" or parsed.netloc != "github.com":
        raise SPIAddPackageError(
            "SPI package URLs must use a public GitHub HTTPS repository URL. "
            f"Found remote URL: {remote_url}"
        )

    path_parts = [part for part in parsed.path.strip("/").split("/") if part]
    if len(path_parts) != 2:
        raise SPIAddPackageError(
            "Expected a GitHub repository URL shaped as "
            f"`https://github.com/owner/repository.git`, but found: {remote_url}"
        )

    owner, repository = path_parts
    repository = repository.removesuffix(".git")
    git_url = f"https://github.com/{owner}/{repository}.git"
    return PackageIdentity(owner=owner, repository=repository, git_url=git_url)


def identity_from_repo(package_root: Path, override_url: str | None) -> PackageIdentity:
    if override_url:
        return normalize_github_url(override_url)

    result = run_command(["git", "remote", "get-url", "origin"], cwd=package_root)
    return normalize_github_url(result.stdout)


def discover_semver_tags(package_root: Path) -> tuple[str, ...]:
    result = run_command(["git", "tag", "--list"], cwd=package_root)
    tags = tuple(sorted(tag for tag in result.stdout.splitlines() if SEMVER_TAG_RE.match(tag)))
    if not tags:
        raise SPIAddPackageError(
            "SPI requires at least one semantic-version release tag before submission. "
            "Create and push a real release tag before opening the Add Package form."
        )
    return tags


def confirm_public_repository(identity: PackageIdentity, package_root: Path) -> None:
    run_command(["git", "ls-remote", "--exit-code", identity.git_url, "HEAD"], cwd=package_root)


def check_spi_index_state(identity: PackageIdentity, timeout: float = 10.0) -> str:
    request = urllib.request.Request(identity.spi_url, headers={"User-Agent": "socket-spi-add-package/1"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            if response.status == 200:
                return "indexed"
            return f"unknown-http-{response.status}"
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return "not-indexed"
        return f"unknown-http-{exc.code}"
    except urllib.error.URLError:
        return "unknown-network"


def fetch_url(url: str, timeout: float = 15.0) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": "socket-spi-add-package/1"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8")


def validate_live_add_package_form(form_text: str) -> None:
    required = {
        "form name": "name: Add Package(s)",
        "form title": "title: 'Add <Package>'",
        "default Add Package label": "labels: ['Add Package']",
        "New Packages field id": "id: list",
        "New Packages label": "label: New Packages",
        "required field": "required: true",
    }
    missing = [label for label, needle in required.items() if needle not in form_text]
    if missing:
        raise SPIAddPackageError(
            "SwiftPackageIndex/PackageList changed its Add Package issue form. "
            "Refusing to open a submission until the script is updated. Missing: "
            + ", ".join(missing)
        )


def build_issue_form_url(identity: PackageIdentity) -> str:
    query = urllib.parse.urlencode(
        {
            "template": "add_package.yml",
            "title": f"Add {identity.repository}",
            "list": identity.git_url,
        }
    )
    return f"{PACKAGE_LIST_ISSUE_FORM_URL}?{query}"


def run_readiness(
    package_root: Path,
    *,
    override_url: str | None,
    skip_build: bool,
    skip_tests: bool,
    skip_remote_check: bool,
    skip_index_check: bool,
) -> ReadinessResult:
    package_root = package_root.resolve()
    if not package_root.is_dir():
        raise SPIAddPackageError(f"Package root does not exist: {package_root}")
    if not (package_root / "Package.swift").is_file():
        raise SPIAddPackageError(f"SPI requires Package.swift at the package root: {package_root}")

    checked_steps: list[str] = ["Package.swift"]
    skipped_steps: list[str] = []
    identity = identity_from_repo(package_root, override_url)

    if skip_remote_check:
        skipped_steps.append("public repository check")
    else:
        confirm_public_repository(identity, package_root)
        checked_steps.append("public repository")

    semver_tags = discover_semver_tags(package_root)
    checked_steps.append("semantic version tags")

    run_command(["swift", "package", "dump-package"], cwd=package_root)
    checked_steps.append("swift package dump-package")

    if skip_build:
        skipped_steps.append("swift build")
    else:
        run_command(["swift", "build"], cwd=package_root)
        checked_steps.append("swift build")

    if skip_tests:
        skipped_steps.append("swift test")
    else:
        run_command(["swift", "test"], cwd=package_root)
        checked_steps.append("swift test")

    if (package_root / ".spi.yml").is_file():
        checked_steps.append(".spi.yml present")
    else:
        skipped_steps.append(".spi.yml not present")

    indexed_state = "unknown-skipped"
    if skip_index_check:
        skipped_steps.append("SPI indexed-state check")
    else:
        indexed_state = check_spi_index_state(identity)
        checked_steps.append(f"SPI indexed-state: {indexed_state}")

    if indexed_state == "indexed":
        raise SPIAddPackageError(
            f"{identity.owner}/{identity.repository} already appears to be indexed on SPI: "
            f"{identity.spi_url}"
        )

    return ReadinessResult(
        package_root=package_root,
        identity=identity,
        semver_tags=semver_tags,
        indexed_state=indexed_state,
        checked_steps=tuple(checked_steps),
        skipped_steps=tuple(skipped_steps),
    )


def open_in_browser(url: str, *, browser: str) -> None:
    run_command(["open", "-b", browser, url], cwd=Path.cwd())


def computer_use_handoff(url: str, *, result: ReadinessResult, browser: str) -> dict[str, object]:
    return {
        "mode": "computer-use-hands-free",
        "browser_bundle_id": browser,
        "preferred_browser_name": ZEN_BROWSER_APP_NAME,
        "official_issue_form_url": url,
        "allowed_actions": [
            "Use Computer Use get_app_state for the browser.",
            "Confirm the page is the SwiftPackageIndex/PackageList Add Package(s) issue form.",
            "Confirm the New Packages field contains the package URL exactly once.",
            "Click GitHub's Submit new issue button.",
            "After creation, verify the issue has the Add Package label and report the URL.",
        ],
        "forbidden_actions": [
            "Do not run gh issue create.",
            "Do not add or edit labels directly.",
            "Do not fork SwiftPackageIndex/PackageList.",
            "Do not clone SwiftPackageIndex/PackageList.",
            "Do not edit packages.json.",
            "Do not create or push PackageList branches.",
            "Do not open a PackageList pull request.",
            "Do not touch CLA-triggering contribution paths.",
        ],
        "package": {
            "owner": result.identity.owner,
            "repository": result.identity.repository,
            "git_url": result.identity.git_url,
            "spi_url": result.identity.spi_url,
        },
    }


def print_summary(result: ReadinessResult, issue_form_url: str) -> None:
    print("SPI readiness passed.")
    print(f"Package: {result.identity.owner}/{result.identity.repository}")
    print(f"Repository URL: {result.identity.git_url}")
    print(f"SPI page: {result.identity.spi_url}")
    print(f"SemVer tags found: {', '.join(result.semver_tags[-5:])}")
    print("Checked:")
    for step in result.checked_steps:
        print(f"  - {step}")
    if result.skipped_steps:
        print("Skipped:")
        for step in result.skipped_steps:
            print(f"  - {step}")
    print("Official Add Package issue-form URL:")
    print(issue_form_url)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Validate Swift Package Index readiness and open only the official "
            "SwiftPackageIndex/PackageList Add Package issue form."
        )
    )
    parser.add_argument(
        "mode",
        choices=("readiness", "url", "open", "hands-free"),
        help=(
            "`readiness` checks only, `url` prints the official issue-form URL, "
            "`open` opens the prefilled form, and `hands-free` opens the form plus "
            "prints the Codex Computer Use handoff."
        ),
    )
    parser.add_argument("package_root", nargs="?", default=".", help="Swift package repository root.")
    parser.add_argument("--repo-url", help="Override the GitHub package URL.")
    parser.add_argument("--browser", default=ZEN_BROWSER_BUNDLE_ID, help="Browser bundle id for open/hands-free.")
    parser.add_argument("--skip-build", action="store_true", help="Skip `swift build`.")
    parser.add_argument("--skip-tests", action="store_true", help="Skip `swift test`.")
    parser.add_argument("--skip-remote-check", action="store_true", help="Skip public GitHub remote check.")
    parser.add_argument("--skip-index-check", action="store_true", help="Skip SPI already-indexed check.")
    parser.add_argument("--skip-live-form-check", action="store_true", help="Skip live PackageList form-shape check.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        result = run_readiness(
            Path(args.package_root),
            override_url=args.repo_url,
            skip_build=args.skip_build,
            skip_tests=args.skip_tests,
            skip_remote_check=args.skip_remote_check,
            skip_index_check=args.skip_index_check,
        )
        if args.skip_live_form_check:
            form_text = ""
        else:
            form_text = fetch_url(PACKAGE_LIST_ADD_FORM_URL)
            validate_live_add_package_form(form_text)
        issue_form_url = build_issue_form_url(result.identity)

        print_summary(result, issue_form_url)

        if args.mode in {"open", "hands-free"}:
            open_in_browser(issue_form_url, browser=args.browser)
            print(f"Opened official Add Package issue form in browser bundle `{args.browser}`.")

        if args.mode == "hands-free":
            print("Codex Computer Use handoff:")
            print(json.dumps(computer_use_handoff(issue_form_url, result=result, browser=args.browser), indent=2))

        return 0
    except SPIAddPackageError as exc:
        print(f"SPI add-package gate failed: {exc}", file=sys.stderr)
        return 1
    except urllib.error.URLError as exc:
        print(f"SPI add-package gate failed while reading live SPI/GitHub data: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("SPI add-package gate interrupted.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
