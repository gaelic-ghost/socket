# agent-plugin-skills

Installable maintainer skills for skills-export repositories.

For maintainer policy, source-of-truth order, and standards references, see [AGENTS.md](./AGENTS.md).

For the durable maintainer map of Codex marketplace catalogs, staged plugin roots, installed cache paths, and config enabled-state, see [docs/maintainers/codex-plugin-install-surfaces.md](./docs/maintainers/codex-plugin-install-surfaces.md).

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

## Codex Plugin Install Map

Codex's documented plugin model splits plugin wiring across separate surfaces that do different jobs. Keeping them distinct makes local installs much easier to reason about.

### The Four Surfaces

1. Marketplace catalog
   - A marketplace file is a catalog that Codex can read from.
   - Personal marketplace: `~/.agents/plugins/marketplace.json`
   - Repo marketplace: `$REPO_ROOT/.agents/plugins/marketplace.json`
   - The marketplace entry says "this plugin exists in this marketplace" and points `source.path` at the staged plugin directory that Codex should read.
2. Staged plugin directory
   - This is the plugin payload on disk: `.codex-plugin/plugin.json`, `skills/`, optional hooks, apps, and MCP packaging.
   - Common personal pattern: `~/.codex/plugins/<plugin-name>`
   - Common repo pattern from the docs: `$REPO_ROOT/plugins/<plugin-name>`
   - The marketplace points at this directory, but it is not the marketplace itself.
3. Installed plugin cache
   - Codex installs plugins into `~/.codex/plugins/cache/$MARKETPLACE_NAME/$PLUGIN_NAME/$VERSION/`.
   - For local plugins, the docs say `$VERSION` is `local`.
   - This is Codex's installed copy, not the source directory you usually edit directly.
4. Enabled-state config
   - Codex stores each plugin's on or off state in `~/.codex/config.toml`.
   - Plugin keys are scoped by plugin name plus marketplace name, for example `[plugins."agent-plugin-skills@socket"]`.
   - This answers "is this marketplace-scoped plugin enabled?" not "where is the plugin stored?"

### Practical Mental Model

- The marketplace is the catalog.
- The staged plugin directory is the source payload the catalog points at.
- The installed cache is Codex's installed copy.
- `config.toml` is the per-plugin on or off switch.

That means a personal marketplace file is not an "install destination". It is a catalog of plugins that your Codex install can see and install from. The actual personal staged plugin tree usually lives under `~/.codex/plugins/`, and Codex's installed cache lives under `~/.codex/plugins/cache/`.

Likewise, a repo marketplace is still just a catalog. The difference is scope and visibility: it is attached to one repo, so plugins exposed there are visible in that repo's Codex context. If a repo tracks that marketplace in git, it is advertising those plugins as part of the repo-visible surface.

Repo-local config is separate again. If a repo has a project-scoped `.codex/config.toml`, that file can override plugin enabled-state for that repo context. It does not replace the marketplace catalog. It answers whether a plugin identity such as `my-plugin@local-repo` should be enabled when Codex is running in that project.

### Repo Scope vs Personal Scope

- Personal scope
  - Catalog: `~/.agents/plugins/marketplace.json`
  - Common staged payload path: `~/.codex/plugins/<plugin-name>`
  - Enabled-state: `~/.codex/config.toml`
- Repo scope
  - Catalog: `$REPO_ROOT/.agents/plugins/marketplace.json`
  - Common staged payload path from the docs: `$REPO_ROOT/plugins/<plugin-name>`
  - Optional repo-scoped enabled-state override: `$REPO_ROOT/.codex/config.toml`

This repository intentionally stays source-first and does not ship a nested repo-local Codex plugin install surface for itself. Local authoring mirrors such as [`.agents/skills`](./.agents/skills) and [`.claude/skills`](./.claude/skills) are discovery mirrors for source skills, not packaged plugin install roots.

Authoritative references for this model:

- [OpenAI Codex plugin build docs](https://developers.openai.com/codex/plugins/build)
- [How Codex uses marketplaces](https://developers.openai.com/codex/plugins/build#how-codex-uses-marketplaces)
- [Install a local plugin manually](https://developers.openai.com/codex/plugins/build#install-a-local-plugin-manually)
- [Marketplace metadata](https://developers.openai.com/codex/plugins/build#marketplace-metadata)
- [Remove or turn off a plugin](https://developers.openai.com/codex/plugins#remove-or-turn-off-a-plugin)

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

Install the full exported skills set at once through [skills.sh](https://skills.sh/):

```bash
npx skills add gaelic-ghost/agent-plugin-skills --all
```

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
