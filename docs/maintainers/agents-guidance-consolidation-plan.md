# Root AGENTS Guidance Consolidation Plan

## Purpose

Consolidate the root [`AGENTS.md`](../../AGENTS.md) into a short routing and
guardrail document. Preserve every Socket-specific safety boundary while moving
procedures, inventories, commands, and domain behavior to their existing owners.

Status: implemented on 2026-08-20.

This audit and implementation record did not change the root marketplace model,
child ownership, release lifecycle, or product architecture policies.

## Audit Baseline

The root file currently contains 152 lines, 2,712 words, and 79 Markdown list
items. It mixes five kinds of guidance:

1. repository scope and task routing;
2. hard safety and authority boundaries;
3. contributor and release procedures;
4. cross-plugin product guidance; and
5. current inventories, commands, and historical context.

The deterministic root guidance and documentation checks both pass:

```text
root guidance audit: PASS
root documentation audit: PASS
```

Those checks establish structural health, not semantic consistency. Manual
comparison found extensive repetition and two concrete drift defects:

- [`CONTRIBUTING.md`](../../CONTRIBUTING.md) still describes
  `plugins/SpeakSwiftlyServer` as a pull-only mirror. The root roadmap,
  [`subtree-workflow.md`](./subtree-workflow.md), and
  [`plugin-packaging-strategy.md`](./plugin-packaging-strategy.md) say that the
  mirror was retired in favor of the Git-backed standalone source.
- `AGENTS.md` describes a similarly named historical deferred-wakeup `-plan.md`,
  but no such file remains. The live owner is
  [`deferred-work-wakeup-policy.md`](./deferred-work-wakeup-policy.md).

## Findings

### The Root File Repeats Maintainer Procedures

The largest duplicate clusters are:

| Root `AGENTS.md` area | Existing detailed owner | Planned treatment |
| --- | --- | --- |
| branch, worktree, push, and direct-`main` rules | global agent guidance, [`CONTRIBUTING.md`](../../CONTRIBUTING.md), and [`subtree-workflow.md`](./subtree-workflow.md) | Keep only the Socket-specific clean-`main` invariant and route implementation work to the workflow owner. |
| subtree sync and branch accounting | [`subtree-workflow.md`](./subtree-workflow.md) and [`release-workflow.md`](./release-workflow.md) | Keep the no-unaccounted-history safety gate; remove the repeated procedure and classifications. |
| deferred remote gates | [`deferred-work-wakeup-policy.md`](./deferred-work-wakeup-policy.md) | Keep one conditional routing rule; remove host-by-host scheduling detail. |
| marketplace shape and Git-backed installation | [`codex-plugin-install-surfaces.md`](./codex-plugin-install-surfaces.md), [`plugin-packaging-strategy.md`](./plugin-packaging-strategy.md), and contributor guidance | Keep the catalog-not-aggregate invariant and route detailed install wording. |
| Swift Package Index submission | [`spi-add-package-automation-plan.md`](./spi-add-package-automation-plan.md) and `scripts/spi_add_package.py` | Keep the hard ban on alternate submission paths plus exact-state language; move the browser choreography and command detail out. |
| setup, Python tooling, validation, and commit format | global agent guidance and [`CONTRIBUTING.md`](../../CONTRIBUTING.md) | Remove duplicated generic policy; retain only conditional Socket validation routing. |
| review readiness and definition of done | [`CONTRIBUTING.md`](../../CONTRIBUTING.md), [`release-workflow.md`](./release-workflow.md), and child guidance | Replace the repeated checklist with task-specific owner links. |

### Domain Guidance Is Too Far Up The Ownership Tree

The SwiftData/SwiftUI, permanent Xcode workspace, native macOS service,
GitHub-owned Linux artifact, and Soto rules are durable, but the root
superproject file is not their closest behavioral owner. The same contracts are
already expressed in Apple and Server-Side Swift skills, child `AGENTS.md`
files, fixtures, or maintainer plans.

Before removing any root copy, verify each contract has all three of these:

1. a current source-owned skill or child-guidance statement;
2. regression coverage or a deterministic validation check where practical;
3. a discoverable routing path from the root when a coordinated pass spans
   multiple plugins.

If one is missing, strengthen the closest owner first. Do not create a generic
root policy document merely to make inventories look symmetrical.

### Information Architecture Is Working Against Selective Reading

The current “Where To Look First” section asks agents to start with several
large documents, including the full roadmap. That increases prompt load before
the task type is known. The replacement should route conditionally:

- root contribution and validation work → `CONTRIBUTING.md`;
- child ownership, marketplace exposure, or sync → `subtree-workflow.md`;
- releases and cleanup → `release-workflow.md`;
- plugin installation state → `codex-plugin-install-surfaces.md`;
- external wait gates → `deferred-work-wakeup-policy.md`;
- SPI submission → `spi-add-package-automation-plan.md` and its script;
- child behavior → the closest child `AGENTS.md` and skill.

