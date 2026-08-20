# Agent Skills Domain Split Plan

## Decision

Replace the broad `productivity-skills` catch-all with focused child plugins.
The target structure separates repository operations, documentation maintenance,
professional workflows, and agent-system engineering. It does not create a
second generic portability layer and does not move language-specific agent
implementation out of the language plugins that own it.

This is a durable building-block change. It gives every skill one clear owner
and makes the coordinator-and-worker protocol available at the moment an agent
starts, schedules, resumes, or supervises work.

## Why The Current Boundary Is Not Sustainable

`productivity-skills` currently mixes unrelated work:

- repository and GitHub maintenance;
- documentation maintenance across README, contributor, agent, API,
  accessibility, architecture, and roadmap files;
- Codex GUI worktree guidance;
- agent automation, agent evaluation, and n8n planning;
- job-search guidance; and
- source-bundled read-only custom-agent roles.

Those jobs do not share one user, runtime, artifact, or implementation
boundary. Keeping them together makes discovery vague and encourages new work
to be added because it is generally useful rather than because the plugin owns
it. Do not retain a catch-all plugin merely to preserve its existing name.

## Target Plugin Boundaries

| Plugin | Owns | Does not own |
| --- | --- | --- |
| `repository-skills` | repository operations, GitHub settings, worktree/branch ownership, validation and release handoffs | document content, generic agent coordination, language implementation |
| `documentation-skills` | README, CONTRIBUTING, AGENTS, API, accessibility, architecture, roadmap, and cross-document maintenance | repository release operations or agent-system runtime design |
| `professional-skills` | career, job-search, and other explicitly professional workflow guidance | repository maintenance, generic personal-task management, or agent-system design |
| `agent-engineering-skills` | designing, building, operating, coordinating, scheduling, and evaluating local or hosted agent systems | host packaging portability or language-specific implementation details |
| `agent-portability-skills` | host adapters and compatibility decisions for skills, plugins, MCP, hooks, apps, and custom-agent surfaces | the universal coordinator/worker operating contract |
| language and stack plugins | implementation of an approved agent service in their language/runtime | the cross-runtime architecture decision that precedes implementation |

`model-lab-skills` remains model-focused. A model is an input to an agent
system, not the owner of that system's scheduling, state, task, or handoff
model.

## Agent Engineering Skills

Create `agent-engineering-skills` as the real home for agent systems. It must
cover both the current host's workers and independently operated external
agents.

Initial skills:

1. `design-agent-system`
   - choose local, hosted, hybrid, single-agent, coordinator/worker, service,
     queue, or no-agent shape;
   - define state, permissions, tool boundaries, observability, approval, and
     escalation requirements; and
   - hand implementation to the owning language/runtime plugin.
2. `orchestrate-agent-work`
   - apply the coordinator/worker launch and report-back contract before
     delegating, creating a worker task or thread, or resuming delegated work.
3. `coordinate-external-agents`
   - coordinate independently operated agents through durable task records,
     artifacts, branches, worktrees, pull requests, or another explicit shared
     surface; never assume direct cross-thread messaging exists.
4. `schedule-agent-work`
   - choose one-shot, recurring, event-triggered, monitored, CI, background,
     queue, or board-based work and define the result-delivery route back to
     Gale and the coordinator.
5. `coordinate-worktrees-and-threads`
   - assign worker/task identity, worktree, branch, write scope, validation
     lane, merge/handoff target, and retention or cleanup decision at launch.
6. `evaluate-agent-systems`
   - evaluate the system and its operating protocol: reports, permissions,
     ownership, retries, blocked states, handoffs, and usable final evidence.

The first release is guidance and contracts, not a new queue, scheduler,
service, generic runtime wrapper, or portable host bridge.

## Universal Orchestration Contract

The orchestration skills define a host-neutral protocol. Host-specific skills
may translate it, but cannot weaken it.

### Coordinator Duties

- Own the user goal, decomposition, authority, dependencies, final synthesis,
  validation decision, and closure.
