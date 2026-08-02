# Deferred Work Wakeup Policy: Audit and Implementation Plan

## Status

Planned. This document is an audit and implementation plan only; it does not
change any released skill, release script, CI workflow, or deployment adapter.

## Decision

When an agent has started a remote or externally-owned operation that will not
produce a useful result promptly, it must stop actively waiting and schedule a
future continuation using the current host's approved scheduler. It must not
keep a terminal, polling loop, or status-watch command open merely to wait for
CI, a review bot, a hosted build, a release publication, deployment readiness,
or a remote worker.

This is a durable cross-host policy, not a new generic runtime abstraction.
It removes the current split where a release script can describe a Codex
heartbeat while the surrounding portable skills still imply that an agent may
watch the remote state directly. The simpler extension considered first was to
clarify the existing Codex-only wording in `maintain-project-repo`; that would
leave deployment, CI, and Hermes users with incompatible behavior.

### Boundary

The rule applies to an *agent waiting for an external process or service*.
It does not replace:

- a program's own synchronization primitive, protocol polling, event loop, or
  test assertion;
- a short, bounded, immediate API-consistency probe needed to finish the
  command that caused the mutation; or
- a tool-owned foreground operation whose live output is necessary to diagnose
  the operation and cannot safely be inspected concurrently.

The implementation must define "short and bounded" concretely: at most one
immediate re-read or a documented sub-minute command-local timeout. Repeated
or multi-minute checks become deferred work. A wakeup must capture the target,
the observed state, the next check time, the continuation command or query,
and the gate that remains closed.

## Host Contract

| Host | Required continuation surface | Required setup/check | Continuation rule |
| --- | --- | --- | --- |
| Codex desktop / ChatGPT app | A current-thread `heartbeat` created through the host automation surface. | Confirm that the active host exposes the heartbeat automation tool. | Use a one-shot same-thread heartbeat; its prompt re-reads the exact PR, run, release, deployment, or process state and continues only when the named gate is clear. |
| Hermes Agent | `cronjob(action="create", ...)` with a one-shot relative schedule, `deliver="origin"`, and `attach_to_session=true`. | Confirm the `cronjob` tool is enabled and `hermes cron status` reports an active gateway before claiming the wakeup is scheduled. | The cron execution is a fresh agent run, so its prompt must be self-contained. `attach_to_session=true` makes the delivered result continuable in the origin conversation; it does not revive a suspended shell or silently authorize the remaining release steps. |
| Other hosts | That host's documented future-wakeup or scheduled-task tool. | Verify its availability before use. | If the host has no approved continuation mechanism, report that limitation and return control rather than emulating a long wait with `sleep`, a background loop, or an idle shell. |

