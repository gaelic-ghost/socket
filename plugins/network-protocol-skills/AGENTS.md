# AGENTS.md

This file is the Network Protocol Skills child-repo override for work done from `socket`. Follow the root `socket` guidance for general git, docs, release, branch, dependency-provenance, and maintainer workflow rules.

## Scope

- `network-protocol-skills` is a monorepo-owned Socket child source for Codex networking and application-protocol workflow skills.
- The shipped scope is protocol selection, HTTP/3 and QUIC planning, Media over QUIC draft-aware guidance, WebRTC workflow routing, and transport diagnostics.
- Root [`skills/`](./skills/) is the authored workflow surface.
- The repo root is the Codex plugin root through [`.codex-plugin/plugin.json`](./.codex-plugin/plugin.json).

## Local Rules

- Treat this plugin as the protocol decision layer. It should explain which transport or real-time protocol fits a task, then hand stack-specific implementation to `server-side-swift`, `rust-skills`, `python-skills`, `server-side-jvm`, `web-dev-skills`, `cloud-deployment-skills`, `apple-dev-skills`, or `android-dev-skills`.
- Check current standards, drafts, and implementation docs before making protocol claims. Prefer IETF RFCs, IETF Datatracker drafts, W3C specifications, browser implementation docs, and framework source/docs over memory.
- State protocol maturity plainly. QUIC and HTTP/3 are RFC-backed; WebRTC has W3C and IETF standards plus browser/runtime behavior; Media over QUIC is still draft-driven and must be rechecked before production-facing guidance.
- Keep examples language-neutral unless the target repository has already chosen a stack.
- Do not add MCP servers, runtime daemons, packet-capture scripts, or protocol test tools to this plugin unless a concrete repeated workflow requires deterministic tooling.
- Do not claim live network, NAT traversal, latency, media quality, browser compatibility, or CDN/proxy behavior is verified without an observed run, trace, log, browser check, or deployment check.

## Validation

```bash
uv run python "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" skills/<skill-name>
```

Run the root Socket metadata validator after plugin metadata, marketplace wiring, or root docs change:

```bash
uv run scripts/validate_socket_metadata.py
```
