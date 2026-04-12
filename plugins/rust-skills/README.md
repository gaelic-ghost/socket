# rust-skills

Placeholder plugin repository for future Rust-focused Codex skills.

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

`rust-skills` is a real plugin repository, but it does not ship authored Rust skills yet.

### What This Project Is

This repository reserves the future Codex plugin surface for Rust-focused skills and keeps the placeholder packaging honest until real skills land.

### Motivation

It exists to keep future Rust workflow work in a dedicated repository instead of mixing that work into unrelated plugin repos too early.

## Setup

There is no end-user quick start yet because the repository does not ship actual skill content. Use the maintainer workflow here only if you are preserving the placeholder repository shape or preparing the first real skill surface.

## Usage

There is no meaningful runtime usage yet. Today this repository is a packaging placeholder plus roadmap.

## Development

### Setup

Review [AGENTS.md](./AGENTS.md), [ROADMAP.md](./ROADMAP.md), and the plugin manifest at [`.codex-plugin/plugin.json`](./.codex-plugin/plugin.json) before expanding the repo.

### Workflow

Keep the repo minimal until the first real skill exists. Add packaging, docs, and validation only when the shipped surface actually earns them.

## Verification

Current verification is lightweight:

- keep [`.codex-plugin/plugin.json`](./.codex-plugin/plugin.json) valid
- keep placeholder docs honest about the repo not shipping real skills yet
- add real validation commands only when the repository starts shipping executable or testable skill content

## Release Notes

Use Git history for placeholder-stage changes. Add GitHub release tracking once the repository begins shipping real Rust skill content.

## License

See [LICENSE](./LICENSE).

## Repository Layout

```text
.
├── .codex-plugin/
│   └── plugin.json
├── AGENTS.md
├── LICENSE
├── README.md
└── ROADMAP.md
```
