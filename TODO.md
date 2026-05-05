# TODO

This file is the Socket-level backlog for child plugins that no longer keep their own `ROADMAP.md` files. `apple-dev-skills` is the exception and keeps its roadmap in `plugins/apple-dev-skills/ROADMAP.md`.

## Active Child Plugins

### agent-plugin-skills

- [ ] Finish docs visibility and wording hardening across exported skills.
- [ ] Keep Git-backed Codex marketplace install and update guidance ahead of local authoring notes.
- [ ] Keep repo-local discovery mirror guidance separate from install guidance.
- [ ] Add or refine troubleshooting language for confusing Codex plugin expectations.
- [ ] Add a maintainer workflow for moving or re-homing skills between repositories.
- [ ] Add durable process support for noticing changes in the Agent Skills standard and OpenAI docs.
- [ ] Define an eval workflow for shipped skills against real Codex runtimes.

### cardhop-app

- [ ] Finish initial Socket adoption for the Cardhop child plugin.
- [ ] Keep `cardhop-contact-workflow`, bundled MCP server docs, `.mcp.json`, and plugin metadata aligned.
- [ ] Validate the bundled MCP server from `plugins/cardhop-app/mcp/`.

### productivity-skills

- [ ] Add `maintain-project-security` for canonical `SECURITY.md` maintenance.
- [ ] Add `maintain-project-support` for canonical `SUPPORT.md` maintenance.
- [ ] Add a future `maintain-project-hooks` workflow for repositories that intentionally use Codex Hooks.
- [ ] Add lightweight validation tooling for `SKILL.md`, frontmatter, and `agents/openai.yaml` alignment.
- [ ] Add validation checks for README layout and active skill inventory consistency.

### python-skills

- [ ] Finish documentation and maintainer-surface alignment around `skills/`, `.codex-plugin/plugin.json`, and Socket-root contribution workflow.
- [ ] Keep `README.md`, `AGENTS.md`, and Socket-root contributor guidance clearly separated.
- [ ] Confirm `uv run scripts/validate_repo_metadata.py` and `uv run pytest` still pass after docs or metadata changes.
- [ ] Add lightweight validation for future Codex metadata changes.

### things-app

- [ ] Finish guidance and maintenance modernization for the mixed Things skill plus bundled MCP server repo.
- [ ] Keep root README and AGENTS guidance clear about whether a change belongs in `skills/`, `mcp/`, or plugin metadata.
- [ ] Expand repo-root maintainer tooling once more than one root skill needs Python-backed verification.
- [ ] Add broader bundled-server smoke coverage when new Things tool families or auth-sensitive update flows are introduced.
- [ ] Revisit packaging mirrors if the repo starts shipping additional Codex discovery surfaces.

## Placeholder Child Plugins

### dotnet-skills

- [ ] Author the first real .NET-focused skill for Codex.
- [ ] Update docs to describe shipped behavior once real skill content exists.
- [ ] Add the minimum validation or smoke coverage needed for the shipped skill surface.
- [ ] Decide whether the long-term home remains Socket-owned or becomes standalone.

### rust-skills

- [ ] Author the first real Rust-focused skill for Codex.
- [ ] Update docs to describe shipped behavior once real skill content exists.
- [ ] Add the minimum validation or smoke coverage needed for the shipped skill surface.
- [ ] Decide whether the long-term home remains Socket-owned or becomes standalone.

### spotify

- [ ] Author the first real Spotify-focused Codex workflow.
- [ ] Add the first maintained Spotify skill, app, or MCP-backed workflow under the canonical exported surface.
- [ ] Update docs and validation once the exported Spotify surface is real.
- [ ] Decide whether Socket remains the canonical home after the first real shipped workflow.

### web-dev-skills

- [ ] Author the first real web-focused skill for Codex.
- [ ] Update docs to describe shipped behavior once real skill content exists.
- [ ] Add the minimum validation or smoke coverage needed for the shipped skill surface.
- [ ] Decide whether the long-term home remains Socket-owned or becomes standalone.
