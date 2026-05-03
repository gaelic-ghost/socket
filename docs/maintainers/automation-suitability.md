# Automation Suitability

This note audits the `productivity-skills` maintenance skills and the `apple-dev-skills` sync skills for cross-repository automation.

The practical split is:

- Use Codex GUI app automations for scheduled reporting, check-only audits, and low-risk reminders that stay inside one thread or one workspace job.
- Use `codex exec` or the Codex GitHub Action for deterministic one-repo tasks that can run from a narrow prompt, make a branch, run tests, and open a PR.
- Use an external agent built with the Agents SDK when the workflow needs durable multi-repo state, task queues, prioritization, handoffs, retries, traces, and policy-controlled write decisions across many repositories.

Official OpenAI anchors:

- Codex non-interactive automation: <https://developers.openai.com/codex/noninteractive>
- Codex GitHub Action from non-interactive mode: <https://developers.openai.com/codex/noninteractive#alternative-use-the-codex-github-action>
- Agents SDK workflow example: <https://developers.openai.com/cookbook/examples/codex/codex_mcp_agents_sdk/building_consistent_workflows_codex_cli_agents_sdk>
- Agents SDK parallel agents example: <https://developers.openai.com/cookbook/examples/agents_sdk/parallel_agents>
- Agents SDK session memory example: <https://developers.openai.com/cookbook/examples/agents_sdk/session_memory>

## Automation Tiers

### Tier 1: GUI automation

Use this for recurring check-ins where the output is a report or a proposed next step. Good jobs include:

- list repos whose docs are stale
- run check-only audits and summarize findings
- triage open GitHub issues without mutating code
- remind Gale to approve a batch of candidate PRs

Avoid using this as the main write path for broad repo changes. GUI automations are useful for keeping attention on the right work, but they should not become the scheduler, state store, policy engine, and release manager for a multi-repo maintenance program.

### Tier 2: `codex exec` or Codex GitHub Action

Use this when one repository can be handled independently with a tight prompt and bounded permissions. Good jobs include:

- run a `check-only` documentation audit
- apply one canonical docs skill to one repo
- refresh `maintain-project-repo`
- run `sync-swift-package-guidance` or `sync-xcode-project-guidance`
- fix CI failures in response to a failed workflow
- open a PR with the patch and validation output

This tier is the likely default for the next phase because the current skills already expose deterministic inputs, check-only/report-only modes, bounded apply modes, and repo-local validation commands.

### Tier 3: external Agents SDK service

Use this when the automation needs to own a cross-repo backlog rather than one isolated repo run. Good jobs include:

- maintain a repo inventory and decide which repos need which skills
- batch docs refreshes while limiting concurrent heavy validation on Gale's machines
- triage issues across repositories and open linked implementation PRs
- split larger Swift source organization work into reviewable slices
- track failed runs, retries, PR outcomes, and stale follow-ups
- coordinate read-only discovery agents, implementation agents, and verification agents with traces

This is the right shape for "make my local repo fleet healthier over time" because it needs durable state, observability, and policy gates that are bigger than a single Codex chat or single `codex exec` invocation.

## Skill Fit Matrix

| Skill | Best automation tier | Why |
| --- | --- | --- |
| `explain-code-slice` | GUI automation or external agent read phase | It is read-only and explanation-focused. Good for batch reports, but it should not mutate repos. |
| `maintain-project-accessibility` | `codex exec` for one repo; external agent for fleet rollout | It has check-only/apply modes and one target file. Use check-only broadly, apply through PRs. |
| `maintain-project-agents` | `codex exec` for one repo; external agent for policy rollout | It changes durable agent instructions, so apply mode should be branch-and-PR gated. GUI automation is good for drift reports. |
| `maintain-project-api` | `codex exec` for one repo; external agent for API-doc inventory | It must avoid invented endpoints and credentials. Best run with repo-grounded evidence and PR review. |
| `maintain-project-contributing` | `codex exec` for one repo; external agent for standardization campaigns | It owns contributor workflow. Good candidate for automated apply after check-only evidence. |
| `maintain-project-readme` | `codex exec` for one repo; external agent for product-doc sweep | It now keeps README product-focused and hands contributor details to `CONTRIBUTING.md`, which makes it safer for repeated repo-wide application. |
| `maintain-project-repo` | `codex exec` first; external agent for coordinated rollout | It installs managed scripts and CI wrappers. It is deterministic, but the write surface is broad enough that every repo should get a PR. |
| `maintain-project-roadmap` | GUI check-only or `codex exec`; external agent for planning sync | Roadmaps reflect human priorities. Automate stale-structure fixes, but keep milestone meaning human-reviewed. |
| `sync-swift-package-guidance` | `codex exec` for one repo; external agent for SwiftPM fleet sync | It classifies repo shape, writes `AGENTS.md`, and refreshes `maintain-project-repo`. It is suitable for PR-based automation after the Socket-cache companion discovery fix. |
| `sync-xcode-project-guidance` | `codex exec` for one repo; external agent for Apple-app fleet sync | It has the same shape as the SwiftPM sync skill but needs more caution around Xcode project state and Apple docs gates. |

## Recommended Rollout Shape

Start with a two-phase system:

1. Use Codex GUI automations for nightly or weekly inventory reports. These should run check-only audits across a repo list and produce a ranked queue: docs drift, missing maintainer scripts, stale AGENTS guidance, failing issue triage, and Swift/Xcode sync candidates.
2. Use `codex exec` jobs for one-repo PR creation. Each job should receive the repo path, the exact skill, the requested run mode, validation command, and PR expectations. It should never batch unrelated repos into one execution.

Move to an Agents SDK service when the queue itself becomes the product. The external agent should own:

- repo inventory
- per-repo state
- scheduling and concurrency limits
- GitHub issue/PR state
- retry and failure records
- model/tool traces
- policy gates for write operations

## Swift Source Organization

Organizing or breaking up Swift sources should start as human-approved, PR-based automation rather than unsupervised scheduled mutation.

Good automation path:

1. GUI automation or `codex exec` produces a read-only structure report.
2. Gale approves one slice.
3. `codex exec` creates one branch for that repo and applies the slice.
4. Local validation runs.
5. A PR opens with a clear diff and rollback boundary.

If this becomes a repeated fleet workflow, graduate it into an Agents SDK service with explicit task slicing, one-PR-per-slice rules, validation budgets, and traces. This work is too semantic and too easy to overreach for direct cron-style apply mode.
