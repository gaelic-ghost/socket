from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


def _load_module():
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "maintain_plugin_docs.py"
    spec = importlib.util.spec_from_file_location("maintain_plugin_docs", module_path)
    assert spec is not None
    assert spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


m = _load_module()


VALID_README = """# agent-plugin-skills

Installable maintainer skills for skills-export repositories.

## Hard Codex Limitation

OpenAI's current documented Codex plugin system is too restricted to provide proper repo-private plugin scoping.

## Honest Scope

This repository exports installable maintainer skills.

## Exported Skills

- `maintain-plugin-docs`
- `maintain-plugin-repo`
- `bootstrap-skills-plugin-repo`
- `sync-skills-repo-guidance`

## Install Guidance

Install all exported skills with the `skills.sh` flow:

- [skills.sh](https://skills.sh/)

```bash
npx skills add gaelic-ghost/agent-plugin-skills --all
```

## Repository Layout

```text
.
├── skills/
└── README.md
```

## Maintainer Tooling

```bash
uv sync --dev
uv tool install ruff
uv tool install mypy
uv run --group dev pytest
```

## License

See [LICENSE](./LICENSE).
"""


def test_detect_profile_marks_skills_repo(tmp_path: Path) -> None:
    repo = tmp_path / "agent-plugin-skills"
    (repo / "skills").mkdir(parents=True)

    assert m.detect_profile(repo) == "skills-maintainer"


def test_check_sections_accepts_valid_skills_readme(tmp_path: Path) -> None:
    repo = tmp_path / "agent-plugin-skills"
    repo.mkdir()

    issues = m.check_sections(repo, "skills-maintainer", VALID_README)

    assert issues == []


def test_check_sections_flags_missing_tooling_guidance(tmp_path: Path) -> None:
    repo = tmp_path / "agent-plugin-skills"
    repo.mkdir()
    broken = VALID_README.replace("uv tool install ruff\n", "")

    issues = m.check_sections(repo, "skills-maintainer", broken)

    assert any(issue.issue_id == "tooling-guidance-missing-snippet" for issue in issues)


def test_check_sections_flags_missing_all_skills_install_guidance(tmp_path: Path) -> None:
    repo = tmp_path / "agent-plugin-skills"
    repo.mkdir()
    broken = VALID_README.replace("- [skills.sh](https://skills.sh/)\n", "")

    issues = m.check_sections(repo, "skills-maintainer", broken)

    assert any(issue.issue_id == "install-guidance-missing-snippet" for issue in issues)
