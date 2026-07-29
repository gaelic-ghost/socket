---
name: design-agent-eval-workflow
description: Design evaluation workflows for agent, skill, prompt, and automation behavior before implementation. Use when choosing eval cases, graders, thresholds, regression runs, full-auto gates, or escalation points for Codex skills, repo-local agents, OpenAI Agents SDK services, LangGraph graphs, or other agentic workflows.
---

# Design Agent Eval Workflow

Design evaluation workflows for agent, skill, prompt, and automation behavior.

This skill is a framework-neutral eval planning surface. It helps define what
good behavior means, how to measure it repeatably, which tasks can safely run
fully automatically, and where escalation remains necessary because safety
cannot be engineered into the workflow with reasonable confidence.

## Inputs

- Required: the agent, skill, prompt, automation, or workflow to evaluate
- Useful: target runtime, task examples, expected outputs, failure modes, write
  surface, external services touched, acceptable risk, and current validation
  commands
- Optional: preferred eval runner, existing case format, model/provider
  constraints, budget, cadence, and reporting destination

## Workflow

1. Restate the behavior under evaluation and the real decision the eval should
   support.
2. Define the automation target:
   - `full-auto`: safe to run without human approval when it passes objective
     gates
   - `auto-with-escalation`: runs automatically but stops on bounded ambiguity,
     failed checks, secret exposure, destructive writes, or external side
     effects
   - `human-review`: requires review because the task cannot yet be made safe
     enough through scope, validation, sandboxing, rollback, or orchestration
   - `manual-only-for-now`: behavior is too underspecified or high-risk for a
     useful eval-backed automation claim
3. Build the case set:
   - happy path
   - realistic messy input
   - regression examples from past failures
   - refusal or stop conditions
   - tool, filesystem, network, or credential boundary cases
   - full-auto eligibility cases when automation is the goal
4. Choose graders:
   - deterministic assertions for structure, file changes, commands, outputs,
     and policy boundaries
   - snapshot review only when stable text shape matters
   - model grading only for judgment that cannot be reduced to deterministic
     checks, with explicit rubrics and sampled audit review
5. Set pass thresholds, stop conditions, and escalation rules.
6. Choose the run surface:
   - local script or `uv run pytest` for repo-local skill and prompt evals
   - `codex exec` or Codex GitHub Action for repeatable repo tasks
   - OpenAI Agents SDK tracing/evals when application code owns tools,
     handoffs, guardrails, and traces
   - LangGraph evaluation or LangSmith-style tracing when a stateful graph owns
     transitions, persistence, resume behavior, or graph-level observability
   - a stack-owned test runner when the workflow belongs to a narrower plugin
7. Produce a scaffold with cases, grader shape, thresholds, reporting,
   automation eligibility, and implementation handoff.
8. Link official docs for every framework, runtime, or eval surface named.

## Decision Rules

- Prefer full automation when the task has bounded inputs, explicit write
  scope, deterministic or reviewable validation, rollback or no-op behavior, and
  no unapproved external side effects.
- Use human-in-the-loop only for the exact decision that cannot be made safe
  through narrower scope, sandboxing, deterministic checks, retries, rollback,
  reporting, or an orchestration layer.
- Prefer deterministic evals before model-graded evals. Add model grading only
  where judgment is the thing being tested.
- Prefer small case sets that run often over broad eval suites that are too
  expensive or brittle to run before changes.
- Capture negative cases that prove the workflow stops instead of guessing,
  writing, contacting services, or leaking secrets.
- Keep the eval owner close to the behavior owner: skill evals live with the
  skill, repo-local agent evals live with the agent package, service evals live
  with the service, and graph evals live with the graph runtime.
- Treat LangGraph as an implementation/eval surface only when the workflow is
  already graph-shaped or needs graph state, persistence, or transition-level
  observability.

## Output Contract

Return a concise plan with these sections:

- `Recommendation`: eval run surface and automation target
- `Behavior Under Test`: what is being evaluated and what decision it supports
- `Case Set`: minimum useful cases and why each exists
- `Graders`: deterministic checks, model rubrics, snapshots, or trace checks
- `Safety Gates`: full-auto gates, escalation points, rollback, and stop rules
- `Run Cadence`: local, pre-commit, CI, scheduled, release, or post-change
- `Scaffold`: case schema, runner outline, or test-file outline
- `Handoff`: owning skill, plugin, package, service, graph, or official docs
- `Sources`: official docs checked, with links

Use `references/eval-plan-template.md` when the user asks for a reusable prompt,
issue body, project note, or implementation brief.

## Guardrails

- Do not claim a workflow is safe for full automation unless the proposed evals
  can catch the meaningful unsafe outcomes.
- Do not use human review as a blanket fallback when a narrower automation,
  validation gate, rollback path, or orchestration agent would make the task
  reasonably safe.
- Do not build or wrap OpenAI Agents SDK, LangGraph, Codex, or other runtimes
  inside this skill. Hand implementation to the owning stack.
- Do not send secrets, private user data, direct personal contact data, or
  credentials into eval artifacts.
- Do not let eval reports become durable policy. Move durable conclusions into
  the owning docs, skill, tests, scripts, or runtime configuration.

## References

- `agents/openai.yaml`
- `references/eval-plan-template.md`
- `references/eval-surface-selection.md`
