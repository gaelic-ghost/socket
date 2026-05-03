from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest


MODULE_PATH = Path(__file__).resolve().parent.parent / "scripts" / "spi_add_package.py"
SPEC = importlib.util.spec_from_file_location("spi_add_package", MODULE_PATH)
assert SPEC and SPEC.loader
spi_add_package = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = spi_add_package
SPEC.loader.exec_module(spi_add_package)


VALID_FORM = """\
name: Add Package(s)
description: Add one or more new packages to the Swift Package Index.
title: 'Add <Package>'
labels: ['Add Package']
body:
  - type: textarea
    id: list
    attributes:
      label: New Packages
    validations:
      required: true
"""


def test_normalize_github_url_accepts_ssh_and_adds_git_suffix() -> None:
    identity = spi_add_package.normalize_github_url("git@github.com:gaelic-ghost/SwiftASB.git")

    assert identity.owner == "gaelic-ghost"
    assert identity.repository == "SwiftASB"
    assert identity.git_url == "https://github.com/gaelic-ghost/SwiftASB.git"


def test_build_issue_form_url_uses_only_official_template_fields() -> None:
    identity = spi_add_package.PackageIdentity(
        owner="gaelic-ghost",
        repository="SwiftASB",
        git_url="https://github.com/gaelic-ghost/SwiftASB.git",
    )

    url = spi_add_package.build_issue_form_url(identity)

    assert url.startswith("https://github.com/SwiftPackageIndex/PackageList/issues/new?")
    assert "template=add_package.yml" in url
    assert "title=Add+SwiftASB" in url
    assert "list=https%3A%2F%2Fgithub.com%2Fgaelic-ghost%2FSwiftASB.git" in url
    assert "labels=" not in url
    assert "body=" not in url


def test_validate_live_add_package_form_rejects_missing_default_label() -> None:
    form = VALID_FORM.replace("labels: ['Add Package']\n", "")

    with pytest.raises(spi_add_package.SPIAddPackageError, match="default Add Package label"):
        spi_add_package.validate_live_add_package_form(form)


def test_validate_live_add_package_form_rejects_missing_list_field() -> None:
    form = VALID_FORM.replace("id: list", "id: urls")

    with pytest.raises(spi_add_package.SPIAddPackageError, match="New Packages field id"):
        spi_add_package.validate_live_add_package_form(form)


def test_validate_mode_rejects_skip_flags_for_hands_free() -> None:
    args = spi_add_package.parse_args(["hands-free", ".", "--skip-tests"])

    with pytest.raises(spi_add_package.SPIAddPackageError, match="complete readiness"):
        spi_add_package.validate_mode_and_skip_flags(args)


def test_dump_package_json_requires_products(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    completed = spi_add_package.subprocess.CompletedProcess(
        args=["swift", "package", "dump-package"],
        returncode=0,
        stdout='{"name":"Empty","products":[]}',
        stderr="",
    )
    monkeypatch.setattr(spi_add_package, "run_command", lambda *_args, **_kwargs: completed)

    with pytest.raises(spi_add_package.SPIAddPackageError, match="at least one"):
        spi_add_package.dump_package_json(tmp_path)


def test_confirm_swift_tools_version_rejects_legacy_manifest(tmp_path: Path) -> None:
    (tmp_path / "Package.swift").write_text("// swift-tools-version: 4.2\n", encoding="utf-8")

    with pytest.raises(spi_add_package.SPIAddPackageError, match="Swift 5.0 or later"):
        spi_add_package.confirm_swift_tools_version(tmp_path)


def test_confirm_remote_semver_tag_requires_pushed_release_tag(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    identity = spi_add_package.PackageIdentity(
        owner="gaelic-ghost",
        repository="SwiftASB",
        git_url="https://github.com/gaelic-ghost/SwiftASB.git",
    )
    completed = spi_add_package.subprocess.CompletedProcess(
        args=["git", "ls-remote", "--tags", identity.git_url],
        returncode=0,
        stdout="abc123\trefs/tags/v0.0.1\n",
        stderr="",
    )
    monkeypatch.setattr(spi_add_package, "run_command", lambda *_args, **_kwargs: completed)

    with pytest.raises(spi_add_package.SPIAddPackageError, match="none were visible"):
        spi_add_package.confirm_remote_semver_tag(identity, tmp_path, ("v1.0.0",))


def test_computer_use_handoff_forbids_failed_external_paths() -> None:
    result = spi_add_package.ReadinessResult(
        package_root=Path("/tmp/SwiftASB"),
        identity=spi_add_package.PackageIdentity(
            owner="gaelic-ghost",
            repository="SwiftASB",
            git_url="https://github.com/gaelic-ghost/SwiftASB.git",
        ),
        semver_tags=("v0.1.0",),
        indexed_state="not-indexed",
        checked_steps=("Package.swift",),
        skipped_steps=(),
    )

    handoff = spi_add_package.computer_use_handoff(
        "https://github.com/SwiftPackageIndex/PackageList/issues/new?template=add_package.yml",
        result=result,
        browser=spi_add_package.ZEN_BROWSER_BUNDLE_ID,
    )
    forbidden_text = "\n".join(handoff["forbidden_actions"])

    assert handoff["browser_bundle_id"] == "app.zen-browser.zen"
    assert "gh issue create" in forbidden_text
    assert "packages.json" in forbidden_text
    assert "fork SwiftPackageIndex/PackageList" in forbidden_text
    assert "pull request" in forbidden_text


def test_source_does_not_contain_forbidden_package_list_write_commands() -> None:
    source = MODULE_PATH.read_text(encoding="utf-8")

    forbidden_snippets = [
        'run_command(["gh"',
        "subprocess.run([\"gh\"",
        "create-pull-request",
        "--label Add Package",
        "SwiftPackageIndex/PackageList.git",
    ]
    for snippet in forbidden_snippets:
        assert snippet not in source
