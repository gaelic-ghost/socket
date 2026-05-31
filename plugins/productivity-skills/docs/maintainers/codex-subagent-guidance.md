# Codex Subagent Guidance

Use this document when a productivity skill needs to explain when Codex subagents are helpful without turning delegation into the default path.

This is a maintainer-focused translation of the official Codex subagent docs for this repository's documentation, maintenance, and explanation skills.

## Official Model

OpenAI's Codex docs use the term `subagent` for a delegated agent Codex starts
to handle a specific task. A `subagent workflow` is a workflow where Codex runs
parallel agents and combines their results.

Current Codex releases enable subagent workflows by default. Codex only spawns
subagents when there is an explicit trigger: the user asks for subagents or
parallel agent work, or a narrower skill/plugin workflow tells the agent to ask
first and the user grants explicit permission. Do not write skill guidance that
implies subagents start automatically just because a skill is active.

Codex ships built-in `default`, `worker`, and `explorer` agents. Custom agents
live in `~/.codex/agents/` for personal agents or `.codex/agents/` for
project-scoped agents, with global limits under `[agents]` in Codex config. A
standalone custom agent file currently requires `name`, `description`, and
`developer_instructions`, and can include supported `config.toml` keys such as
model, sandbox, MCP server, and skill configuration.

Subagents inherit the parent run's sandbox policy. In interactive sessions,
approval requests can surface from inactive agent threads. In non-interactive
flows, or when a fresh approval cannot be surfaced, an action that needs new
approval fails and Codex returns that failure to the parent workflow.

Treat subagents as in-run parallel workers. They are not a replacement for
Codex app automations, `codex exec`, repo-local validation, or a durable
external scheduler.

## Good Fits

Subagents are useful when the work can be split into bounded, mostly independent read-heavy tasks and returned as concise summaries.

Good fits in this repository include:

- documentation source gathering before a maintainer skill edits one target file
- broad repo scans where each worker owns a separate document family or directory
- code-slice exploration where one worker maps call sites while another reads tests or docs
- maintenance audits where one worker checks commands, another checks docs structure, and another checks package or plugin metadata
- review triage where workers return findings with file references instead of raw logs
- CSV-style fan-out where each row is a similar read-heavy audit target and each worker returns one structured result

## Poor Fits

Avoid recommending subagents when the work is small, sequential, or primarily one write target.

Poor fits include:

- single-file formatting or template normalization
- one focused README, AGENTS, ROADMAP, CONTRIBUTING, ACCESSIBILITY, or API apply pass
- write-heavy parallel edits to the same files or same tightly coupled document set
- tasks where the main agent needs each result immediately before it can choose the next step
- prompts where neither the user nor applicable workflow guidance explicitly calls for subagents, delegation, or parallel agent work
- background scheduling, retries, cross-run state, or queue ownership

## Skill Wording Pattern

Use wording like this in applicable skills:

```markdown
## Codex Subagent Fit

When the user explicitly requests subagents, or applicable workflow guidance tells the agent to ask and the user grants explicit permission, this skill can split read-heavy discovery into bounded subagent tasks and keep the main thread focused on decisions and final edits.

Good subagent jobs for this skill:

- inspect source docs and return concise evidence with links
- audit separate document families or directories
- compare current guidance against one upstream source per worker

Keep apply-mode edits in the main thread unless the user explicitly asks for parallel implementation and each worker has a disjoint write scope.
```

The important parts are:

- name the explicit trigger for delegation, whether it came directly from the user or from narrower workflow guidance that tells the agent to ask and receive permission before use
- limit subagents to bounded jobs
- prefer read-heavy discovery, triage, tests, and summarization
- ask workers for summaries, findings, and file references instead of raw intermediate output
- keep write ownership clear when parallel edits are intentionally requested
- name sandbox and approval behavior when a skill suggests non-interactive subagent use

## Official References

- [OpenAI Codex Subagents](https://developers.openai.com/codex/subagents)
- [OpenAI Codex Subagent concepts](https://developers.openai.com/codex/concepts/subagents)
- [OpenAI Codex Configuration Reference](https://developers.openai.com/codex/config-reference)
