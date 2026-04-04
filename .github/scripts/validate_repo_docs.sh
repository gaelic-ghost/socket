#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT_DIR"

fail() {
  echo "ERROR: $*" >&2
  exit 1
}

require_contains() {
  local file="$1"
  local needle="$2"
  grep -Fq "$needle" "$file" || fail "Missing required string in $file: $needle"
}

echo "Validating roadmap presence..."
[[ -f ROADMAP.md ]] || fail "Missing ROADMAP.md at repo root."

echo "Validating root docs presence..."
[[ -f README.md ]] || fail "Missing README.md at repo root."
[[ -f AGENTS.md ]] || fail "Missing AGENTS.md at repo root."
[[ -f docs/maintainers/workflow-atlas.md ]] || fail "Missing docs/maintainers/workflow-atlas.md."
[[ -f docs/maintainers/reality-audit.md ]] || fail "Missing docs/maintainers/reality-audit.md."

echo "Validating local discovery mirrors..."
[[ -L ".agents/skills" ]] || fail "Expected .agents/skills to be a symlink to ../skills"
[[ "$(readlink .agents/skills)" == "../skills" ]] || fail "Expected .agents/skills -> ../skills"
[[ -L ".claude/skills" ]] || fail "Expected .claude/skills to be a symlink to ../skills"
[[ "$(readlink .claude/skills)" == "../skills" ]] || fail "Expected .claude/skills -> ../skills"
[[ -L "plugins/apple-dev-skills/skills" ]] || fail "Expected plugins/apple-dev-skills/skills to be a symlink to ../../skills"
[[ "$(readlink plugins/apple-dev-skills/skills)" == "../../skills" ]] || fail "Expected plugins/apple-dev-skills/skills -> ../../skills"

echo "Validating authoritative resource links in root docs..."
required_resource_strings=(
  "/Users/galew/.codex/skills/.system/skill-creator/SKILL.md"
  "https://developers.openai.com/codex/skills"
  "https://developers.openai.com/codex/mcp/"
  "openaiDeveloperDocs"
  "\$openai-docs"
  "https://code.claude.com/docs/en/features-overview"
  "https://code.claude.com/docs/en/skills"
  "https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices"
  "https://code.claude.com/docs/en/plugins"
  "https://agentskills.io/home"
  "https://vercel.com/kb/guide/agent-skills-creating-installing-and-sharing-reusable-agent-context"
)
for needle in "${required_resource_strings[@]}"; do
  require_contains "AGENTS.md" "$needle"
done

echo "Validating README maintainer pointer..."
require_contains "README.md" 'Maintainers: authoritative skill-authoring resources live in `AGENTS.md`.'
require_contains "README.md" 'docs/maintainers/workflow-atlas.md'
require_contains "README.md" 'docs/maintainers/reality-audit.md'
require_contains "README.md" '.agents/skills -> ../skills'
require_contains "README.md" '.claude/skills -> ../skills'
require_contains "README.md" 'plugins/apple-dev-skills/skills -> ../../skills'

echo "Validating AGENTS maintainer pointers..."
require_contains "AGENTS.md" 'docs/maintainers/reality-audit.md'
require_contains "AGENTS.md" 'docs/maintainers/workflow-atlas.md'
require_contains "AGENTS.md" '.agents/skills -> ../skills'
require_contains "AGENTS.md" '.claude/skills -> ../skills'
require_contains "AGENTS.md" 'plugins/apple-dev-skills/skills -> ../../skills'

echo "Validating plugin and marketplace metadata..."
require_contains "plugins/apple-dev-skills/.codex-plugin/plugin.json" '"skills": "./skills/"'
require_contains ".agents/plugins/marketplace.json" '"installation": "AVAILABLE"'

echo "Validating workflow document structure..."
workflow_doc="docs/maintainers/workflow-atlas.md"
require_contains "$workflow_doc" "## Repo Workflow Map"
require_contains "$workflow_doc" '## `xcode-app-project-workflow`'
require_contains "$workflow_doc" '## `explore-apple-swift-docs`'
require_contains "$workflow_doc" '## `swift-style-tooling-workflow`'
require_contains "$workflow_doc" '## `bootstrap-swift-package`'
require_contains "$workflow_doc" '## `bootstrap-xcode-app-project`'
require_contains "$workflow_doc" '## `sync-xcode-project-guidance`'
require_contains "$workflow_doc" '## `sync-swift-package-guidance`'

