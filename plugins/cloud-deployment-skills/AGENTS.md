# AGENTS.md

This file is the Cloud Deployment Skills child-repo override for work done from `socket`. Follow the root `socket` guidance for general git, docs, release, branch, dependency-provenance, and maintainer workflow rules.

## Scope

- `cloud-deployment-skills` is a monorepo-owned Socket child and the canonical source of truth for shipped cloud-provider deployment routing skills.
- Root [`skills/`](./skills/) is the authored workflow surface.
- The repo root is the Codex plugin root through [`.codex-plugin/plugin.json`](./.codex-plugin/plugin.json).
- Keep this plugin focused on provider selection, official-tool routing, deployment readiness, and cross-provider handoffs.
- Keep framework-specific application implementation in the owning stack plugins such as `server-side-swift`, `web-dev-skills`, `python-skills`, `dotnet-skills`, `rust-skills`, and `server-side-jvm`.

## Local Rules

- Match the `socket` shared semantic version exactly; use the Socket root release workflow for version inventory and bumps.
- Prefer official provider plugins, MCP servers, CLIs, and docs before adding Socket-authored setup guidance.
- For AWS work, route Codex users to the official `aws/agent-toolkit-for-aws` marketplace and its `aws-core` plugin before considering Socket-owned AWS guidance.
- Do not bundle AWS MCP configuration, AWS CLI setup instructions, AWS SAM setup instructions, or copied AWS Agent Toolkit skills in this plugin while the official AWS plugin owns that surface.
- Treat provider credentials, account configuration, API mutation, billing, and production deployment as high-impact operations. Verify the target account, region, profile, project, and intended mutation before taking action.
- Keep provider-specific skills small and explicit. Add a new provider workflow only when it removes real routing ambiguity or covers a provider that does not already offer a first-party agent plugin.
- Do not commit machine-local credentials, profiles, `.env` files, cloud state, generated deployment artifacts, or local cache paths.
- Use repo-local files, checked-out provider config, provider CLIs, and official provider documentation before making claims about current deployment behavior.
