# Agent Reports

Use this directory for report artifacts written by repo-local agents and
maintainer automation.

Reports in this directory should be reviewable Markdown artifacts. They may
record audit results, proposed documentation synchronization work, validation
notes, or other maintainer findings. They should not be treated as the source of
truth for repository policy; durable decisions belong in the relevant root docs,
maintainer docs, child `AGENTS.md`, roadmap, scripts, or marketplace metadata.

Guidelines:

- Keep reports concise and dated or clearly named when they are meant to persist.
- Do not include secrets, tokens, private environment values, or raw logs with
  sensitive local paths unless the report is intentionally private and ignored.
- Prefer proposed actions plus evidence over long transcripts.
- Link to repo-relative files instead of machine-local absolute paths.
- Remove or archive stale reports once their durable conclusions move into the
  owning docs.

## Check-Only Skill Surface Audit

Use the root skill-surface audit when a maintainer or Codex automation needs a
fresh token-efficiency and drift snapshot without editing skills:

```bash
uv run scripts/audit_skill_surfaces.py \
  --top 10 \
  --output docs/agents/skill-surface-audit.md
```

Treat the generated report as review material. Move durable conclusions into the
owning roadmap, maintainer docs, validation scripts, or skill sources before
considering the report resolved.