Hermes evidence: its official [Scheduled Tasks (Cron)](https://hermes-agent.nousresearch.com/docs/user-guide/features/cron)
documentation identifies `cronjob` as the agent-facing scheduler, describes
one-shot schedules, and documents continuable jobs through
`attach_to_session`. The same documentation also makes the important boundary
explicit: cron runs in a fresh agent session, so continuation prompts must not
depend on unstated prior context.

## Audit Method and Results

The audit searched the tracked Socket source for agent-facing `wait`, `sleep`,
`poll`, `watch`, `monitor`, `heartbeat`, `wakeup`, `release`, `GitHub Actions`,
and deployment guidance. It found 169 files with a generic wait-related token
and 202 files with a release/deployment-related token. Most are intentionally
outside this policy: application runtime semantics, test synchronization,
watch-directory configuration, historical plans, or generic release mentions.

The following are the complete actionable set. Derived Hermes exports are
listed separately and must be regenerated, never hand-edited.

| Surface | Current state | Planned change |
| --- | --- | --- |
| Root `AGENTS.md` | Says a pushed branch does not imply waiting on CI, but has no universal agent-wait rule. | Add the host-neutral mandatory policy and the short bounded-probe exception; route detailed release behavior to `maintain-project-repo`. |
| `plugins/agent-engineering-skills/skills/schedule-agent-work/SKILL.md` | Selects a native scheduled task but does not map the current hosts or ban idle remote waits. | Add the host matrix above and a required deferred-work envelope. Keep it about scheduling; do not duplicate release choreography. |
| `plugins/repository-skills/skills/maintain-project-repo/SKILL.md` | Recommends a Codex heartbeat only "when available" and describes the full remote-CI mode as a normal default. | Make deferred scheduling mandatory for agent-run remote gates; name Codex heartbeat and Hermes `cronjob` precisely; require a state snapshot and explicit resume gate. |
| `plugins/repository-skills/skills/maintain-project-repo/references/automation-prompts.md` | Mentions only a Codex heartbeat. | Replace it with host-neutral prompts covering Codex and Hermes, and forbid a long-lived polling shell. |
| `plugins/repository-skills/skills/maintain-project-repo/references/release-modes.md` | Permits `gh pr checks --watch` by default and says a same-thread Codex heartbeat for defer. | Specify that agent-run standard releases enter deferred mode after the initial state snapshot; describe continuation packets and both host implementations. |
| `plugins/repository-skills/skills/maintain-project-repo/assets/repo-maintenance/config/release.env` | Defaults `REPO_MAINTENANCE_REMOTE_CI_MODE=full`; comments name a vague Timer/Wakeup or heartbeat. | Default agent-oriented configuration to `defer`, name the host-level scheduler requirement, and retain any blocking mode only as an explicit human-operated shell opt-in if it remains supported. |
| `plugins/repository-skills/skills/maintain-project-repo/assets/repo-maintenance/release.sh` | `full` uses `gh pr checks --watch`; `defer` still has Codex-only wording. | Make defer emit one structured, parseable continuation packet after the initial snapshot. Do not let agent guidance select `full`. Preserve short remote-visibility retries only within the policy boundary; otherwise return the packet for scheduling. |
| `plugins/repository-skills/skills/maintain-project-repo/assets/repo-maintenance/lib/common.sh` | Uses five-second polling loops for branch, tag, release, and initial-check visibility. | Separate bounded read-after-write convergence from remote job monitoring; cap/document the former and return actionable state instead of extending it into a remote wait. |
| `plugins/repository-skills/skills/maintain-project-repo/tests/test_maintain_project_repo_workflow.py` | Locks in Codex-only heartbeat wording and the blocking watcher. | Replace those assertions with portable policy assertions, structured-packet coverage, and a test that agent defaults never invoke `gh ... --watch`. |
| Apple guidance templates: `bootstrap-swift-package/assets/AGENTS.md`, `bootstrap-xcode-app-project/assets/AGENTS.md`, `sync-swift-package-guidance/assets/AGENTS.md`, `sync-swift-package-guidance/assets/append-section.md`, `sync-xcode-project-guidance/assets/AGENTS.md`, and `sync-xcode-project-guidance/assets/append-section.md` | Each tells generated repositories to "watch CI". | Replace with the shared deferred remote-gate rule so downstream repositories do not reinstall the old behavior. Update their focused tests. |
| `plugins/cloud-deployment-skills/skills/dockerized-service-release-deployment-workflow/SKILL.md` | Correctly forbids blind Docker polling, but says to wait on an active build without a host continuation instruction. | Add an explicit ownership-preserving deferred-wakeup rule for hosted build, release-published deployment, environment approval, health, and rollback gates. A wakeup must inspect the original log/session without starting a concurrent Docker operation. |
| `skills/dockerized-service-release-deployment-workflow/` | Generated Hermes export of the Cloud Deployment skill. | Regenerate with `uv run scripts/export_hermes_skills.py`; do not edit this mirror. |
| `plugins/server-side-swift/skills/fly-io-deployment-workflow/SKILL.md` | Covers `fly deploy`, logs, status, and health checks but does not say how an agent waits when the rollout takes time. | Add a deployment-specific continuation checkpoint after an accepted deploy: snapshot app/region/release state, schedule a host wakeup, then inspect status/checks/logs at the wakeup. |
| `plugins/cloud-inference-skills/skills/flash/SKILL.md` | An upstream Runpod mirror uses an unbounded `sleep 2` readiness loop for a long-running local server. | Do not hand-edit this mirror. First confirm the upstream refresh path; then update upstream or carry an approved Socket wrapper/reference that replaces unbounded agent waiting with a short readiness probe followed by a host wakeup. |

### Explicitly audited but not changed

- GitHub Actions design skills for Android, .NET, Python, and Rust teach CI
  construction rather than an agent waiting for a remote run. They will receive
  a short cross-reference only if a concrete release/deployment wait is added;
  duplicating the entire host matrix there would be drift.
- Application polling, SwiftNIO nonblocking-I/O rules, XCUITest waits, test
  confirmations, callback-server waits, media-job monitoring, and shell cleanup
  `wait` calls are program behavior, not an agent's idle wait. They remain
  unchanged.
- Historical roadmap entries retain their historical wording. A new current
  ticket records this plan instead of rewriting release history.

## Implementation Sequence

1. Add the universal root rule and the `schedule-agent-work` host matrix. Define
   the continuation packet fields and the bounded-probe exception once.
2. Change `maintain-project-repo` documentation, prompts, release-mode
   reference, defaults, and script output together. Decide explicitly whether
   human-operated `full` remains supported; agents must not select it.
3. Update all six Apple generated-guidance sources and their tests so a newly
   bootstrapped or synchronized repository inherits the same release policy.
4. Add deployment-specific checkpoints in the Dockerized-service and Fly.io
   workflows. Preserve their existing production approval, exact-digest,
   ownership, and health-check gates.
5. Resolve the Runpod Flash upstream-mirror boundary: inspect its upstream
   source and refresh policy, then make the smallest maintainable change rather
   than editing the checked-in mirror directly.
6. Regenerate Hermes exports, run root and child validation, and use a focused
   fixture to verify the Codex heartbeat and Hermes cron continuation prompts
   contain the same target, state, resume command, and closed gate.

## Acceptance Criteria

- No agent-facing release, CI, or server-deployment guidance tells an agent to
  keep `gh ... --watch`, `sleep` polling, or an idle terminal open for a
  long-running remote gate.
- Codex instructions always use a same-thread heartbeat automation.
- Hermes instructions always use one-shot `cronjob` plus `deliver="origin"`,
  `attach_to_session=true`, a self-contained prompt, and gateway/tool
  availability verification.
- The release script returns a machine-readable continuation packet in deferred
  mode and cannot accidentally merge, tag, or release while the named remote
  gate is pending.
- Script-level read-after-write visibility checks are clearly bounded and do
  not masquerade as a long-running CI or deployment monitor.
- Docker and Fly deployment instructions preserve existing ownership and safety
  constraints while making the future wakeup mandatory.
- Generated Hermes skill exports are current and no generated file was edited
  by hand.

## Validation Plan

Run, serially:

```bash
uv run scripts/validate_socket_metadata.py
uv run scripts/validate_hermes_compatibility.py
uv run scripts/export_hermes_skills.py --check
uv run pytest plugins/repository-skills/skills/maintain-project-repo/tests/test_maintain_project_repo_workflow.py
```

Then run the affected child-plugin tests identified by the template and skill
changes. Use non-mutating fixtures for the release-script continuation packet;
do not open a real PR, schedule a real persistent Hermes job, deploy a service,
or alter a cloud account merely to validate this guidance.
