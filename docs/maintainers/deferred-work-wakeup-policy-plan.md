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

### Minimum Continuation Interval

Every agent-created heartbeat, continuation, or scheduled re-check must be at
least **five minutes** after its observation time. This is a minimum, not a
recommended cadence: agents must never schedule a one-, two-, or four-minute
heartbeat/cron job to emulate polling. They may choose a longer delay when the
provider, CI queue, approval window, or prior state makes that more honest.

The only shorter operation is the command-local, one-time bounded re-read
defined above. It completes the current mutation attempt; it is not scheduled,
is not repeated, and must not grow into a polling loop.

### Continuation Reuse

Before scheduling a remote-gate continuation, inspect for a live scheduler item
for the same repository/target, gate, and identity. If that gate is still
pending and has not failed or changed, reuse the existing heartbeat or cron job
unchanged; do not delete and recreate it merely because the fresh snapshot is
also pending. Pause or delete the item when the gate clears, fails, is
cancelled, or the identity drifts. A new or updated item is appropriate only
after the prior continuation has fired or its recorded state is no longer the
current gate.

## Host Contract

| Host | Required continuation surface | Required setup/check | Continuation rule |
| --- | --- | --- | --- |
| Codex desktop / ChatGPT app | A current-thread `heartbeat` created through the host automation surface. | Confirm that the active host exposes the heartbeat automation tool and look for a live matching heartbeat first. | Reuse the matching heartbeat while its named PR, run, release, deployment, or process gate is pending and healthy. Pause/delete it only on resolution, failure, cancellation, or identity drift. |
| Hermes Agent | `cronjob(action="create" or update, ...)` with a relative schedule of five minutes or longer, `deliver="origin"`, and `attach_to_session=true`. | Confirm the `cronjob` tool is enabled and `hermes cron status` reports an active gateway, then look for a matching cron job first. | Reuse/update the matching cron job rather than churning jobs on an unchanged pending state. The cron execution is a fresh agent run, so its prompt must be self-contained. `attach_to_session=true` makes the delivered result continuable in the origin conversation; it does not revive a suspended shell or silently authorize the remaining release steps. |
| Other hosts | That host's documented future-wakeup or scheduled-task tool. | Verify its availability and inspect for a matching live item before use. | Reuse it while healthy and pending; only create/replace it after it fires or becomes resolved, failed, cancelled, or stale. If the host has no approved continuation mechanism, report that limitation and return control rather than emulating a long wait with `sleep`, a background loop, or an idle shell. |

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

## Proposed Release Automation Shape

### What Changes for Maintainers

The release tooling stays highly automated, but it stops pretending that one
shell process should remain alive for the whole lifecycle. A maintainer starts
the release once. The script advances through every immediately provable step,
then returns a precise continuation packet when GitHub or a deployment platform
owns the next result. The host schedules the next inspection and the same
release command safely advances again.

This is a durable building-block change. It unlocks unattended-but-gated
protected-main releases, review-bot handling, release-published deployments,
and reliable restart/retry behavior without leaving an agent or terminal idle.
It removes duplicated release choreography in host prompts and eliminates the
current confused ownership between `release.sh` and a host scheduler.

The simpler extension path was retaining one large release script and replacing
only `gh pr checks --watch`. That would still combine local mutation, remote
observation, sleep loops, and resume instructions in one opaque process; a
failed or restarted session would remain difficult to reason about.

### Responsibilities

| Surface | Owns | Must not own |
| --- | --- | --- |
| `release.sh` | Deterministic preflight, validation, version bump, Git mutations, PR/release inspection, safe state transitions, and emitting continuation packets. | Sleeping, `gh --watch`, indefinite polling, or scheduling host work. |
| Codex heartbeat / Hermes cron job | Waiting until the chosen next check, then invoking an explicit re-inspection or advance prompt in the correct repository context. | Inventing release state, bypassing approval gates, or assuming a prior shell remains alive. |
| Git and GitHub | Authoritative branch, commit, PR, check, review, merge, tag, and release state. | Storing machine-local secret values or inferred local-validation results. |
| Deployment workflow / provider adapter | Deploying an exact approved artifact and reporting provider-specific rollout/health state. | Rebuilding source, mutating Git release state, or making a production approval decision. |

No database, daemon, or generic queue is proposed. The continuation packet is
transport, not a second source of truth. On every invocation, the script reads
Git and GitHub again and treats a changed branch tip, PR, tag, or release as a
new fact that must be validated or surfaced.

### Commands and State Transitions

Replace the current monolithic `standard` path with three idempotent modes:

| Command | Performs | Stops and emits a packet when |
| --- | --- | --- |
| `release.sh prepare --mode standard --version vX.Y.Z` | Validates locally, creates or recognizes the version-bump commit, pushes the branch, creates/finds the PR, and reads one initial PR/check snapshot. | The PR/check/review gate is not conclusively clear. |
| `release.sh inspect --mode standard --version vX.Y.Z` | Reads only: branch tip, PR, check, review/comment, merge, tag, and GitHub Release state. | It always returns a normalized state and never waits or mutates. This is the default scheduled-wakeup action. |
| `release.sh advance --mode standard --version vX.Y.Z` | Re-reads state, verifies the expected branch/PR/tag identity, then performs every safe immediately-ready next step: merge, fast-forward, tag, push tag, create/verify Release, and branch accounting. | A remote gate is pending, a read-after-write result is not immediately visible, state differs from the packet, or an approval/review condition is not satisfied. |

