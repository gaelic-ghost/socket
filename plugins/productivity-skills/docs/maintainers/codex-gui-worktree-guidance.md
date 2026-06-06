# Codex GUI Worktree Guidance

Use this maintainer note when updating `productivity-skills:codex-gui-worktree-workflow`.

This workflow owns general Codex app worktree-first planning: which worktree surface to use, how to talk about Codex local environments, and where stack-specific setup or action commands should be delegated.

## Ownership Boundary

- `productivity-skills` owns general Codex GUI workflow choice and repo guidance shape.
- `apple-dev-skills` owns SwiftPM and Xcode local environment templates.
- `server-side-swift` owns Vapor, Hummingbird, and server-side Swift local environment templates.
- Other stack plugins own their stack-specific build, test, run, and setup actions.
- Worktrunk bridge implementation belongs to its own integration work, not this workflow skill.

## Required Claims

Refresh official Codex docs before changing product-behavior wording. Keep these claims aligned with current docs:

- Codex GUI Worktree mode uses Git worktrees plus app-managed thread association, handoff, snapshots, cleanup, review pane state, local environment setup, and actions.
- Permanent Codex worktrees are the app-visible long-lived branch option.
- Plain Git and Worktrunk-managed worktrees are terminal-first unless opened as their own Codex app project or path-specific thread.
- Local environment files should be portable and repo-owned.
- Auto-review reviews approval requests but does not expand the sandbox boundary.

## Official References

- [OpenAI Codex app worktrees](https://developers.openai.com/codex/app/worktrees)
- [OpenAI Codex local environments](https://developers.openai.com/codex/app/local-environments)
- [OpenAI Codex app features](https://developers.openai.com/codex/app/features)
- [OpenAI Codex sandboxing](https://developers.openai.com/codex/concepts/sandboxing)
- [OpenAI Codex auto-review](https://developers.openai.com/codex/concepts/sandboxing/auto-review)