echo "Validating reality audit guide..."
audit_doc="docs/maintainers/reality-audit.md"
require_contains "$audit_doc" "## Source-of-Truth Order"
require_contains "$audit_doc" "## Audit Procedure"
require_contains "$audit_doc" "## Reporting Shape"

echo "Validating skill directory layout..."
active_skill_mds=(
  "./skills/xcode-app-project-workflow/SKILL.md"
  "./skills/explore-apple-swift-docs/SKILL.md"
  "./skills/swift-style-tooling-workflow/SKILL.md"
  "./skills/bootstrap-swift-package/SKILL.md"
  "./skills/bootstrap-xcode-app-project/SKILL.md"
  "./skills/sync-xcode-project-guidance/SKILL.md"
  "./skills/sync-swift-package-guidance/SKILL.md"
)
[[ ${#active_skill_mds[@]} -eq 7 ]] || fail "Expected exactly 7 active skills, found ${#active_skill_mds[@]}."

shared_xcode_snippet="./shared/agents-snippets/apple-xcode-project-core.md"
shared_package_snippet="./shared/agents-snippets/apple-swift-package-core.md"
[[ -f "$shared_xcode_snippet" ]] || fail "Missing shared snippet: $shared_xcode_snippet"
[[ -f "$shared_package_snippet" ]] || fail "Missing shared snippet: $shared_package_snippet"

for skill_md in "${active_skill_mds[@]}"; do
  skill_dir="${skill_md%/SKILL.md}"
  [[ -f "$skill_dir/agents/openai.yaml" ]] || fail "Missing $skill_dir/agents/openai.yaml"
  [[ -f "$skill_dir/references/customization.template.yaml" ]] || fail "Missing $skill_dir/references/customization.template.yaml"
  [[ -f "$skill_dir/references/customization-flow.md" ]] || fail "Missing $skill_dir/references/customization-flow.md"
  [[ -f "$skill_dir/scripts/customization_config.py" ]] || fail "Missing $skill_dir/scripts/customization_config.py"
  [[ -d "$skill_dir/references" ]] || fail "Missing $skill_dir/references/"

  for heading in \
    "^## Purpose$" \
    "^## When To Use$" \
    "^## Single-Path Workflow$" \
    "^## Inputs$" \
    "^## Outputs$" \
    "^## Guards and Stop Conditions$" \
    "^## Fallbacks and Handoffs$" \
    "^## Customization$" \
    "^## References$"
  do
    grep -q "$heading" "$skill_md" || fail "Missing required heading in $skill_md: ${heading#^}"
  done

  # Some skills are policy-only and intentionally do not ship scripts.
  if grep -q "scripts/" "$skill_md"; then
    [[ -d "$skill_dir/scripts" ]] || fail "Missing $skill_dir/scripts/ (referenced by $skill_md)"
  fi

  case "$skill_dir" in
    ./skills/bootstrap-swift-package|./skills/sync-swift-package-guidance)
      local_snippet="$skill_dir/references/snippets/apple-swift-package-core.md"
      shared_snippet="$shared_package_snippet"
      snippet_ref='references/snippets/apple-swift-package-core.md'
      ;;
    *)
      local_snippet="$skill_dir/references/snippets/apple-xcode-project-core.md"
      shared_snippet="$shared_xcode_snippet"
      snippet_ref='references/snippets/apple-xcode-project-core.md'
      ;;
  esac

  [[ -f "$local_snippet" ]] || fail "Missing $local_snippet"
  cmp -s "$shared_snippet" "$local_snippet" || fail "Snippet drift detected between $shared_snippet and $local_snippet"

  grep -Fq "$snippet_ref" "$skill_md" || fail "Missing local snippet reference in $skill_md"
  grep -Eiq "recommend.{0,120}$snippet_ref|$snippet_ref.{0,120}recommend" "$skill_md" || fail "Missing snippet recommendation guidance in $skill_md"
done

echo "Validating skill-creator contract..."
uv run python .github/scripts/validate_skill_creator_contract.py >/dev/null

echo "Validating workflow document content..."
grep -q '```mermaid' "$workflow_doc" || fail "$workflow_doc must contain Mermaid diagrams."
grep -q 'Agent ↔ User UX' "$workflow_doc" || fail "$workflow_doc must describe Agent ↔ User UX."
grep -q 'Failure / Fallback / Handoff States' "$workflow_doc" || fail "$workflow_doc must describe failure, fallback, and handoff states."
! grep -q 'apple-skills-router' "$workflow_doc" || fail "$workflow_doc must not mention apple-skills-router."

echo "All validation checks passed."
