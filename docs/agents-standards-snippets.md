# AGENTS Standards Snippets

Use these snippets as copy/paste starting points for repository-level `AGENTS.md` files.

## Python Execution Baseline

```markdown
- Use `uv run` for Python commands (`uv run python`, `uv run pytest`, `uv run ruff check`, `uv run mypy`) unless project docs explicitly require otherwise.
```

## Safety Defaults

```markdown
- Never auto-commit changes.
- Never auto-install dependencies or tools without explicit user confirmation.
- Keep edits bounded to the requested scope.
- When blocked, report the exact blocker and the next required user action.
```

## Config Precedence Template

```markdown
Configuration precedence:
1. CLI flags
2. `config/customization.yaml`
3. `config/customization.template.yaml`
4. tool/script defaults
```

## Output Contract Template

```markdown
- Provide a short human-readable summary.
- Provide machine-readable JSON output when the workflow supports it.
- Include touched files, unresolved issues, and explicit error details.
```

## Relative Date Normalization Template

```markdown
- Resolve relative date terms (`today`, `tomorrow`, `next Monday`) against current local date/time first.
- Confirm scheduled dates in absolute form with timezone in user-visible output.
```