`advance` is intentionally resumable, not blindly transactional. Re-running it
after an interruption must recognize an existing version-bump commit, PR,
merge, tag, or release only when it points at the expected commit. A branch tip
that changed after `prepare` invalidates that prepare result and sends the
release back to the local-validation gate rather than merging new code on the
strength of stale checks.

An explicit human-only `--remote-ci-mode full` may remain as a convenience for
a terminal user who deliberately wants live `gh` output. It is not the default
agent path and is never selected by guidance. The agent default becomes this
prepare/inspect/advance path; it does not call a blocking watcher.

### Continuation Packet

When a command reaches an external gate, it writes one human-readable summary
and one machine-readable JSON object. The packet contains no credentials and
is sufficient for a fresh Hermes cron session or a later Codex heartbeat:

```json
{
  "schema": "repo-maintenance-continuation/v1",
  "operation": "standard-release",
  "repository": "owner/repository",
  "release_tag": "vX.Y.Z",
  "branch": "release/vX.Y.Z",
  "head_commit": "full-commit-sha",
  "pr_number": "123",
  "phase": "awaiting-pr-checks",
  "minimum_delay_minutes": 5,
  "resume_command": "scripts/repo-maintenance/release.sh --mode standard --version vX.Y.Z --operation inspect",
  "advance_command": "scripts/repo-maintenance/release.sh --mode standard --version vX.Y.Z --operation advance"
}
```

`minimum_delay_minutes` is the script's sole delay field; it must be at least
five. The host adapter schedules no sooner than that floor. Its prompt must
include the packet, tell the agent to run `inspect` first (or `prepare` for a
pre-PR `not-started` or `awaiting-branch-visibility` packet), and permit
`advance` only if the packet's repository, tag, branch, commit, and gate still
match current source-of-truth state. If still pending and the same continuation
is live, it retains that scheduler item rather than replacing it. It creates or
updates a continuation only after the previous one fires or is stale. If failed
or changed, it reports the discrepancy and does not continue automatically.

### Lifecycle

1. `prepare` validates the release candidate and publishes the release branch
   and PR. It emits `awaiting-pr-checks` instead of watching CI.
2. The host creates one continuation, or reuses the live matching item. The
   wakeup runs `inspect` and either reports a failed/changed gate, retains the
   healthy pending item (or updates it after it fires), or calls `advance`.
3. `advance` verifies CI, review comments, and review-bot contexts before
   merging. It never treats a pending bot as approval.
4. After merge, `advance` fast-forwards the local base, creates/pushes the tag,
   and creates/verifies the GitHub Release. A remote object that is not yet
   visible produces another packet, not a sleep loop.
5. Release completion remains distinct from deployment completion. A
   release-published deployment workflow receives the immutable artifact and
   creates its own provider/health continuation packet. It does not make the
   Git release script wait for a server rollout.
6. Final branch accounting and cleanup occur only after the GitHub Release
   state is confirmed. A pending deployment is reported separately, never
   misrepresented as a failed or completed release.

### Failure and Recovery Rules

- A failed check, requested changes, new review comment, or changed branch tip
  stops advancement and names the exact next human or agent action.
- A scheduler failure never authorizes a fallback polling loop. The current
  state and continuation packet are reported for a user-directed retry.
- A duplicate wakeup is harmless: `inspect` is read-only and `advance` verifies
  identities before every mutation.
- A restart on a different host does not reuse machine-local shell state. It
  can only continue after resolving the repository and proving the packet still
  matches Git/GitHub state.
- Deployment adapters retain their own approval and rollback rules. The release
  executor only proves the release artifact is published and hands off its
  exact immutable reference.

## Implementation Sequence

1. Add the universal root rule and the `schedule-agent-work` host matrix. Define
   the continuation packet fields, five-minute minimum interval, scheduler
   adapter contract, and bounded-probe exception once.
2. Refactor `maintain-project-repo` from its monolithic release path into
   idempotent `prepare`, `inspect`, and `advance` commands. Keep Git/GitHub as
   the source of truth; do not add a database or background daemon.
3. Change `maintain-project-repo` documentation, prompts, release-mode
   reference, defaults, script output, and focused tests together. Preserve
   `full` only as an explicit human-only choice if maintainers still want it;
   agents must not select it.
4. Update all six Apple generated-guidance sources and their tests so a newly
   bootstrapped or synchronized repository inherits the same release policy.
5. Add deployment-specific checkpoints in the Dockerized-service and Fly.io
   workflows. Preserve their existing production approval, exact-digest,
   ownership, health-check, rollback, and separate deployment-completion gates.
6. Resolve the Runpod Flash upstream-mirror boundary: inspect its upstream
   source and refresh policy, then make the smallest maintainable change rather
   than editing the checked-in mirror directly.
7. Regenerate Hermes exports, run root and child validation, and use a focused
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
- Every continuation packet emits `minimum_delay_minutes >= 5`, and every
  agent-created heartbeat or scheduled re-check honors that floor; focused
  tests reject shorter values and repeated short-delay reschedules.
- The release script returns a machine-readable continuation packet in deferred
  mode, supports idempotent `prepare`, read-only `inspect`, and guarded
  `advance` actions, and cannot accidentally merge, tag, or release while the
  named remote gate is pending.
- A changed branch tip invalidates its prior local-validation result; a duplicate
  continuation cannot produce duplicate merges, tags, or releases.
- Release publication and provider deployment remain separate state machines
  with separate completion claims.
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
