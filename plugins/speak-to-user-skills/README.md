# speak-to-user-skills

Standalone plugin repository for future speech-facing and spoken-reply Codex skills.

## Table of Contents

- [Overview](#overview)
- [Setup](#setup)
- [Usage](#usage)
- [Development](#development)
- [Release Notes](#release-notes)
- [Verification](#verification)
- [License](#license)
- [Repository Layout](#repository-layout)

## Overview

This repository is intentionally minimal right now.

- it is a real Git source repository again
- it ships baseline Codex plugin packaging
- skill content has not been authored yet
- the repository stays compatible with `socket` subtree import and sync workflows

Track the placeholder plan in [ROADMAP.md](./ROADMAP.md) until the first real exported skill lands.

### Status

This repository is still a placeholder and is not shipping authored speak-to-user skills yet.

### What This Project Is

This repository owns the future install surface for user-facing speech and narration workflow skills once real content lands.

### Motivation

It exists to reserve a clean standalone home for future speech-oriented skills instead of burying that work in unrelated repos.

## Setup

There is no real end-user quick start yet. Use the Development and ROADMAP sections if you are maintaining the placeholder repository shape.

## Usage

There is no meaningful runtime usage yet because the repository does not ship authored speak-to-user skills today.

## Development

### Setup

Clone the repository and review the placeholder packaging and roadmap before adding the first real exported skill.

### Workflow

Keep the repository minimal until the first real skill exists, then expand docs, validation, and packaging only as the shipped surface earns it.

## Verification

Review the placeholder packaging files, keep the docs honest, and add real validation commands only when the repository starts shipping executable skill content.

## Release Notes

Use Git history now for placeholder-repo changes, and add GitHub release tracking once the repository starts shipping real speech-facing skill content.

## License

See [LICENSE](./LICENSE).

## Repository Layout

```text
.
├── .codex-plugin/
│   └── plugin.json
├── AGENTS.md
├── README.md
└── ROADMAP.md
```
