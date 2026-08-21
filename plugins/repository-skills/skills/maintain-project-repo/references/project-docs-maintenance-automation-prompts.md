# Project Docs Maintenance Automation Prompts

Use these prompts when scheduling or delegating the documentation phase owned by
`maintain-project-repo`.

## Check-Only Sweep

Run `maintain-project-repo --operation report-only` for the target repository.
Report the planned toolkit actions and audit README, CONTRIBUTING, AGENTS, and
ROADMAP in that order. Include owner-skill findings, cross-document
responsibility drift, and stale command evidence. Do not edit files, commit,
push, or open a pull request.

## Bounded Apply Sweep

Run `maintain-project-repo --operation refresh` after the operator approves the
repository refresh. Let each owner document workflow edit only its own target
file. Report remaining cross-document issues separately from fixes already
applied. Do not move content across files unless the operator explicitly
requested that cleanup.

## Subagent Discovery

When the repository is large, ask subagents for read-only findings before the main thread edits:

- one worker checks README and contributor docs for stale commands
- one worker checks AGENTS and nested guidance for routing or policy drift
- one worker checks ROADMAP and issue state for small-ticket candidates

Require file references and concise evidence from each worker. The main thread owns the final edits and validation.
