# Project Roadmap

## Vision

- Keep `cardhop-app` as the honest mixed repo for Cardhop.app workflow guidance, bundled MCP tooling, and thin Codex plugin packaging.

## Current Milestone

### Milestone 1: initial socket adoption

#### Status

In Progress

#### Scope

- [ ] Land the first monorepo-owned `cardhop-app` child under `socket/plugins/`.
- [ ] Keep the packaged plugin metadata, first skill, and bundled MCP server aligned.

#### Tickets

- [ ] Add the initial `cardhop-contact-workflow` skill.
- [ ] Move the former standalone `cardhop-mcp` server under `mcp/`.
- [ ] Keep root packaging metadata and bundled server docs explicit.

#### Exit Criteria

- [ ] `cardhop-app` ships a root Codex plugin manifest, bundled MCP config, and at least one usable skill.
- [ ] The bundled MCP server validates locally from `mcp/`.
- [ ] The repository docs describe the live mixed skill-plus-server shape accurately.

## History

- Moved the former standalone `cardhop-mcp` checkout into `socket/plugins/cardhop-app` and started the mixed skill-plus-server plugin shape.
