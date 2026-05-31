# Automation Suitability

This note audits the `productivity-skills` maintenance skills and the
`apple-dev-skills` sync skills for cross-repository automation.

The practical split is:

- Use Codex app automations for scheduled reporting, check-only audits, and
  low-risk reminders that stay inside one thread or one workspace job.
- Use `codex exec` or the Codex GitHub Action for deterministic one-repo tasks
  that can run from a narrow prompt, make a branch, run tests, and open a PR.
- Use Codex subagents only for explicit-trigger parallel work inside a Codex
  run, especially read-heavy discovery or review fan-out.
- Use a code-owned agent service when the workflow needs durable state, task
  queues, prioritization, handoffs, retries, traces, and policy-controlled
  write decisions across many repositories.

## Authoritative Sources

OpenAI:

- Codex app automations: <https://developers.openai.com/codex/app/automations>
- Codex non-interactive mode: <https://developers.openai.com/codex/noninteractive>
- Codex GitHub Action: <https://developers.openai.com/codex/github-action>
- Codex subagents: <https://developers.openai.com/codex/subagents>
- Agents SDK overview: <https://developers.openai.com/api/docs/guides/agents>

Other agent frameworks:

- LangGraph overview: <https://docs.langchain.com/oss/python/langgraph/overview>
- Hermes Agent documentation: <https://hermes-agent.nousresearch.com/docs>
- Hugging Face Hermes Agent integration: <https://huggingface.co/docs/inference-providers/main/en/integrations/hermes-agent>

## Current Framework Read

Codex app automations are the right surface when Socket wants recurring Codex
tasks that report findings into the Codex inbox, optionally run in a worktree,
and use existing skills or plugins. They are a good scheduling surface, not a
durable fleet scheduler or cross-repo policy database.

`codex exec` is the right surface when the job is a bounded command-line run.
The official docs emphasize explicit sandbox settings, JSONL output, structured
final output with schemas, and single-run automation. The Codex GitHub Action is
the safer GitHub Actions path because it keeps API key exposure away from
repository-controlled setup and test steps.

Codex subagents are useful only after an explicit trigger. They inherit the
parent sandbox policy, can run specialized read or implementation threads, and
return results to the parent workflow. Treat them as in-run parallel workers,
not as a background queue or a substitute for repo-local validation.

The OpenAI Agents SDK is the best OpenAI code-first path when a server owns the
agent loop, tool execution, state, approvals, traces, and handoffs. Use it when
Socket needs a real agent application around a repo fleet rather than a prompt
template that calls Codex once.

LangGraph is a good fit when the workflow is naturally a long-running state
machine or graph: persisted state, human-in-the-loop pauses, streaming,
explicit transitions, memory, and production observability are first-class
requirements. It is heavier than a Codex prompt or Agents SDK run when the job
is only "run this maintainer skill against one repo."

Hermes Agent is a full autonomous CLI/runtime with memory, skills, scheduled
automations, messaging gateways, terminal backends, MCP support, and subagents.
It is relevant as a peer agent environment or future integration target, but it
is not the best primary abstraction for Socket's repo-maintenance automation
guidance unless Gale intentionally wants Hermes-specific workflows.

## Automation Tiers

### Tier 1: Codex app automation

Use this for recurring check-ins where the output is a report or a proposed next step. Good jobs include:

- list repos whose docs are stale
- run check-only audits and summarize findings
- triage open GitHub issues without mutating code
- remind Gale to approve a batch of candidate PRs
- wake an existing thread while a release, CI run, or review loop is still active

Avoid using this as the main write path for broad repo changes. App
automations are useful for keeping attention on the right work, but they should
not become the scheduler, state store, policy engine, and release manager for a
multi-repo maintenance program.

### Tier 2: `codex exec` or Codex GitHub Action

Use this when one repository can be handled independently with a tight prompt
and bounded permissions. Good jobs include:

- run a `check-only` documentation audit
- apply one canonical docs skill to one repo
- refresh `maintain-project-repo`
- run `sync-swift-package-guidance` or `sync-xcode-project-guidance`
- fix CI failures in response to a failed workflow
- open a PR with the patch and validation output
- emit structured JSON output for a scheduler or report collector

This tier is the likely default for the next phase because the current skills
already expose deterministic inputs, check-only/report-only modes, bounded
apply modes, and repo-local validation commands.

### Tier 3: Codex subagent fan-out

Use this when one Codex run needs parallel discovery, review, or comparison and
the user or narrower workflow guidance explicitly asks for subagents. Good jobs
include:

- split a repository-wide review into security, correctness, docs, and test
  passes
- inspect separate document families before one main-thread docs edit
- compare one upstream documentation source per worker
- process a CSV of similar audit targets and return structured summaries

Keep apply-mode edits in the parent run unless each worker has a clearly
disjoint write scope and Gale explicitly asked for parallel implementation.

### Tier 4: code-owned agent service

Use this when the automation needs to own a cross-repo backlog rather than one
isolated repo run. Good jobs include:

- maintain a repo inventory and decide which repos need which skills
- batch docs refreshes while limiting concurrent heavy validation on Gale's machines
- triage issues across repositories and open linked implementation PRs
- split larger Swift source organization work into reviewable slices
- track failed runs, retries, PR outcomes, and stale follow-ups
- coordinate read-only discovery agents, implementation agents, and verification agents with traces

