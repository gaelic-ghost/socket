# Codex Subagent Skill Guidance

Use this document when `agent-portability-skills` needs to bootstrap or audit guidance about Codex subagents in skills-export and plugin-export repositories.

This document does not replace OpenAI's Codex docs. It gives these maintainer skills a narrow house pattern for teaching optional subagent use without overstating what Codex does automatically.

Date checked: 2026-07-19.

## Official Model

OpenAI's Codex docs call this feature `subagents`.

- A `subagent` is a delegated agent that Codex starts to handle a specific task.
- A `subagent workflow` is a workflow where Codex runs parallel agents and combines their results.
- Current Codex releases enable subagent workflows by default, but Codex only spawns subagents when there is an explicit trigger: the user asks for subagents or parallel agent work, or a narrower skill/plugin workflow instructs the agent to ask first and the user grants explicit permission.
- Built-in agents include `default`, `worker`, and `explorer`; project-scoped custom agents live under `.codex/agents/` when a repo intentionally owns that setup.
- Custom agents can set a role-local model. For bounded read-heavy discovery roles, `gpt-5.6-terra` is the current soft default because OpenAI positions it as the faster, lower-cost option for lighter subagent work. Use `gpt-5.6` for harder planning and reasoning, or leave the model unpinned when Codex should choose.
- Subagents are best for bounded read-heavy discovery, tests, triage, log analysis, and summarization.
- Write-heavy parallel work needs clear ownership because multiple agents editing code or docs at once can create conflicts and coordination overhead.

## What Skills Should Say

Only add subagent guidance to skills where the workflow has real parallelizable support work.

Good candidates:

- docs lookup and source verification skills
- repo-maintenance, metadata, or packaging audits
- broad codebase exploration or explanation skills
- test, log, or CI triage skills
- migration checks where each worker can own one independent surface

Weak candidates:

- narrow single-file apply skills
- skills whose primary job is one sequential command
- workflows where one output directly determines the next input
- skills that already have a tight write target with no independent discovery phase

## Required Wording Points

When a skill includes a `Codex Subagent Fit` section, it should say:

- subagents require an explicit trigger, either from the user's request or from narrower workflow guidance that tells the agent to request and receive permission before delegation
- the subagent jobs must be bounded and independently useful
- read-heavy discovery, triage, tests, docs pulling, and summarization are the default fit
- read-heavy custom-agent roles may pin `model = "gpt-5.6-terra"` locally, but generated repo guidance should not turn that into a global rule for every subagent
- workers should return concise evidence, findings, links, or file references instead of raw command logs
- apply-mode or implementation edits should stay in the main thread unless the user asks for parallel implementation and each worker has a disjoint write scope
- plugin-specific guidance can be stricter; for example, Codex Security repository-wide scans may require asking for subagent use because the scan quality depends on parallel file-pass review

## Review Checklist

When auditing a skills repo, flag guidance that:

- says or implies Codex will spawn subagents automatically
- tells agents to delegate merely because a task is complex or lengthy, without a concrete workflow reason
- recommends parallel writes without separate file ownership
- hides token, latency, or coordination costs
- asks subagents to dump raw exploratory output instead of distilled results
- uses older generic `multi-agent` wording where current Codex docs use `subagent`

## Official References

- [OpenAI Codex Subagents](https://developers.openai.com/codex/subagents)
- [OpenAI Codex Subagent concepts](https://developers.openai.com/codex/concepts/subagents)
- [OpenAI Codex subagent model guidance](https://learn.chatgpt.com/docs/agent-configuration/subagents#choosing-models-and-reasoning)
