# Codex GUI Worktree Guidance

Use this reference when a repo wants Codex GUI worktree-first development as the default collaboration shape.

## Worktree Surfaces

- Codex GUI Worktree mode is best for Codex-started isolated work because the app owns thread association, handoff, snapshots, cleanup, review pane state, setup scripts, and action buttons.
- Permanent Codex worktrees are best for long-lived branches that should stay visible as app projects.
- Plain Git worktrees and Worktrunk-managed worktrees are best for terminal-first branch management. Open those paths as their own Codex app project or path-specific new thread when the GUI should work there.
- Worktrunk bridge work belongs to a separate integration project, not to ordinary repo guidance.

## Local Environment Shape

Local environment files should live under `.codex/environments/` in the target repo when they are meant to be shared. Keep them portable:

- no machine-local absolute paths
- no private checkout paths
- no local dependency paths
- no user-specific DerivedData locations
- no secrets

Use setup scripts for worktree initialization and actions for common commands the user should run from the Codex app top bar.

## Stack Handoffs

General workflow guidance belongs here. Stack commands belong elsewhere:

- Apple SwiftPM and Xcode templates: `apple-dev-skills`
- server-side Swift service templates: `server-side-swift`
- Python commands: `python-skills`
- Rust commands: `rust-skills`
- .NET commands: `dotnet-skills`
- JavaScript or TypeScript commands: the repo's owning web or Node workflow

## Sandbox And Auto-Review

Auto-review changes who reviews approval requests. It does not expand writable roots, allow protected paths, or make arbitrary Git metadata writable.

If worktree workflows create too many mundane reviews, fix the boundary or command shape first:

- keep build output inside the worktree when the stack supports it
- use repo-owned scripts for repeatable commands
- use narrow command prefix rules only for commands the user actually trusts
- avoid broad full-access defaults

## Official References

- [OpenAI Codex app worktrees](https://developers.openai.com/codex/app/worktrees)
- [OpenAI Codex local environments](https://developers.openai.com/codex/app/local-environments)
- [OpenAI Codex app features](https://developers.openai.com/codex/app/features)
- [OpenAI Codex sandboxing](https://developers.openai.com/codex/concepts/sandboxing)
- [OpenAI Codex auto-review](https://developers.openai.com/codex/concepts/sandboxing/auto-review)