- Launch each worker with a structured envelope before it begins work.
- State whether the coordinator waits for all results, processes partial
  results, or uses a durable handoff for later continuation.
- Track every worker until it is completed, blocked, cancelled, failed, or
  deliberately retained for follow-up.
- Acknowledge each returned result by consuming it, requesting one bounded
  follow-up, marking it superseded, or cancelling it explicitly.
- Keep user-facing decisions, cross-worker conflict resolution, final edits,
  merge, publication, and final verification with the coordinator unless an
  explicitly approved disjoint ownership plan says otherwise.

### Worker Launch Envelope

Every worker task must state:

- task and coordinator identity;
- objective and bounded scope;
- relevant inputs and source-of-truth locations;
- allowed and forbidden actions, including write authority;
- worktree, branch, artifact, or shared-task surface when applicable;
- acceptance criteria and validation owner;
- expected report format and return route; and
- escalation, cancellation, and completion conditions.

### Worker Report-Back Rule

Every worker must return to its coordinator through the host's supported
result or handoff channel. It must end with exactly one terminal state:
`completed`, `blocked`, `needs-decision`, `cancelled`, or `failed`.

The final report includes the outcome, evidence or artifacts, validation
performed or intentionally not performed, unresolved uncertainty, and one
recommended next action. It must not silently stop, assume that a coordinator
noticed an artifact, or make a scope/authority decision on the coordinator's
behalf.

### Escalation And Parallel Work

Workers stop and report rather than improvising when scope expands, ownership
conflicts, authority is missing, evidence contradicts itself, an external or
destructive action is required, or acceptance criteria become ambiguous.

Parallel writes require explicit disjoint files or directories, branch and
worktree ownership, Git-operation sequencing, validation responsibility, and
integration order. Do not allow workers to share a Git mutation or heavy build
lane without an approved serialized owner.

Default to one delegation layer. Nested orchestration requires a concrete
reason, an explicit depth and fan-out limit, and host support.

## External Agents And Durable Work

An external agent is an independently operated worker, not an in-run subagent.
It requires a durable, discoverable handoff surface before dispatch. Valid
surfaces include a task-board record, issue, pull request, shared document,
branch/worktree, artifact directory, or another host-native record with clear
access and retention behavior.

The record must include the same launch envelope, status, final report, and
return route. Starting an external worker is not progress unless the
coordinator can later discover its status and consume its result.

For work that must survive session closure, restarts, human decisions, or
multiple independent agent roles, choose a durable queue, board, scheduled
task, CI workflow, or service. Do not pretend a transient child-agent run has
those properties.

## Migration Map

| Current surface | Target owner | Migration note |
| --- | --- | --- |
| `maintain-project-repo` | `repository-skills` | Keep release choreography, setup, validation, and branch-accounting boundaries. |
| `maintain-github-repository` | `repository-skills` | Keep remote settings separate from local Git operations. |
| `codex-gui-worktree-workflow` | split | Move repository mechanics to `repository-skills`; make coordinator requirements defer to `agent-engineering-skills`. |
| `maintain-project-docs`, README, CONTRIBUTING, AGENTS, API, accessibility, architecture, and roadmap skills | `documentation-skills` | Preserve one skill per document responsibility and existing owner-file boundaries. |
| `repo-docs-auditor` | `documentation-skills` | Keep it read-only and report-first. |
| `design-agent-automation-workflow` | `agent-engineering-skills` | Expand from framework selection into the first system-design entry point. |
| `design-agent-eval-workflow` | `agent-engineering-skills` | Keep evaluation separate from runtime implementation. |
| `design-n8n-agent-workflow` | `agent-engineering-skills` | Treat n8n as one external automation/runtime adapter, not the general owner. |
| `code-slice-tracer` and `explain-code-slice` | decide during migration | Keep together; choose `documentation-skills` only if their durable purpose remains explanation artifacts, otherwise create a narrow codebase-understanding owner. |
| `dice-job-search-workflow` | `professional-skills` | Keep job-search privacy and external-service boundaries intact. |
| `build-python-agent-service`, FastMCP/FastAPI, .NET/JVM agent-service skills | stay in language plugins | Add a first-step handoff to Agent Engineering Skills when architecture remains undecided. |
| host-compatibility and adapter guidance | `agent-portability-skills` | Keep host translations thin; do not duplicate the universal contract. |

