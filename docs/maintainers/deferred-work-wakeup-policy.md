# Deferred Work Wakeup Policy

Use this live reference when an agent needs to resume work after external CI,
review, release, deployment, provider, or remote-worker state changes.

## Required Behavior

An agent must not keep a terminal, `sleep` loop, watcher, or remote-status poll
open merely to wait for an external result. It must use the current host's
approved scheduler with an interval of at least five minutes.

Before creating a continuation, inspect for a live scheduler item for the same
target, gate, and identity. Reuse that item unchanged while the gate is pending
and healthy. Pause or delete it only when the gate resolves, fails, is
cancelled, or its identity changes. Create or update an item only after the
prior item has fired or is stale.

One immediate command-local re-read is allowed after a mutation. It is not a
scheduled recheck and must not become a polling loop.

## Host Rules

| Host | Continuation | Required behavior |
| --- | --- | --- |
| Codex desktop / ChatGPT | Same-thread `heartbeat` through the host automation surface. | Confirm the heartbeat tool exists, then reuse the matching live heartbeat. Its prompt must name the exact target, identity, observed state, and safe next inspection. |
| Hermes Agent | Self-contained `cronjob` with `deliver="origin"` and `attach_to_session=true`. | Confirm the cron tool and active gateway, then create or update the matching cron job. A cron run is a fresh session, so the prompt must include all necessary state. |
| Other hosts | The host's documented future-wakeup mechanism. | Verify it exists before use; otherwise report the limitation rather than emulating a wait with a shell loop. |

On wakeup, inspect source-of-truth state first. Continue only if every recorded
identity still equals the fresh state. A mismatch stops the prior continuation
and requires a new packet; it never authorizes a merge, deployment, rollback,
or other mutation.

## Release Contract

`maintain-project-repo` releases use bounded `prepare`, `inspect`, and
`advance` operations. They never watch CI.

- `prepare` validates locally, publishes the release branch/PR, takes one
  remote snapshot, and emits a continuation packet when a gate remains closed.
- `inspect` is read-only, returns a normalized state even before a PR exists,
  and is the default wakeup action for a post-PR packet.
- `advance` re-reads GitHub state and performs only immediately-safe work. It
  does not merge while required checks, review bots, comments, or approvals are
  pending.

Every emitted packet includes the repository, release tag, branch, head commit,
PR number, phase, `minimum_delay_minutes`, and resume/advance commands. The
minimum delay is five minutes. Pre-PR packets resume with `prepare`; post-PR
packets resume with `inspect`.

For exact release-script behavior and configuration, use
[`maintain-project-repo`'s release modes](../../plugins/repository-skills/skills/maintain-project-repo/references/release-modes.md).

## Deployment Contract

For build or deployment continuations, record the relevant immutable identity:
tag, digest, workflow/deployment run, environment, provider target, release,
and health target. On wakeup, compare every recorded value with the fresh value
before any further action. Keep release publication and provider deployment as
separate completion states.

## Verification

Run these serially after changing this policy or its exported guidance:

```bash
just repo-sync
just repo-validate
just test
```
