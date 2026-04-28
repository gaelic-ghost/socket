# Codex Subagent Skill Guidance

Use this document when `agent-plugin-skills` needs to bootstrap or audit guidance about Codex subagents in skills-export and plugin-export repositories.

This document does not replace OpenAI's Codex docs. It gives these maintainer skills a narrow house pattern for teaching optional subagent use without overstating what Codex does automatically.

## Official Model

OpenAI's Codex docs call this feature `subagents`.

- A `subagent` is a delegated agent that Codex starts to handle a specific task.
- A `subagent workflow` is a workflow where Codex runs parallel agents and combines their results.
- Codex only spawns subagents when the user explicitly asks for subagents or parallel agent work.
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

- subagents require an explicit user request
- the subagent jobs must be bounded and independently useful
- read-heavy discovery, triage, tests, docs pulling, and summarization are the default fit
- workers should return concise evidence, findings, links, or file references instead of raw command logs
- apply-mode or implementation edits should stay in the main thread unless the user asks for parallel implementation and each worker has a disjoint write scope

## Review Checklist

When auditing a skills repo, flag guidance that:

- says or implies Codex will spawn subagents automatically
- tells agents to delegate merely because a task is complex or lengthy
- recommends parallel writes without separate file ownership
- hides token, latency, or coordination costs
- asks subagents to dump raw exploratory output instead of distilled results
- uses older generic `multi-agent` wording where current Codex docs use `subagent`

## Official References

- [OpenAI Codex Subagents](https://developers.openai.com/codex/subagents)
- [OpenAI Codex Subagent concepts](https://developers.openai.com/codex/concepts/subagents)
