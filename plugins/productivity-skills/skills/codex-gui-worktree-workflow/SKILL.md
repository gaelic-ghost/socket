---
name: codex-gui-worktree-workflow
description: Plan and align Codex GUI worktree-first workflows, local environments, actions, permanent worktrees, and handoffs to Git or Worktrunk worktrees. Use when a repo should make Codex app Worktree mode easier to use without mixing stack-specific commands into general guidance.
---

# Codex GUI Worktree Workflow

## Purpose

Make Codex GUI worktree-first development easier to use by choosing the right worktree mode, local environment shape, action set, and stack-specific handoff.

This is a general productivity workflow. It owns the Codex app workflow decision and repo-facing guidance shape. It does not own SwiftPM, Xcode, Vapor, Hummingbird, JavaScript, Python, Rust, or other stack-specific build commands; use the relevant stack plugin for those templates and validation details.

## When To Use

- Use this skill when a repository should prefer Codex GUI Worktree mode for Codex-started tasks.
- Use this skill when the user wants Codex local environments, setup scripts, and app action buttons planned or aligned.
- Use this skill when choosing between Codex GUI managed worktrees, permanent Codex worktrees, plain Git worktrees, and Worktrunk-managed worktrees.
- Use this skill when repo guidance should explain how Codex GUI worktrees differ from terminal-created worktrees.
- Do not use this skill to implement stack-specific build, test, run, or simulator commands. Hand those to the owning stack plugin.
- Do not use this skill to build a Worktrunk bridge. Treat that as a separate integration project.

## Workflow

1. Refresh current Codex docs before making product-behavior claims:
   - Codex app worktrees
   - Codex local environments
   - Codex app features
   - Codex sandboxing and auto-review
2. Inspect the target repo shape:
   - Git repository state and worktree list
   - whether the intended base or feature branch is already checked out in another live worktree
   - existing `.codex/environments/*.toml`
   - repo `AGENTS.md`
   - existing validation or maintainer scripts
   - stack markers such as `Package.swift`, `.xcodeproj`, `pyproject.toml`, `package.json`, `Cargo.toml`, or service framework files
3. Choose the worktree strategy:
   - Codex GUI Worktree mode for Codex-started isolated tasks
   - permanent Codex worktree for long-lived branches that should stay visible as app projects
   - plain Git or Worktrunk-managed worktree for terminal-first branch management
   - path-specific new Codex thread or app project when a terminal-created worktree should become a GUI workspace
   - when starting a Codex thread from a named existing branch, verify the branch ref exists first; for new branch work, create the branch first or start from the current working tree and have the worker create or switch to the branch
4. Shape general repo guidance:
   - explain that Codex GUI worktrees are Git worktrees plus app-owned thread association, handoff, snapshots, cleanup, review pane state, local environment setup, and action buttons
   - explain that terminal-created Git or Worktrunk worktrees are not automatically Codex-managed app worktrees
   - warn that keeping the same branch checked out in two live worktrees can leave one checkout's index and files stale after commits land elsewhere
   - state that auto-review reviews approval requests without expanding writable roots or sandbox permissions
   - keep `.codex/environments/*.toml` portable and repo-owned
5. Delegate stack-specific commands:
   - Apple SwiftPM or Xcode commands: use `apple-dev-skills`
   - server-side Swift commands: use `server-side-swift`
   - Python commands: use `python-skills`
   - Rust commands: use `rust-skills`
   - .NET commands: use `dotnet-skills`
   - JavaScript or TypeScript commands: use the repo's owning web or Node workflow
6. If the user asks for implementation, create or update only the general guidance and general local environment structure here; apply stack-specific templates from the owning plugin.

## Output Contract

Return a concise plan or implementation summary with:

- `Worktree Mode`: local, Codex GUI worktree, permanent Codex worktree, Git worktree, or Worktrunk-managed worktree
- `Local Environment`: setup script and action button plan
- `Stack Handoff`: owning plugin or repo script for stack-specific commands
- `Sandbox Notes`: approval and writable-root implications
- `Files`: `.codex/environments`, `AGENTS.md`, or docs touched or proposed
- `Validation`: commands run or intentionally skipped

## Guardrails

- Do not claim Codex can control where Codex-managed worktrees are created if current docs say it cannot.
- Do not treat shell `cwd` changes as moving an existing Codex GUI project.
- Do not ask Codex to create a managed worktree from a branch name that has not been created yet.
- Do not intentionally keep the same branch checked out in multiple active worktrees except as a short-lived recovery step; if it happens, verify both checkout statuses before handoff or cleanup.
- Do not commit machine-local absolute paths, private checkout paths, user-specific DerivedData locations, secrets, local package paths, or local dependency paths.
- Do not make global `danger-full-access` or broad writable-root changes as a convenience fix for noisy approvals.
- Do not imply auto-review expands the sandbox boundary.
- Do not put stack-specific command templates in this productivity skill when an owning stack plugin exists.

## References

- `references/codex-gui-worktree-guidance.md`
