from __future__ import annotations

from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parent.parent


def surface(plugin: str, skill: str, *references: str) -> str:
    root = ROOT / "plugins" / plugin / "skills" / skill
    paths = [root / "SKILL.md", *(root / "references" / name for name in references)]
    return "\n".join(path.read_text(encoding="utf-8").lower() for path in paths)


@pytest.mark.parametrize(
    ("plugin", "skill", "references", "phrases"),
    [
        (
            "apple-dev-skills",
            "macos-privacy-permissions-workflow",
            ("responsible-code-and-attribution.md", "permission-class-matrix.md"),
            ("helper or xpc", "axisprocesstrustedwithoptions", "responsible executable"),
        ),
        (
            "apple-dev-skills",
            "macos-privacy-permissions-workflow",
            ("permission-class-matrix.md",),
            ("epdevelopertool.authorizationstatus", "requestaccess()", "do not promise ui"),
        ),
        (
            "apple-dev-skills",
            "macos-privacy-permissions-workflow",
            ("permission-class-matrix.md", "responsible-code-and-attribution.md"),
            ("controller-target pair", "nsappleeventsusagedescription", "terminal"),
        ),
        (
            "apple-dev-skills",
            "macos-sandbox-file-access-workflow",
            ("security-scoped-bookmark-lifecycle.md",),
            ("startaccessingsecurityscopedresource()", "stopaccessingsecurityscopedresource()", "if stale"),
        ),
        (
            "apple-dev-skills",
            "diagnose-apple-entitlements",
            ("five-state-entitlement-comparison.md", "artifact-and-nested-code-inspection.md"),
            ("tracked source", "account authorization", "signed result", "runtime result", "helper"),
        ),
        (
            "apple-dev-skills",
            "macos-sandbox-file-access-workflow",
            ("sandbox-and-filesystem-control-map.md",),
            ("posix and acl", "app sandbox", "tcc", "data vault/sip"),
        ),
        (
            "cybersecurity-skills",
            "assess-macos-threat",
            ("macos-security-layers.md",),
            ("xprotect", "not automatically proof of prior execution", "research-macos-security-control"),
        ),
        (
            "reverse-engineering-skills",
            "research-macos-security-control",
            ("technical-note-contract.md", "source-and-evidence-hierarchy.md"),
            ("private implementation evidence", "not public api", "exact macos version/build"),
        ),
    ],
)
def test_planned_forward_scenario_has_an_explicit_decision_path(
    plugin: str,
    skill: str,
    references: tuple[str, ...],
    phrases: tuple[str, ...],
) -> None:
    contents = surface(plugin, skill, *references)
    missing = [phrase for phrase in phrases if phrase not in contents]
    assert not missing, f"{plugin}:{skill} is missing forward-test decisions: {missing}"