The roadmap should be read when planning or status is relevant, not as a
default prerequisite for every edit.

## Target Ownership Model

Use one normative owner for each kind of information:

- root `AGENTS.md`: repository-specific routing, invariants, hard stops, and
  escalation boundaries that must be visible before work begins;
- global agent guidance: Gale-wide communication, Git, tool, and safety defaults;
- `CONTRIBUTING.md`: human-readable contribution workflow, setup, commands,
  validation selection, and review expectations;
- live maintainer references: exact operational procedures and current models;
- child `AGENTS.md`: child repository ownership and local validation boundaries;
- skills and their references: runtime task behavior and domain-specific rules;
- `ROADMAP.md`: current status, planned work, and compact historical conclusions;
- historical plans: evidence only while they still explain an unresolved or
  compatibility-sensitive decision.

A rule may be summarized by a higher-level file only when the summary adds a
necessary routing or safety decision. The summary should link to one detailed
owner instead of restating its steps.

## Proposed Root AGENTS Shape

Target 700–1,100 words and roughly 30–40 list items, a reduction of about
60 percent by word count. Use this outline:

1. **Scope And Routing**
   - define the superproject boundary;
   - distinguish root concerns from child behavior;
   - provide conditional owner links.
2. **Root Invariants**
   - local child payloads are Socket-owned;
   - Apple Dev Skills is canonical under `plugins/` and is not a subtree push
     target;
   - Speak Swiftly is externally owned and Git-backed;
   - the root is a catalog, not an aggregate plugin;
   - authored surfaces are source of truth and installed/cache state is not.
3. **Change Coupling**
   - route ordinary implementation to a named feature branch/worktree;
   - require marketplace, docs, portability records, and validation to move
     together when their shared contract changes;
   - route release and sync work to their live workflows.
4. **Hard Stops And Escalation**
   - preserve the existing `Never Do` and `Ask Before` intent;
   - preserve branch-history accounting before deletion;
   - stop before widening the marketplace or superproject ownership model.
5. **Validation Routing**
   - point to the compatibility baseline and child/full validation selection in
     `CONTRIBUTING.md` without duplicating command catalogs.
6. **Local Overrides**
   - require the closest child `AGENTS.md` for child work.

## Migration Matrix

Apply the consolidation by current root section, not by ad hoc sentence edits:

| Current section | Action |
| --- | --- |
| `Repository Scope` | Retain and compress. Replace the unconditional reading list with task-based routing. |
| `Change Scope` | Retain Socket ownership exceptions; move general Git, worktree, push, continuation, and documentation-update procedures to existing owners. |
| `Child Sync And Branch Accounting Gates` | Retain one hard safety gate and links; move classifications and release sequencing entirely to the release workflow. |
| `Source of Truth` | Keep authored-vs-installed invariants. Route portability to the Hermes and Claude references. Verify domain rules in child owners, then remove their root copies. Move documentation layout, version baselines, terminology, and Python tooling to contributor guidance. |
| `Communication and Escalation` | Retain in shorter form because these rules decide whether root or child authority applies. |
| `Commands` | Remove from `AGENTS.md`; `CONTRIBUTING.md` owns setup and validation commands, and the release/subtree references own their commands. |
| `Review and Delivery` | Remove generic commit style already inherited globally. Keep only Socket-specific completion gates that cannot safely be deferred to a linked procedure. |
| `Safety Boundaries` | Preserve and tighten. Merge overlapping marketplace and subtree prohibitions into distinct hard stops. |
| `Local Overrides` | Retain. |

## Implementation Phases

### Phase 1: Establish One Current Truth

- Correct the stale Speak Swiftly mirror statement in `CONTRIBUTING.md`.
- Remove the nonexistent deferred-policy-plan reference.
- Confirm every root link and named file exists.
- Classify active versus historical maintainer plans before using any plan as a
  durable owner.

### Phase 2: Prove Domain Ownership

- Build a behavior-preservation checklist for every root-only or cross-plugin
  rule.
- Confirm SwiftData/SwiftUI ownership in Apple skills and all intentional
  handoff surfaces.
- Confirm workspace, native-local-service, GitHub cloud-artifact, and Soto
  ownership in the Apple and Server-Side Swift children.
- Confirm documentation-source routing and POSIX symlink rules in their owning
  skills or contributor references.
- Add or strengthen focused regression checks before deleting a root statement
  that is the only enforceable copy.

### Phase 3: Rewrite Root AGENTS

- Replace the file as one coherent pass using the proposed outline.
- Preserve hard negatives and ask-before boundaries in direct language.
- Replace repeated procedures with conditional links to live owners.
- Avoid links to historical plans unless a current compatibility decision still
  depends on their evidence.

### Phase 4: Deduplicate Adjacent Root Docs

- Remove repeated agent-only rules from `CONTRIBUTING.md` after the root rewrite.
- Keep contributor-facing explanations where they help a human execute the
  workflow; link to maintainer procedures instead of restating them.
