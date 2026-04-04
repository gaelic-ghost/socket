---
name: bootstrap-skills-plugin-repo
description: Bootstrap or align a skills repository to Gale's preferred plugin-first structure with root skills authoring, plugin packaging under plugins/, POSIX symlink mirrors for Codex and Claude discovery, maintainer docs, and AGENTS guidance. Use when creating a new skills repo or structurally aligning an existing one. Do not use this for narrow README-only or roadmap-only maintenance.
---

# Bootstrap Skills Plugin Repo

Bootstrap or align a skills repository to the house layout used for Gale's skills repos.

## Inputs

- Required: target repository root
- Optional: plugin name when it should differ from the repository directory name
- Optional: owner or GitHub namespace for install examples
- Optional: whether the request is check-only planning or real scaffold application

## Workflow

1. Confirm this is structural bootstrap or alignment work, not a narrow README-only or roadmap-only request.
2. Read the existing repo surface before changing anything:
   - `README.md`
   - `AGENTS.md`
   - `ROADMAP.md`
   - `docs/maintainers/reality-audit.md`
   - `docs/maintainers/workflow-atlas.md`
3. Use `scripts/bootstrap_skills_plugin_repo.py` to audit the target structure in `check-only` mode first.
4. If the user wants scaffold creation or alignment, run the script in `apply` mode to create missing repo structure, plugin manifests, marketplace wiring, and POSIX symlink mirrors.
5. Keep root `skills/` as the canonical authored skill surface.
6. Keep plugin, marketplace, MCP, app, and hook manifests under `plugins/<plugin-name>/` and `.agents/plugins/`.
7. Create POSIX symlink mirrors for local discovery:
   - `.agents/skills -> ../skills`
   - `.claude/skills -> ../skills`
   - `plugins/<plugin-name>/skills -> ../../skills`
8. Preserve existing repo-specific guidance. Merge missing house guidance into docs and `AGENTS.md` without flattening local policy.
9. Seed maintainer Python tooling guidance so bootstrapped repos call out `uv sync --dev`, `uv tool install ruff`, `uv tool install mypy`, and `uv run --group dev pytest`.
10. Use `$skill-creator` for individual skill authoring. This skill owns repo structure, not per-skill content design.
11. Validate the resulting repo layout, symlinks, manifests, and docs alignment before closing.

## Output Contract

- Return a short summary plus JSON with:
  - `run_context`
  - `findings`
  - `apply_actions`
  - `created_paths`
  - `errors`
- If there are no findings, no apply actions, and no errors, output exactly `No findings.`

## Guardrails

- Never overwrite an existing `README.md`, `AGENTS.md`, or maintainer doc wholesale.
- Never use this skill as a substitute for `$skill-creator`.
- Never claim Windows-native symlink behavior is guaranteed. This layout assumes macOS or Linux development, including WSL 2 when Windows is involved.
- Never leave the repo ambiguous about which surfaces are canonical authoring versus packaging or discovery mirrors.
- Do not use this skill for README-only, roadmap-only, or single-skill content changes.

## References

- `references/bootstrap-contract.md`
- `references/posix-symlink-policy.md`