This is the right shape for "make my local repo fleet healthier over time"
because it needs durable state, observability, and policy gates that are bigger
than a single Codex chat or single `codex exec` invocation.

Use the Agents SDK first when Socket wants a code-first OpenAI agent
application with typed tools, handoffs, guardrails, traces, and custom state.
Use LangGraph when the work is fundamentally graph-shaped and needs persisted
state transitions, human pauses, and explicit execution resumes. Consider
Hermes only for Hermes-specific agent runtime integration or experiments, not
as the default Socket maintainer automation runtime.

## Skill Fit Matrix

| Skill | Best automation tier | Why |
| --- | --- | --- |
| `explain-code-slice` | Codex app automation, subagent read phase, or code-owned read phase | It is read-only and explanation-focused. Good for batch reports, but it should not mutate repos. |
| `maintain-project-accessibility` | `codex exec` for one repo; code-owned service for fleet rollout | It has check-only/apply modes and one target file. Use check-only broadly, apply through PRs. |
| `maintain-project-agents` | `codex exec` for one repo; code-owned service for policy rollout | It changes durable agent instructions, so apply mode should be branch-and-PR gated. App automation is good for drift reports. |
| `maintain-project-api` | `codex exec` for one repo; subagents for read-heavy evidence; code-owned service for API-doc inventory | It must avoid invented endpoints and credentials. Best run with repo-grounded evidence and PR review. |
| `maintain-project-contributing` | `codex exec` for one repo; code-owned service for standardization campaigns | It owns contributor workflow. Good candidate for automated apply after check-only evidence. |
| `maintain-project-readme` | `codex exec` for one repo; code-owned service for product-doc sweep | It keeps README product-focused and hands contributor details to `CONTRIBUTING.md`, which makes it safer for repeated repo-wide application. |
| `maintain-project-repo` | `codex exec` first; code-owned service for coordinated rollout | It installs managed scripts and CI wrappers. It is deterministic, but the write surface is broad enough that every repo should get a PR. |
| `maintain-project-roadmap` | App check-only or `codex exec`; code-owned service only for planning sync | Roadmaps reflect human priorities. Automate stale-structure fixes, but keep milestone meaning human-reviewed. |
| `sync-swift-package-guidance` | `codex exec` for one repo; code-owned service for SwiftPM fleet sync | It classifies repo shape, writes `AGENTS.md`, and refreshes `maintain-project-repo`. It is suitable for PR-based automation after the Socket-cache companion discovery fix. |
| `sync-xcode-project-guidance` | `codex exec` for one repo; code-owned service for Apple-app fleet sync | It has the same shape as the SwiftPM sync skill but needs more caution around Xcode project state and Apple docs gates. |

## Dedicated Skill Recommendation

Add a future `productivity-skills:design-agent-automation-workflow` skill if
Gale starts repeating agent or automation planning work across repositories.
The useful shape is a planning and scaffolding skill, not a runtime framework:

- classify the work as app automation, `codex exec`, subagent fan-out, Agents
  SDK service, LangGraph graph, Hermes integration, or "do not automate yet"
- name state, queue, approval, retry, observability, and validation needs
- choose which repo or child plugin should own the implementation
- produce a prompt template, framework checklist, and safety gates
- link to current official docs for every framework it mentions

This belongs in `productivity-skills` because the decision is broadly useful
and framework-neutral. If the skill later grows framework-specific
implementation steps, delegate those slices to `python-skills`, `web-dev-skills`,
or another stack-owned plugin rather than making the productivity skill own
SDK code generation.

## Recommended Rollout Shape

Start with a two-phase system:

1. Use Codex app automations for nightly or weekly inventory reports. These should run check-only audits across a repo list and produce a ranked queue: docs drift, missing maintainer scripts, stale AGENTS guidance, failing issue triage, and Swift/Xcode sync candidates.
2. Use `codex exec` jobs for one-repo PR creation. Each job should receive the repo path, the exact skill, the requested run mode, validation command, and PR expectations. It should never batch unrelated repos into one execution.

Move to a code-owned agent service when the queue itself becomes the product.
The external agent should own:

- repo inventory
- per-repo state
- scheduling and concurrency limits
- GitHub issue/PR state
- retry and failure records
- model/tool traces
- policy gates for write operations

Use Agents SDK as the default service candidate when OpenAI model/tool
integration, handoffs, guardrails, and traces are the center of the work. Use
LangGraph when explicit persisted graph transitions and human-in-the-loop
resume points are the center of the work. Do not choose Hermes as the default
service target unless the workflow specifically needs Hermes' CLI/runtime,
messaging gateways, local memory, or portable skill ecosystem.

## Swift Source Organization

Organizing or breaking up Swift sources should start as human-approved, PR-based automation rather than unsupervised scheduled mutation.

Good automation path:

1. Codex app automation or `codex exec` produces a read-only structure report.
2. Gale approves one slice.
3. `codex exec` creates one branch for that repo and applies the slice.
4. Local validation runs.
5. A PR opens with a clear diff and rollback boundary.

If this becomes a repeated fleet workflow, graduate it into a code-owned agent service with explicit task slicing, one-PR-per-slice rules, validation budgets, and traces. This work is too semantic and too easy to overreach for direct cron-style apply mode.
