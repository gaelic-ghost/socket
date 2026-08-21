# AGENTS.md

Use this file for durable Socket-specific rules. Keep procedures in contributor
or maintainer documentation and implementation details in the owning child.

## Repository Scope

### What This File Covers

Socket is the root marketplace and coordination repository for the plugin
payloads under `plugins/`. The root owns marketplace metadata, shared exports,
root documentation, and cross-plugin policy.

### Where To Look First

- Use `CONTRIBUTING.md` for setup, validation, and contribution workflow.
- Use `ROADMAP.md` for current plans and recorded decisions.
- Use `docs/maintainers/` for release, subtree, compatibility, and installation
  procedures.
- For child work, read the closest child `AGENTS.md` and task-owning skill.

## Working Rules

### Change Scope

- Keep root changes limited to one coherent cross-repository concern.
- Edit monorepo-owned payloads directly under `plugins/`.
- Work on Speak Swiftly in its standalone repository; Socket only references it.
- Surface any change that would widen root ownership or alter the marketplace
  model before implementing it.

### Source of Truth

- Authored child `skills/`, `mcps/`, `apps/`, and equivalent surfaces are source.
- Plugin manifests and marketplace files are packaging metadata.
- Installed plugins, caches, enabled-state configuration, and consumer copies
  are runtime state, not editable source.
- When documentation and automation disagree, correct the owning source rather
  than preserving duplicate behavior.

### Communication and Escalation

State the concrete ownership, compatibility, or release consequence of a change.
Ask before introducing a new packaging layer, subtree-managed child, or
cross-repository policy.

## Commands

### Setup

```bash
just --list
```

### Validation

```bash
just repo-validate
just test
```

Socket intentionally has one root integration/E2E test and no nested or unit
test suites. `CONTRIBUTING.md` owns release routing.

### Optional Project Commands

Use the focused child commands documented by the owning child repository.

## Review and Delivery

### Review Expectations

- Report exactly which surfaces changed and which checks ran.
- Update nearby root docs and marketplace metadata when their owned behavior
  changes.
- Verify child ownership and remote reachability before claiming synchronization
  or safe cleanup.

### Definition of Done

The requested behavior and documentation agree, relevant focused checks pass,
and no unrelated working-tree changes were modified.

## Safety Boundaries

### Never Do

- Do not import non-Git directories as subtrees or rewrite subtree history.
- Do not invent an aggregate root plugin around already packaged children.
- Do not assume every child exposes its manifest at the child root.
- Do not delete branches, worktrees, refs, or child directories until their
  unmerged history is accounted for.
- Do not use alternate submission paths for Swift Package Index work.

### Ask Before

- Adding or restoring a subtree-managed child.
- Changing repository ownership, visibility, packaging, or release architecture.
- Deleting a maintainer document whose durable conclusions have not moved to a
  live owner.

## Local Overrides

Nested `AGENTS.md` files under `plugins/` refine this file for their directories.
Closer guidance takes precedence for child-specific work.
