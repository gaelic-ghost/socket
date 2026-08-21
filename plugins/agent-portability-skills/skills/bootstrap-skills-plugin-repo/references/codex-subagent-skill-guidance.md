# Codex Subagent Skill Guidance

Use this reference when bootstrapping or auditing guidance about Codex subagents
in skills-export and plugin-export repositories. It does not replace OpenAI's
Codex documentation; it records the narrow Socket house pattern for optional
subagent guidance.

Date checked: 2026-07-19.

## Official Model

- Codex calls delegated agents `subagents` and their coordinated use a
  `subagent workflow`.
- Subagent workflows require an explicit trigger: the user asks for subagents
  or parallel work, or narrower workflow guidance asks first and the user grants
  permission.
- Built-in roles include `default`, `worker`, and `explorer`. Project-scoped
  custom roles belong under `.codex/agents/` only when the repository
  intentionally owns that configuration.
- Bounded read-heavy discovery, tests, triage, log analysis, documentation
  lookup, and summarization are the normal fit.
- Parallel writes require disjoint ownership because shared edits create merge
  conflicts and coordination overhead.

## What Skills Should Say

Add a `Codex Subagent Fit` section only when the workflow has independently
useful support work. Good candidates include documentation verification,
metadata or packaging audits, broad codebase exploration, test or CI triage,
and migration checks with separate evidence surfaces.

Avoid subagent guidance for narrow single-file changes, one sequential command,
workflows where each output determines the next input, or tightly bounded write
targets with no independent discovery phase.

When subagent guidance is present, require:

- bounded, independently useful jobs;
- concise findings, evidence, links, or file references instead of raw logs;
- main-thread ownership of apply-mode edits unless the user explicitly requests
  parallel implementation with disjoint write scopes;
- local model choices only when a repository intentionally owns them, without
  turning one role's choice into a global rule; and
- stricter plugin-specific policy when the owning workflow requires it.

## Review Checklist

Flag guidance that:

- implies Codex delegates automatically;
- recommends delegation merely because work is long or complex;
- recommends parallel writes without separate ownership;
- hides token, latency, or coordination costs;
- requests raw exploratory dumps instead of distilled findings; or
- uses vague `multi-agent` wording where current Codex documentation uses
  `subagent`.

## Official References

- [OpenAI Codex Subagents](https://developers.openai.com/codex/subagents)
- [OpenAI Codex Subagent concepts](https://developers.openai.com/codex/concepts/subagents)
- [OpenAI Codex subagent model guidance](https://learn.chatgpt.com/docs/agent-configuration/subagents#choosing-models-and-reasoning)
