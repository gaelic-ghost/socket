# Project Docs Maintenance Automation Prompts

Use these prompts when scheduling or delegating recurring documentation sweeps.

## Check-Only Sweep

Run `maintain-project-docs` in `check-only` mode for the target repository. Audit README, CONTRIBUTING, AGENTS, ACCESSIBILITY, and ROADMAP in that order. Report owner-skill findings, cross-document responsibility drift, stale command evidence, and any roadmap small-ticket candidates requested by the operator. Do not edit files, commit, push, or open a pull request.

## Bounded Apply Sweep

Run `maintain-project-docs` in `apply` mode only after the operator approves bounded file normalization. Let each owner document skill edit only its own target file. After apply, rerun the umbrella audit and report remaining cross-document issues separately from fixes already applied. Do not move content across files unless the operator explicitly requested that cleanup.

## Subagent Discovery

When the repository is large, ask subagents for read-only findings before the main thread edits:

- one worker checks README and contributor docs for stale commands
- one worker checks AGENTS and nested guidance for routing or policy drift
- one worker checks ROADMAP and issue state for small-ticket candidates

Require file references and concise evidence from each worker. The main thread owns the final edits and validation.
