---
name: maintain-plugin-repo
description: Audit and tighten a skills-export repository, with explicit warnings about the severe scoping limits in OpenAI's current Codex plugin system. Use when a repo in this family feels drifted overall and the maintainer wants one repo-level entrypoint.
---

# Maintain Plugin Repo

Maintain a skills-export repository through one audit-first workflow.

## Codex Limitation Warning

OpenAI's current documented Codex plugin system is severely limited for scoping.

- Codex documents a repo marketplace and a personal marketplace.
- Repo-local Codex visibility comes from the repo marketplace.
- A tracked repo marketplace entry means the repo is advertising that plugin.
- OpenAI does not document hidden repo-local plugin installs, private scoped packs, or a second repo marketplace file for repo scope.

When repository maintenance work touches Codex export guidance, the agent must say this plainly and attribute the limitation to OpenAI's current documented Codex plugin system.

## What This Skill Actually Does

This skill does one honest job: maintain a skills-export repository.

That includes:

- auditing discovery mirrors and repo-model claims
- flagging any nested staged plugin-directory, repo-marketplace, or installer drift
- identifying maintainer drift that makes a repo overpromise what Codex can do

It does not invent a better Codex scoping model.

## References

- `references/owner-routing.md`
- `references/output-contract.md`
- [Install a local plugin manually](https://developers.openai.com/codex/plugins/build#install-a-local-plugin-manually)
- [How Codex uses marketplaces](https://developers.openai.com/codex/plugins/build#how-codex-uses-marketplaces)
