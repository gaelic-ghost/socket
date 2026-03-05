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
[[ -f WORKFLOWS.md ]] || fail "Missing WORKFLOWS.md at repo root."

echo "Validating authoritative resource links in root docs..."
required_resource_strings=(
  "/Users/galew/.codex/skills/.system/skill-creator/SKILL.md"
  "https://developers.openai.com/codex/skills/"
  "https://developers.openai.com/codex/mcp/"
  "openaiDeveloperDocs"
  "\$openai-docs"
  "https://docs.anthropic.com/en/docs/claude-code/sub-agents"
  "https://docs.anthropic.com/en/docs/claude-code/ide-integrations"
  "https://docs.anthropic.com/en/docs/claude-code/mcp"
  "https://agentskills.io/home"
  "https://vercel.com/kb/guide/agent-skills-creating-installing-and-sharing-reusable-agent-context"
)
for needle in "${required_resource_strings[@]}"; do
  require_contains "AGENTS.md" "$needle"
done

echo "Validating README maintainer pointer..."
require_contains "README.md" 'Maintainers: authoritative skill-authoring resources live in `AGENTS.md`.'
require_contains "README.md" 'WORKFLOWS.md'

echo "Validating workflow document structure..."
require_contains "WORKFLOWS.md" "## Repo Workflow Map"
require_contains "WORKFLOWS.md" '## `apple-xcode-workflow`'
require_contains "WORKFLOWS.md" '## `apple-dash-docsets`'
require_contains "WORKFLOWS.md" '## `apple-swift-package-bootstrap`'

echo "Validating skill directory layout..."
skill_mds=()
while IFS= read -r line; do
  skill_mds+=("$line")
done < <(find . -type f -name SKILL.md \
  -not -path "./.git/*" \
  -not -path "./.github/*" \
  | sort)
[[ ${#skill_mds[@]} -eq 3 ]] || fail "Expected exactly 3 active skills, found ${#skill_mds[@]}."

shared_snippet="./shared/agents-snippets/apple-swift-core.md"
[[ -f "$shared_snippet" ]] || fail "Missing shared snippet: $shared_snippet"

for skill_md in "${skill_mds[@]}"; do
  skill_dir="${skill_md%/SKILL.md}"
  [[ -f "$skill_dir/agents/openai.yaml" ]] || fail "Missing $skill_dir/agents/openai.yaml"
  [[ -f "$skill_dir/customization.template.yaml" ]] || fail "Missing $skill_dir/customization.template.yaml"
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

  local_snippet="$skill_dir/references/snippets/apple-swift-core.md"
  [[ -f "$local_snippet" ]] || fail "Missing $local_snippet"
  cmp -s "$shared_snippet" "$local_snippet" || fail "Snippet drift detected between $shared_snippet and $local_snippet"

  grep -Fq "references/snippets/apple-swift-core.md" "$skill_md" || fail "Missing local snippet reference in $skill_md"
  grep -Eiq "recommend.{0,120}references/snippets/apple-swift-core.md|references/snippets/apple-swift-core.md.{0,120}recommend" "$skill_md" || fail "Missing snippet recommendation guidance in $skill_md"
done

echo "Validating workflow document content..."
grep -q '```mermaid' WORKFLOWS.md || fail "WORKFLOWS.md must contain Mermaid diagrams."
grep -q 'Agent ↔ User UX' WORKFLOWS.md || fail "WORKFLOWS.md must describe Agent ↔ User UX."
grep -q 'Failure / Fallback / Handoff States' WORKFLOWS.md || fail "WORKFLOWS.md must describe failure, fallback, and handoff states."
! grep -q 'apple-skills-router' WORKFLOWS.md || fail "WORKFLOWS.md must not mention apple-skills-router."

echo "All validation checks passed."
