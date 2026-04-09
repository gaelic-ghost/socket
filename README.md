# agent-plugin-skills

Installable maintainer skills for skills-export repositories.

For maintainer policy, source-of-truth order, and standards references, see [AGENTS.md](./AGENTS.md).

## Hard Codex Limitation

OpenAI's current documented Codex plugin system is too restricted to provide proper repo-private plugin scoping.

- Codex documents one repo marketplace at `$REPO_ROOT/.agents/plugins/marketplace.json`.
- Codex documents one personal marketplace at `~/.agents/plugins/marketplace.json`.
- A repo-local plugin that Codex can discover is exposed through that repo marketplace.
- If that repo marketplace entry is tracked in git, the repo is advertising that plugin as part of the repo's exported product surface.
- OpenAI does not document hidden repo-local plugin installs, private scoped plugin packs, or a second repo marketplace file that Codex will use for repo scope.

This repository does not pretend otherwise. It is a global-install skills-export repository. It does not ship a nested repo-local Codex plugin copy of itself, and it does not ship workflows that normalize or hide those Codex limitations.

Authoritative references:

- [OpenAI Codex plugin build docs](https://developers.openai.com/codex/plugins/build)
- [Install a local plugin manually](https://developers.openai.com/codex/plugins/build#install-a-local-plugin-manually)
- [How Codex uses marketplaces](https://developers.openai.com/codex/plugins/build#how-codex-uses-marketplaces)
- [OpenAI Codex skills docs](https://developers.openai.com/codex/skills)

## Honest Scope

This repository does two honest things:

- exports installable maintainer skills from root [`skills/`](./skills/)
- keeps those skills blunt about what OpenAI's documented Codex plugin system can and cannot do

It does not ship an installer skill. It does not ship an install-validation skill. It does not track a nested plugin directory for itself.

## Exported Skills

- `maintain-plugin-repo`
  - Repo-level maintainer entrypoint for auditing and tightening a skills-export repository.
- `maintain-plugin-docs`
  - Docs-maintenance helper for README, ROADMAP, and cross-doc drift in skills-export repositories.
- `bootstrap-skills-plugin-repo`
  - Bootstrap and structural-alignment helper for creating a clean skills-export repository with root `skills/` and local discovery mirrors.
- `sync-skills-repo-guidance`
  - Guidance-alignment helper for keeping README, AGENTS, ROADMAP, maintainer docs, and discovery mirrors in sync.

## Install Guidance

### Vercel `skills` CLI

Install one skill:

```bash
npx skills add gaelic-ghost/agent-plugin-skills --skill maintain-plugin-repo
```

Install the whole exported set:

```bash
npx skills add gaelic-ghost/agent-plugin-skills --all
```

### Codex And Claude Local Authoring In This Repo

For local authoring work in this repository, the source skills are discoverable through the repo mirrors below.

- Codex local authoring mirror: [`.agents/skills`](./.agents/skills)
- Claude local authoring mirror: [`.claude/skills`](./.claude/skills)

Those mirrors exist so the source skills are usable while this repository is being developed. They are not a nested packaged plugin surface.

Claude Code continues to support direct `.claude/skills` discovery for local authoring, while its documented plugin workflow is a separate `.claude-plugin/` packaging surface that you can test with `claude --plugin-dir`. This repository intentionally ships only the local `skills/` mirror for Claude authoring, not a bundled Claude plugin.

## Repository Layout

```text
.
├── .agents/
│   └── skills -> ../skills
├── .claude/
│   └── skills -> ../skills
├── README.md
├── AGENTS.md
├── skills/
│   ├── bootstrap-skills-plugin-repo/
│   ├── maintain-plugin-docs/
│   ├── maintain-plugin-repo/
│   └── sync-skills-repo-guidance/
├── docs/
│   └── maintainers/
├── ROADMAP.md
└── pyproject.toml
```

## Maintainer Tooling

```bash
uv sync --dev
uv tool install ruff
uv tool install mypy
uv run --group dev pytest
```

## License

Apache License 2.0. See [LICENSE](./LICENSE).
