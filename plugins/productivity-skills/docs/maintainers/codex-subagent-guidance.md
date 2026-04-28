# Codex Subagent Guidance

Use this document when a productivity skill needs to explain when Codex subagents are helpful without turning delegation into the default path.

This is a maintainer-focused translation of the official Codex subagent docs for this repository's documentation, maintenance, and explanation skills.

## Official Model

OpenAI's Codex docs use the term `subagent` for a delegated agent Codex starts to handle a specific task. A `subagent workflow` is a workflow where Codex runs parallel agents and combines their results.

Codex only spawns subagents when the user explicitly asks for subagents or parallel agent work. Do not write skill guidance that implies subagents start automatically just because a skill is active.

## Good Fits

Subagents are useful when the work can be split into bounded, mostly independent read-heavy tasks and returned as concise summaries.

Good fits in this repository include:

- documentation source gathering before a maintainer skill edits one target file
- broad repo scans where each worker owns a separate document family or directory
- code-slice exploration where one worker maps call sites while another reads tests or docs
- maintenance audits where one worker checks commands, another checks docs structure, and another checks package or plugin metadata
- review triage where workers return findings with file references instead of raw logs

## Poor Fits

Avoid recommending subagents when the work is small, sequential, or primarily one write target.

Poor fits include:

- single-file formatting or template normalization
- one focused README, AGENTS, ROADMAP, CONTRIBUTING, ACCESSIBILITY, or API apply pass
- write-heavy parallel edits to the same files or same tightly coupled document set
- tasks where the main agent needs each result immediately before it can choose the next step
- prompts where the user did not explicitly ask for subagents, delegation, or parallel agent work

## Skill Wording Pattern

Use wording like this in applicable skills:

```markdown
## Codex Subagent Fit

When the user explicitly asks for subagents or parallel agent work, this skill can split read-heavy discovery into bounded subagent tasks and keep the main thread focused on decisions and final edits.

Good subagent jobs for this skill:

- inspect source docs and return concise evidence with links
- audit separate document families or directories
- compare current guidance against one upstream source per worker

Keep apply-mode edits in the main thread unless the user explicitly asks for parallel implementation and each worker has a disjoint write scope.
```

The important parts are:

- name that the user must ask explicitly
- limit subagents to bounded jobs
- prefer read-heavy discovery, triage, tests, and summarization
- ask workers for summaries, findings, and file references instead of raw intermediate output
- keep write ownership clear when parallel edits are intentionally requested

## Official References

- [OpenAI Codex Subagents](https://developers.openai.com/codex/subagents)
- [OpenAI Codex Subagent concepts](https://developers.openai.com/codex/concepts/subagents)
