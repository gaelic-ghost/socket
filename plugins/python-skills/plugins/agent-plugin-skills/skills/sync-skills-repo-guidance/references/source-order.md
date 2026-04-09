# Source Order

Use this order when reconciling a skills repository:

1. Canonical authored skill content under `skills/`
2. skill-local metadata such as `agents/openai.yaml`
3. repo maintainer docs and `AGENTS.md`
4. plugin and marketplace metadata under `plugins/` and `.agents/plugins/`
5. upstream standards and official docs for drift detection

If local repo docs and local implementation disagree, fix the repo first.

If local repo policy and upstream docs disagree, surface the conflict explicitly instead of silently picking one.
