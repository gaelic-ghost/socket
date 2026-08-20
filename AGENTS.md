# AGENTS.md

Use this file for Socket-specific routing, invariants, and hard stops. Use the
linked contributor and maintainer documents for procedures and commands.

## Scope And Routing

- `socket` is Gale's local Codex plugin and skills superproject. It owns the
  child payloads under [`plugins/`](./plugins/), the root marketplace at
  [`.agents/plugins/marketplace.json`](./.agents/plugins/marketplace.json), and
  root coordination documentation.
- Treat this repository as a stopgap around Codex's documented marketplace
  scoping. Do not present it as evidence of a richer shared-parent or
  repo-private plugin model.
- For root contribution, setup, validation, and review workflow, use
  [`CONTRIBUTING.md`](./CONTRIBUTING.md).
- For child ownership, marketplace exposure, or synchronization, use
  [`subtree-workflow.md`](./docs/maintainers/subtree-workflow.md). For releases,
  branch accounting, and cleanup, use
  [`release-workflow.md`](./docs/maintainers/release-workflow.md).
- For plugin source, cache, and enabled-state questions, use
  [`codex-plugin-install-surfaces.md`](./docs/maintainers/codex-plugin-install-surfaces.md).
  For pending external gates, use
  [`deferred-work-wakeup-policy.md`](./docs/maintainers/deferred-work-wakeup-policy.md).
- For Swift Package Index work, use
  [`spi-add-package-automation-plan.md`](./docs/maintainers/spi-add-package-automation-plan.md)
  and `scripts/spi_add_package.py`.
- When work concerns one child repository's behavior, packaging, or validation,
  read that child's `AGENTS.md` and task-owning skill before broader root docs.
  Read [`ROADMAP.md`](./ROADMAP.md) when planning or status is relevant, not as
  a prerequisite for every edit.

## Root Invariants

- Treat Gale's local `socket` checkout on `main` as the clean coordination and release-verification checkout. Use a named feature branch/worktree for implementation unless Gale explicitly authorizes direct-`main` work or a repo-owned release helper owns the operation.
- Edit ordinary monorepo-owned child payloads directly under `plugins/` and
  commit them in `socket`.
- `plugins/apple-dev-skills` is the canonical Apple Dev Skills payload. The
  standalone repository is a compatibility marketplace pointer; do not
  subtree-push Socket payload changes to it.
- Speak Swiftly is owned by the standalone `SpeakSwiftlyServer` repository and
  reaches Socket through a Git-backed marketplace entry. Socket has no local
  `plugins/SpeakSwiftlyServer` mirror.
- The Socket root is a marketplace catalog, not an aggregate plugin. Point each
  marketplace entry at the real packaged plugin root or canonical Git-backed
  source.
- Treat authored `skills/`, `mcps/`, `apps/`, and equivalent top-level child
  surfaces as source of truth. Plugin manifests and marketplace files are
  packaging metadata. Managed installs, caches, enabled-state configuration,
  and consumer-side copies are runtime state, not editable source.
- Every new or materially changed plugin, skill, or MCP declaration needs an
  explicit Codex, Hermes, and Claude compatibility outcome in the same pass.
  Follow the compatibility commands and ownership rules in
  [`CONTRIBUTING.md`](./CONTRIBUTING.md).
- When shipped behavior, active inventory, packaging roots, or validation
  commands change, update their owning docs and the roadmap in the same pass.
  When docs and scripts disagree, fix the script or narrow the documented
  contract.

## Change Coupling

- Keep root changes bounded to one coherent concern. Put detailed child
  behavior in its owning child and keep the root explanation limited to the
  cross-child policy or discovery reason.
- When child packaging is added, removed, moved, or renamed, update the root
  marketplace, user-facing install surface, and relevant maintainer references
  together, then run the validation selected by `CONTRIBUTING.md`.
- Root docs and marketplace wiring are updated together when packaging or policy changed.
- Treat child synchronization and branch accounting as completion gates. Do
  not claim work is merged, preserved, synchronized, or safe to clean up until
  reachability and ownership are verified in the exact repository and remote.
- Route every release through the single branch-backed release lifecycle.
  Child synchronization is a conditional gate inside that lifecycle, not a
  direct-`main` exception or separate release mode.
- At a remote CI, review, release, deployment, or provider gate that will not
  resolve in the current command, follow the live deferred-wakeup policy. Do
  not hold a terminal open or create a polling loop.
- For SPI submission, use only the official Add Package issue-form path through
  the repository script. Never substitute `gh issue create`, manual labels, a
  PackageList fork or clone, `packages.json` edits, or a PackageList pull
  request. Report only the exact verified states `SPI-ready locally`,
  `SPI Add Package issue submitted`, or `indexed on SPI`.

## Hard Stops And Escalation

- Do not import non-Git directories as subtrees, rewrite subtree history to look
  monorepo-native, re-vendor an existing child plugin inside another child, or
  invent a second root packaging layer around an already packaged plugin.
- Do not assume every child surface exposes `.codex-plugin/plugin.json` at its directory root. Inspect the child's actual installable surface.
- Do not delete a branch, worktree, remote branch, archive ref, rescue ref, or
  child directory until all unmerged history is explicitly accounted for and
  preserved where required.
- Ask before adding or reintroducing a subtree-managed child repository.
- Ask before broadening Socket into a stronger bundle or packaging abstraction,
  widening root ownership, or changing the root marketplace model.
- Ask before deleting a root maintainer document unless its durable conclusions
  have already moved to `ROADMAP.md` or a live owner reference.
- Stop and surface the widening when a bounded root concern becomes a cross-repo
  policy or architecture change.

## Validation Routing

- Use the focused child validation for child behavior and the root profile that
  matches the changed surface. `CONTRIBUTING.md` owns the current commands and
  the distinction between compatibility, full, and release validation.
- Before delivery, verify affected links and rendered Markdown plus any required
  marketplace, portability, child-sync, and branch-accounting outcomes. Do not
  imply that a build, test, sync, merge, release, or publication occurred when
  it did not.

## Local Overrides

- Nested `AGENTS.md` files under `plugins/` refine this guidance for their own
  repository shape, domain rules, validation, and packaging boundaries.
