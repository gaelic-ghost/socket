# socket

Gale's Codex plugin marketplace for macOS users and Apple/Swift devs. Includes companion plugins for my other packages, like SwiftASB.

![Codex plugin directory filtered to the Socket marketplace, showing Productivity Skills featured above installable Socket child plugins.](./docs/media/codex-plugin-directory-socket-productivity-skills.png)

`Socket` is the "marketplace", or catalog, of available plugins. Add `socket` to Codex, then use Codex to choose which individual plugins you wanna install.

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Plugin Status](#plugin-status)
- [Development](#development)
- [Repo Structure](#repo-structure)
- [Release Notes](#release-notes)
- [License](#license)

## Overview

### Status

`socket` is active, maintained, and used by Gale daily.

### What This Project Is

TBD

### Motivation

TBD

## Quick Start

Add the `socket` marketplace to Codex with:

```bash
codex plugin marketplace add gaelic-ghost/socket
```

When the marketplace changes, refresh it with:

```bash
codex plugin marketplace upgrade socket
```

After adding or upgrading `socket`, restart your Codex, open the plugin directory, select `Socket`, and then install or enable whichever plugins you want.

## Usage

Use `socket` when you want one Codex catalog for Gale's agent-focused plugin set.

Currently available from the catalog:

- `agent-plugin-skills`
- `apple-dev-skills`
- `cardhop-app`
- `productivity-skills`
- `python-skills`
- `speak-swiftly`
- `swiftasb-skills`
- `things-app`

## Plugin Status

Apple Dev Skills keeps its own roadmap because it is the remaining subtree-managed child with a deeper standalone release surface. Other child planning now lives in [TODO.md](./TODO.md).

Current Socket catalog shape:

- `agent-plugin-skills`: active maintainer skills for skills-export and plugin-export repositories
- `apple-dev-skills`: active Apple, Swift, SwiftUI, Xcode, and DocC workflows with its own roadmap
- `cardhop-app`: active mixed skill plus bundled MCP server for Cardhop.app contact workflows
- `productivity-skills`: active general-purpose maintainer and documentation workflow baseline
- `python-skills`: active Python, `uv`, FastAPI, FastMCP, and pytest workflow plugin
- `speak-swiftly`: active Git-backed Speak Swiftly plugin from the standalone SpeakSwiftlyServer repository
- `swiftasb-skills`: active SwiftASB companion guidance
- `things-app`: active mixed skill plus bundled MCP server for Things.app workflows

Placeholder plugin directories are intentionally visible but not installable until real skill or workflow content exists:

- `dotnet-skills`
- `rust-skills`
- `spotify`
- `web-dev-skills`

## Development

For setup, local workflow, validation, review, release, and maintainer expectations, see [CONTRIBUTING.md](./CONTRIBUTING.md). For the consolidated child backlog, see [TODO.md](./TODO.md). For agent-facing repo rules, see [AGENTS.md](./AGENTS.md).

## Repo Structure

```text
.
├── .agents/plugins/marketplace.json
├── docs/
│   ├── media/
│   └── maintainers/
├── plugins/
├── scripts/
├── AGENTS.md
├── CONTRIBUTING.md
├── README.md
├── TODO.md
└── ROADMAP.md
```

## Release Notes

Use GitHub releases and Git history for root `socket` changes. Child plugins may carry their own release notes and maintainer docs.

## License

The `socket` superproject is licensed under the Apache License 2.0. See [LICENSE](./LICENSE) and [NOTICE](./NOTICE).
