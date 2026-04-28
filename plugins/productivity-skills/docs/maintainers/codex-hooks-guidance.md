# Codex Hooks Guidance

Use this document when a productivity skill needs to explain or audit OpenAI Codex Hooks without turning hooks into a default requirement for every repository.

This is a maintainer-focused translation of the official Codex Hooks docs for repository guidance, AGENTS maintenance, and local maintainer-tooling work.

## Official Model

Codex Hooks are a Codex extensibility framework. They run scripts at specific Codex lifecycle events so a repository, user, or managed environment can add checks, context, logging, or guardrails around a Codex session.

Hooks are behind a feature flag:

```toml
[features]
codex_hooks = true
```

Codex discovers hooks next to active config layers in either `hooks.json` or inline `[hooks]` tables in `config.toml`. The most common locations are:

- `~/.codex/hooks.json`
- `~/.codex/config.toml`
- `<repo>/.codex/hooks.json`
- `<repo>/.codex/config.toml`

Project-local hooks load only when the project `.codex/` layer is trusted.

## Events To Name Carefully

The current official Codex Hooks guide documents these main events:

- `SessionStart`: adds context when a session starts, resumes, or clears.
- `PreToolUse`: can inspect supported tool calls before they run.
- `PermissionRequest`: can allow, deny, or decline to decide on approval requests.
- `PostToolUse`: can inspect supported tool results after they run.
- `UserPromptSubmit`: can inspect the user prompt before it is sent.
- `Stop`: can tell Codex to continue after a turn stops.

Do not describe every event as a hard enforcement boundary. `PreToolUse` and `PostToolUse` are useful guardrails, but the docs state that they do not intercept every possible tool path today.

## Good Fits

Hooks guidance is useful when a repository needs to document or audit Codex runtime behavior such as:

- repo-local policy checks before selected shell, edit, or MCP tool calls
- approval-request policy for sensitive tools or permission escalations
- turn-end validation reminders or continuation prompts
- session-start context that points Codex at repo-local conventions
- prompt checks that prevent accidental secrets or sensitive data in user prompts
- logging or analytics that the repository or organization intentionally owns

## Poor Fits

Avoid recommending hooks when ordinary repo guidance, skills, or maintainer scripts are enough.

Poor fits include:

- replacing `AGENTS.md` with hook-generated instructions
- treating hooks as the only enforcement layer for destructive operations
- adding project-local hooks to untrusted or public repos without a clear review story
- duplicating git pre-commit behavior without explaining why Codex lifecycle timing matters
- using relative hook script paths that break when Codex starts from a subdirectory

## Skill Wording Pattern

Use wording like this in applicable skills:

```markdown
## Codex Hooks Fit

When a repository documents Codex Hooks, keep the guidance explicit: hooks require `features.codex_hooks = true`, project-local hooks load only from trusted `.codex/` layers, and hooks may live in `hooks.json` or inline `[hooks]` config.

Good hook guidance names the lifecycle event, the matcher scope, the script location, and the user-visible effect. Do not present hooks as a replacement for AGENTS.md, normal approval policy, tests, or git hooks.
```

## Review Checklist

When auditing hooks guidance, flag wording that:

- omits the `features.codex_hooks` feature flag
- implies project-local hooks load in untrusted projects
- says higher-precedence config layers replace lower-precedence hooks
- treats `PreToolUse` or `PostToolUse` as complete enforcement for all tool paths
- confuses Codex Hooks with git pre-commit hooks or repo-maintenance hook scripts
- uses relative repo-local script paths instead of resolving from the git root or another stable absolute path
- leaves hook behavior vague instead of naming the event, matcher, and expected effect

## Official References

- [OpenAI Codex Hooks](https://developers.openai.com/codex/hooks)
- [OpenAI Codex Configuration Reference](https://developers.openai.com/codex/config-reference)
