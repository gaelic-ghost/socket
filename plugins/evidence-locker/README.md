# evidence-locker

Placeholder plugin repository for future evidence-collection, preservation, and review workflows.

## Table of Contents

- [Overview](#overview)
- [Setup](#setup)
- [Usage](#usage)
- [Development](#development)
- [Verification](#verification)
- [Release Notes](#release-notes)
- [License](#license)
- [Repository Layout](#repository-layout)

## Overview

This repository is intentionally minimal today.

### Status

`evidence-locker` is a real plugin repository, but it does not ship authored evidence workflows yet.

### What This Project Is

This repository reserves a dedicated Codex plugin surface for future evidence collection, preservation, audit, and review workflows.

### Motivation

It exists to keep evidence-focused workflow work in its own child repository instead of mixing that work into unrelated plugins before the real surface is ready.

## Setup

There is no end-user quick start yet because the repository does not ship actual skills, apps, or MCP server wiring. Use the maintainer workflow here only when preserving the placeholder shape or preparing the first real evidence surface.

## Usage

There is no meaningful runtime usage yet. Today this repository is a packaging placeholder plus roadmap.

## Development

### Setup

Review [AGENTS.md](./AGENTS.md), [ROADMAP.md](./ROADMAP.md), and [`.codex-plugin/plugin.json`](./.codex-plugin/plugin.json) before expanding the repo.

### Workflow

Keep the repository minimal until the first real evidence workflow exists. Add skills, MCP wiring, apps, docs, and validation only when the shipped surface actually earns them.

## Verification

Current verification is lightweight:

- keep [`.codex-plugin/plugin.json`](./.codex-plugin/plugin.json) valid
- keep placeholder docs honest about the repo not shipping real workflow content yet
- add real validation commands only when the repository starts shipping executable or testable evidence surfaces

## Release Notes

Use Git history for placeholder-stage changes. Add GitHub release tracking once the repository begins shipping real evidence workflow content.

## License

See the root [LICENSE](../../LICENSE).

## Repository Layout

```text
.
├── .codex-plugin/
│   └── plugin.json
├── AGENTS.md
├── README.md
└── ROADMAP.md
```