- Reconcile `subtree-workflow.md`, `plugin-packaging-strategy.md`, and the
  roadmap around the single current Speak Swiftly model.
- Collapse any newly obsolete plan conclusions into a live reference or roadmap
  history before deleting a maintainer plan.

### Phase 5: Validate Behavior And Prompt Load

Run validation serially:

```bash
just repo-validate
```

Also perform a manual scenario review for:

1. ordinary root documentation work;
2. an edit inside a monorepo-owned child;
3. Apple Dev Skills work with no subtree push;
4. Speak Swiftly work in the standalone checkout;
5. a marketplace packaging move;
6. a release with an unmerged local branch;
7. a pending remote CI gate;
8. an SPI submission request; and
9. a coordinated cross-plugin domain-policy change.

Each scenario must still route to the correct owner, preserve required
authority checks, and name the relevant validation surface.

## Acceptance Criteria

- Root `AGENTS.md` is no more than 1,100 words unless a measured safety gap
  justifies the excess.
- Every removed rule is recorded as inherited globally, moved to one named
  owner, enforced by a source-owned skill/test, or intentionally retired.
- No operational procedure has more than one full normative copy in root docs.
- Hard stops remain directly visible in `AGENTS.md`; they are not hidden only
  behind links.
- Conditional reading replaces the unconditional root-doc reading list.
- The Speak Swiftly source model and deferred-wakeup references are consistent
  across all live root docs.
- Root guidance/documentation audits and the compatibility profile pass.
- The final review reports word-count reduction and the behavior-preservation
  checklist, not just a clean diff.

## Implementation Evidence

The completed root [`AGENTS.md`](../../AGENTS.md) is 880 words and 114 lines,
down from 2,712 words and 152 lines. That is a 68 percent word-count reduction
and is within the planned 700–1,100-word bound.

The behavior-preservation review produced these results:

| Scenario | Preserved route or guard |
| --- | --- |
| ordinary root documentation work | `CONTRIBUTING.md` owns contribution, validation, and review procedure; root guidance retains change-coupling and truthful-delivery requirements. |
| monorepo-owned child edit | root guidance directs the edit to `plugins/<child>`, then requires the closest child `AGENTS.md` and task-owning skill. |
| Apple Dev Skills change | root guidance directly identifies `plugins/apple-dev-skills` as canonical and forbids a compatibility-repo subtree push. |
| Speak Swiftly change | root guidance and contributor workflow direct payload work to the standalone repository and state that no local mirror exists. |
| marketplace packaging move | root guidance requires marketplace, install surface, maintainer references, and validation to move together. |
| release with unmerged history | branch/history deletion remains directly blocked until explicit accounting; the detailed lifecycle routes to `release-workflow.md`. |
| pending external gate | terminal waits and polling loops remain directly prohibited; host procedure routes to the live deferred-wakeup policy. |
| SPI submission | alternate GitHub issue, label, fork, clone, file-edit, and pull-request paths remain directly prohibited; exact procedure routes to the script and live plan. |
| coordinated domain-policy change | root guidance requires a bounded cross-child explanation, closest child owners, compatibility outcomes, and escalation before widening architecture or ownership. |

Domain-policy ownership was confirmed before removing root copies:

- SwiftData/SwiftUI behavior is owned by Apple Dev Skills' `swiftdata-workflow`
  and SwiftUI architecture surfaces, with intentional handoffs in affected
  Swift child skills.
- permanent workspace behavior is owned by Apple Dev Skills'
  `bootstrap-xcode-workspace` workflow and its managed guidance.
- native local services and Soto ownership are explicit in
  `plugins/server-side-swift/AGENTS.md` and their task-owning skills.
- GitHub-owned Linux artifact behavior is enforced by Server-Side Swift and
  root deployment-safety contract tests.
- POSIX discovery mirrors are owned by Agent Portability Skills' symlink policy.
- documentation-source routing remains inherited from Gale's global guidance
  and refined by source-specific child skills.

Focused tests in [`tests/test_root_agents_guidance.py`](../../tests/test_root_agents_guidance.py)
now guard the word budget, live-owner routes, directly visible hard stops,
absence of reintroduced domain/command detail, and the retired Speak Swiftly
mirror model.

Final validation passed with the root guidance and documentation audits, all
140 root tests, Mypy, Ruff, root marketplace and shared-skill metadata checks,
and the Hermes and Claude compatibility validators.

## Suggested Change Slices

1. `docs: reconcile root guidance sources`
   - fix known semantic drift and establish current owners.
2. `docs: consolidate root agent guidance`
   - rewrite `AGENTS.md` and update directly affected live references.
3. `tests: guard root guidance ownership`
   - add focused deterministic checks only where manual drift caused the current
     duplication or contradiction.

The implementation remained one reviewable documentation-and-contract-test
change on a feature branch. Gale separately authorized its local merge; no
push, pull request, tag, release, or publication belongs to this work.