## Implementation Slices

1. **Define and validate the new plugin boundaries.**
   - Inventory every `productivity-skills` file, custom agent, test, manifest,
     docs reference, root marketplace entry, and generated/discovery surface.
   - Decide the final destination of `explain-code-slice` and
     `code-slice-tracer` before moving files.
   - Do not create empty plugins merely to reserve names.
2. **Ship `agent-engineering-skills` first.**
   - Add the universal orchestration contract, external-agent and scheduling
     guidance, and the initial design/evaluation workflows.
   - Update existing custom-agent role templates to require the terminal
     report-back rule.
   - Add host adapters that describe Codex, ChatGPT Work, and Hermes mechanics
     without claiming unsupported generic cross-thread messaging.
3. **Extract repository and documentation ownership.**
   - Move authored skills, role definitions, tests, documentation, manifests,
     marketplace metadata, and references together in focused passes.
   - Preserve current document-type separation; do not collapse documentation
     skills into one oversized apply workflow.
4. **Create `professional-skills` and retire the catch-all.**
   - Move career/job-search guidance first.
   - Classify any remaining Productivity surfaces by a real owner or delete
     them only after their content is preserved elsewhere.
   - Remove `productivity-skills` from the marketplace only after all owned
     content, roles, validations, and install/update references have moved.
5. **Release and verify.**
   - Update root README, CONTRIBUTING, ROADMAP, marketplace metadata, host
     compatibility records, custom-agent inventories, tests, and discovery
     exports in the same release sequence.
   - Test isolated marketplace installs for every new and renamed plugin.
   - Account for subtree implications and all non-main branches before cleanup.

## Migration Mechanics

Treat this as a move-and-adapt migration, not a rewrite. Preserve authored
skills, references, scripts, tests, custom-agent definitions, manifests, and
documentation whenever their responsibility is unchanged.

- Use a normal filesystem or editor move for files and directories when the
  target owner changes; verify the resulting diff preserves the intended
  rename/move rather than treating Git staging syntax as the migration method.
- Use focused patches to update names, links, ownership wording, imports,
  manifests, tests, and validation paths after each move.
- Keep a file-by-file migration map before moving a plugin surface so no skill,
  role, reference, script, test, asset, or packaging entry is silently dropped.
- Compare each moved surface against its pre-move content. A move should produce
  a small, reviewable diff; unrelated rewrites need their own explicit reason
  and review scope.
- Preserve behavior and validation first. Improve wording, structure, or
  implementation only where the new owner boundary actually requires it or a
  separately approved cleanup is already in scope.
- Do not recreate files from memory or copy large replacement blocks when a
  move plus narrow patch preserves the source of truth.
- Run targeted validation after each migration slice and inspect the rename,
  deletion, and modification summary before moving to the next slice.

## Non-Goals

- Do not add a generic runtime wrapper, queue, scheduler, or host bridge merely
  because the new plugin discusses them.
- Do not move Python, .NET, JVM, or other language-specific implementation
  details into Agent Engineering Skills.
- Do not treat ChatGPT Work, Codex, Hermes, or any future agent host as having
  identical thread, task, scheduling, or direct-message capabilities.
- Do not retain a new catch-all under another name.

## Exit Criteria

- Each migrated skill, custom agent, test, manifest, marketplace entry, and
  documentation reference has one explicit owner.
- `productivity-skills` is retired rather than left as an ambiguous residual
  plugin.
- Agent Engineering Skills enforces the launch-envelope and terminal
  report-back contract for in-run and external-agent coordination.
- Repository and documentation skills retain their present narrow boundaries.
- Runtime and host adapters use the shared contract without claiming feature
  parity or generic direct cross-thread communication.
- Isolated install and validation evidence covers all newly created or renamed
  plugins before release.
