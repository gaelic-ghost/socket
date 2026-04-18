# AGENTS.md

Use this file for durable repo-local guidance that Codex should follow before changing code, docs, or project workflow surfaces in this repository.

## Repository Scope

### What This File Covers

- `socket` is Gale's local Codex plugin and skills superproject.
- Use it to coordinate the child repositories under [`plugins/`](./plugins/), the repo-root marketplace at [`.agents/plugins/marketplace.json`](./.agents/plugins/marketplace.json), and the root maintainer docs.
- Treat this repository as a conscious stopgap around OpenAI's current documented Codex plugin-scoping limits, not as proof that Codex supports richer shared-parent or repo-private plugin scoping than the documented marketplace model.
- These defaults apply across the nested plugin and skills repositories unless a closer `AGENTS.md` narrows them.

### Where To Look First

- Start with [README.md](./README.md), [CONTRIBUTING.md](./CONTRIBUTING.md), [ROADMAP.md](./ROADMAP.md), and [`docs/maintainers/subtree-workflow.md`](./docs/maintainers/subtree-workflow.md).
- Use [`docs/maintainers/plugin-packaging-strategy.md`](./docs/maintainers/plugin-packaging-strategy.md) when the question is about the root marketplace or the independent-plugin packaging stance.
- When a task is really about one child repo's own behavior, read that child repo's docs before reading broadly across the superproject.

## Working Rules

### Change Scope

- Treat Gale's local `socket` checkout as the normal day-to-day working checkout on `main`.
- Direct work on local `main` is the default for `socket` unless Gale explicitly asks for a feature branch or a dedicated worktree.
- Use a feature branch or worktree when the change needs isolation for safety, review, or overlapping parallel work, but do not force that path for ordinary `socket` maintenance.
- Prefer small, focused commits over broad mixed changes.
- For ordinary fixes in monorepo-owned child directories, edit the relevant copy under `plugins/` directly in `socket`.
- For `apple-dev-skills`, `python-skills`, and `SpeakSwiftlyServer`, keep subtree sync operations explicit and isolated from unrelated edits.
- When a child repo gains, removes, or moves plugin packaging, update [`.agents/plugins/marketplace.json`](./.agents/plugins/marketplace.json), [README.md](./README.md), and the root maintainer docs in the same pass.

### Source of Truth

- Treat managed production installs such as `~/.agents/skills` as read-only deployment artifacts while working in these development repositories.
- When a repository ships reusable skills, treat the top-level authored surface such as `skills/`, `mcps/`, or `apps/` as the source of truth. Treat plugin manifests, marketplace files, and nested packaged plugin roots as packaging metadata unless a nearer `AGENTS.md` explicitly says otherwise.
- Keep installed skills independent from repo-level docs under `docs/`.
- Prefer POSIX symlink discovery mirrors over duplicate or hardlinked skill trees when a repo exposes `.agents/skills` or `.claude/skills`.
- Do not track consumer-side install copies, cache directories, or machine-local runtime state in git.
- Keep the same names for the same concepts across `SKILL.md`, `agents/openai.yaml`, docs, automation prompts, scripts, and marketplace metadata.
- If docs and scripts disagree, fix the script or narrow the documented contract so they match.
- When shipped behavior, active skill inventory, packaging roots, or validation commands change, update the relevant docs and `ROADMAP.md` in the same pass unless Gale explicitly says not to.
- For Python-backed skill repositories, prefer `uv sync --dev`, `uv run pytest`, and uv-managed maintainer tools such as `ruff` and `mypy`.
- When OpenAI or Claude product behavior matters, prefer official docs first. When describing Codex plugin boundaries, say plainly that repo-visible plugins come from the documented marketplace model and that OpenAI does not currently document a richer repo-private scoping model.
- Use these terms consistently:
  - `skill`: reusable workflow-authoring unit
  - `plugin`: installable distribution bundle
  - `subagent`: delegated runtime worker with its own context and tool policy

### Communication and Escalation

- Start from the root docs when the task is about the mixed monorepo model, root marketplace wiring, subtree sync for `apple-dev-skills`, `python-skills`, or `SpeakSwiftlyServer`, or superproject release flow.
- Start from the child repo docs when the task is really about one child repo's own behavior.
- If scope widens from one root concern into a cross-repo or packaging-policy change, stop and surface that widening before continuing.
- When a historical maintainer doc no longer carries live decision-making value, collapse its durable conclusions into `ROADMAP.md` or a still-live reference doc instead of preserving another stale planning note.

## Commands

### Setup

```bash
uv sync --dev
```

### Validation

```bash
uv run scripts/validate_socket_metadata.py
```

### Optional Project Commands

```bash
git subtree pull --prefix=plugins/apple-dev-skills apple-dev-skills main
git subtree push --prefix=plugins/apple-dev-skills apple-dev-skills main
git subtree pull --prefix=plugins/python-skills python-skills main
git subtree push --prefix=plugins/python-skills python-skills main
git subtree pull --prefix=plugins/SpeakSwiftlyServer speak-swiftly-server main
git subtree push --prefix=plugins/SpeakSwiftlyServer speak-swiftly-server main
```

Use these commands only when the work is intentionally publishing or syncing one of the remaining subtree-managed child repos.

## Review and Delivery

### Review Expectations

- Use the shared house style for commit messages across terminal Git, Codex-driven commits, and subtree-managed child repo work.
- Default commit subject format is a short lowercase kebab-case scope, one colon, one space, and an imperative summary such as `docs: tighten root docs`, with no trailing period.
- For bigger, wider, riskier, refactor, breaking, or release commits, keep the same scoped subject and add concise body sections when relevant in this order: `Why:`, `Breaking:`, `Verification:`.
- Prefer concrete scopes such as `runtime`, `normalize`, `forensics`, `models`, `docs`, `tests`, `release`, `build`, `plugin`, or `subtree`, and describe the real changed surface instead of vague intent.

### Definition of Done

- The change clearly belongs at the `socket` superproject layer or intentionally uses the documented subtree workflow for one child repo.
- Root docs and marketplace wiring are updated together when packaging or policy changed.
- The root validation path ran when marketplace metadata or packaged plugin paths changed.
- Child-repo-specific validation ran from the relevant child repo when the real change lives there.

## Safety Boundaries

### Never Do

- Do not import non-git directories as subtrees.
- Do not hand-edit subtree history to make imported child repos look monorepo-native.
- Do not re-vendor one child plugin repo inside another nested directory when the top-level copy already exists in `socket`.
- Do not assume every child surface exposes `.codex-plugin/plugin.json` at its directory root.
- Do not invent a second packaging layer at the superproject root when a child repo already has a real packaged plugin root.

### Ask Before

- Ask before adding or reintroducing a subtree-managed child repo.
- Ask before broadening `socket` from a superproject stopgap into a stronger packaging or bundle abstraction.
- Ask before deleting a root maintainer doc unless its durable conclusions have already been moved into `ROADMAP.md` or a still-live root reference.

## Local Overrides

- Nested `AGENTS.md` files under `plugins/` refine this root guidance for their own repo shapes, domain rules, validation paths, and packaging boundaries.
