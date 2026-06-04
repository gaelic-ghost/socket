---
name: design-agent-automation-workflow
description: Design framework-neutral agent and automation workflows before implementation. Use when choosing between Codex app automations, codex exec, Codex subagents, OpenAI Agents SDK services, LangGraph graphs, Hermes-specific workflows, full-auto execution, auto-with-escalation, or no automation yet, and when the user wants a planning/scaffolding pass that delegates stack-specific implementation to the owning plugin or official docs.
---

# Design Agent Automation Workflow

Design agent and automation workflows before implementation.

This skill is a framework-neutral planning surface. It helps choose the smallest
defensible automation shape, name the safety and state boundaries, decide
whether the task is fit for full automation or needs exact escalation gates, and
produce a scaffold another stack-owned skill or implementation pass can use.

## Inputs

- Required: the automation goal or workflow idea
- Useful: target repository, cadence, write surface, expected outputs, full-auto
  eligibility, escalation points, state needs, retry needs, observability needs,
  and preferred runtime constraints
- Optional: known framework preference, deployment target, language stack, or
  existing scheduler/service

## Workflow

1. Restate the intended real-world outcome and the smallest useful first run.
2. Decide whether automation is appropriate yet. Prefer safe full automation
   when bounded scope, validation, rollback or draft behavior, and side-effect
   controls make it reasonably reliable. Use human review only for the exact
   decision that cannot be made safe through narrower scope, deterministic
   checks, retries, rollback, sandboxing, or an orchestration layer.
3. Classify the best-fit surface:
   - Codex app automation
   - `codex exec` or Codex GitHub Action
   - Codex subagent fan-out
   - OpenAI Agents SDK service
   - LangGraph graph
   - Hermes-specific workflow
   - full-auto execution
   - auto-with-escalation
   - no automation yet
4. Name the practical reason for the choice: schedule, isolation, state,
   approvals, retries, observability, deployment, or integration with an
   existing runtime.
5. Identify ownership:
   - prefer existing agent skills, plugins, scripts, and official workflow
     surfaces before adding new automation code, so business process knowledge
     has one maintained source of truth
   - prompt or skill-only work stays in this planning skill
   - Python implementation belongs in `python-skills`
   - web or TypeScript implementation belongs in the Build Web Apps plugin or the repo's owning JavaScript/TypeScript workflow
   - Swift or Apple-platform implementation belongs in Apple/Swift-owned skills
   - Hermes-specific work belongs in Hermes docs or a Hermes-owned skill if one
     exists later
6. Produce a scaffold with the chosen surface, guardrails, validation plan,
   output contract, and next implementation handoff.
7. Link official docs for every framework or runtime named in the
   recommendation.

## Decision Rules

- Prefer reusing an existing skill, plugin, repo script, or official tool when
  one already owns the task. Add a new agent/service only when the existing
  workflow cannot express the needed state, approval, scheduling, or integration
  boundary.
- Prefer full automation when the workflow has bounded inputs, explicit write
  scope, deterministic or reviewable validation, durable failure reporting,
  bounded retries, and rollback, no-op, or draft behavior for unsafe outcomes.
- Prefer auto-with-escalation when one specific decision remains unsafe or
  ambiguous. Name the exact escalation trigger instead of making the whole
  workflow human-reviewed.
- Prefer Codex app automations for recurring check-ins, reminders, inbox
  reports, and skill-backed background tasks where Codex should stay the user
  interface.
- Prefer `codex exec` for deterministic one-repo CLI jobs with explicit sandbox
  settings, structured output, CI integration, or PR-producing workflows.
- Prefer Codex subagents only when the user or applicable workflow explicitly
  asks for parallel agent work and the jobs can be split into bounded mostly
  independent read, review, test, or implementation slices.
- Prefer the OpenAI Agents SDK when application code should own agent
  orchestration, tools, handoffs, guardrails, approvals, state, tracing, or
  server integration.
- Prefer LangGraph when the workflow is a durable graph with persisted state,
  explicit transitions, long-running execution, human-in-the-loop pauses,
  streaming, and resume behavior.
- Prefer Hermes-specific workflows only when the work intentionally targets the
  Hermes Agent runtime, Hermes memory/skills/automation model, messaging
  gateways, or Hermes provider configuration.
- Prefer no automation yet only when the goal, validation, owner, write scope,
  or rollback/escalation boundary is still unclear after trying to narrow the
  workflow.

## Output Contract

Return a concise plan with these sections:

- `Recommendation`: one chosen surface and one sentence explaining why
- `Not Chosen`: short reasons the other plausible surfaces are not first
- `State And Safety`: state, automation target, escalation gates, secrets,
  permissions, write scope, and rollback/no-op behavior
- `Scaffold`: prompt, job shape, graph shape, or service outline
- `Validation`: how the first run should prove it worked
- `Handoff`: which skill, plugin, repo, or official docs should own
  implementation
- `Sources`: official docs checked, with links

Use `references/automation-plan-template.md` when the user asks for a reusable
prompt, issue body, project note, or implementation brief.

## Guardrails

- Do not implement framework runtime code unless the user asks for that as a
  second step and the owning stack/plugin guidance has been loaded.
- Do not wrap OpenAI Agents SDK, LangGraph, Hermes, or Codex runtimes inside
  this skill.
- Do not invent scheduler, queue, auth, deployment, or observability features
  that are not grounded in the target repo or official docs.
- Do not duplicate business-process logic that already belongs to an existing
  agent skill, plugin, repo script, or official workflow surface. Delegate,
  invoke, or extend the owner instead.
- Do not suggest unattended write automation unless the validation path,
  rollback/no-op path, and escalation boundary are explicit.
- Do not use human review as a blanket fallback when a narrower automation,
  validation gate, rollback path, or orchestration agent would make the task
  reasonably safe.
- Do not use Codex subagents unless the user requested them or applicable
  workflow guidance tells the agent to ask and receive permission first.
- Keep the first version small enough to review: one workflow, one repo, or one
  disjoint batch before fleet-scale rollout.

## References

- `agents/openai.yaml`
- `references/framework-selection.md`
- `references/automation-plan-template.md`
