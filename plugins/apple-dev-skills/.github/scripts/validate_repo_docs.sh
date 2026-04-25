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
  grep -Fq -- "$needle" "$file" || fail "Missing required string in $file: $needle"
}

require_not_contains() {
  local file="$1"
  local needle="$2"
  ! grep -Fq -- "$needle" "$file" || fail "Unexpected stale string in $file: $needle"
}

echo "Validating roadmap presence..."
[[ -f ROADMAP.md ]] || fail "Missing ROADMAP.md at repo root."

echo "Validating root docs presence..."
[[ -f README.md ]] || fail "Missing README.md at repo root."
[[ -f CONTRIBUTING.md ]] || fail "Missing CONTRIBUTING.md at repo root."
[[ -f AGENTS.md ]] || fail "Missing AGENTS.md at repo root."
[[ -f docs/maintainers/workflow-atlas.md ]] || fail "Missing docs/maintainers/workflow-atlas.md."
[[ -f docs/maintainers/reality-audit.md ]] || fail "Missing docs/maintainers/reality-audit.md."
[[ -f docs/maintainers/customization-consolidation-review.md ]] || fail "Missing docs/maintainers/customization-consolidation-review.md."
[[ -f docs/maintainers/execution-split-and-inference-plan.md ]] || fail "Missing docs/maintainers/execution-split-and-inference-plan.md."

echo "Validating local discovery mirrors..."
[[ -L ".agents/skills" ]] || fail "Expected .agents/skills to be a symlink to ../skills"
[[ "$(readlink .agents/skills)" == "../skills" ]] || fail "Expected .agents/skills -> ../skills"
[[ -L ".claude/skills" ]] || fail "Expected .claude/skills to be a symlink to ../skills"
[[ "$(readlink .claude/skills)" == "../skills" ]] || fail "Expected .claude/skills -> ../skills"
[[ ! -e "plugins/apple-dev-skills" ]] || fail "Did not expect a nested plugins/apple-dev-skills tree."

echo "Validating root README contract..."
require_contains "README.md" 'Treat `productivity-skills` as the default baseline layer for general repo-doc and maintenance work'
require_contains "README.md" 'This repository is the canonical source of truth for Gale'"'"'s Apple, Swift, and Xcode workflow skills.'
require_contains "README.md" 'Treat root [`skills/`](./skills/) as the canonical authored surface.'
require_contains "README.md" 'Keep shared reusable assets in [`shared/`](./shared/)'
require_contains "README.md" 'Run the repository test suite for skill and metadata changes:'
require_contains "README.md" 'Use [`CONTRIBUTING.md`](./CONTRIBUTING.md) for maintainer workflow details'
require_not_contains "README.md" 'plugins/apple-dev-skills/'
require_not_contains "README.md" 'install-plugin-to-socket'

echo "Validating CONTRIBUTING contract..."
require_contains "CONTRIBUTING.md" 'Use this guide when preparing changes so the repository stays understandable, testable, and truthful about the Apple workflow surface it actually ships.'
require_contains "CONTRIBUTING.md" '## Contribution Workflow'
require_contains "CONTRIBUTING.md" '## Local Setup'
require_contains "CONTRIBUTING.md" '## Development Expectations'
require_contains "CONTRIBUTING.md" 'bash .github/scripts/validate_repo_docs.sh'
require_contains "CONTRIBUTING.md" 'uv run pytest'

echo "Validating AGENTS contract..."
require_contains "AGENTS.md" 'This repository is the canonical home for Gale'"'"'s Apple, Swift, and Xcode workflow skills.'
require_contains "AGENTS.md" 'Treat `productivity-skills` as the default baseline maintainer layer'
require_contains "AGENTS.md" 'Root `skills/` is the canonical authored and exported surface.'
require_contains "AGENTS.md" 'Keep shared reusable assets in [`shared/`](./shared/) and maintainer tests in [`tests/`](./tests/).'
require_contains "AGENTS.md" 'require reading the relevant Apple documentation before proposing implementation changes.'
require_contains "AGENTS.md" 'Keep `explore-apple-swift-docs` as the canonical docs-routing surface'
require_not_contains "AGENTS.md" 'plugins/apple-dev-skills/'

echo "Validating workflow document structure..."
workflow_doc="docs/maintainers/workflow-atlas.md"
require_contains "$workflow_doc" "## Repo Workflow Map"
require_contains "$workflow_doc" '## `xcode-app-project-workflow`'
require_contains "$workflow_doc" '## `xcode-build-run-workflow`'
require_contains "$workflow_doc" '## `xcode-testing-workflow`'
require_contains "$workflow_doc" '## `swift-package-build-run-workflow`'
require_contains "$workflow_doc" '## `swift-package-testing-workflow`'
require_contains "$workflow_doc" '## `explore-apple-swift-docs`'
require_contains "$workflow_doc" '## `author-swift-docc-docs`'
require_contains "$workflow_doc" '## `swiftui-app-architecture-workflow`'
require_contains "$workflow_doc" '## `apple-ui-accessibility-workflow`'
require_contains "$workflow_doc" '## `format-swift-sources`'
require_contains "$workflow_doc" '## `structure-swift-sources`'
require_contains "$workflow_doc" '## `bootstrap-swift-package`'
require_contains "$workflow_doc" '## `bootstrap-xcode-app-project`'
require_contains "$workflow_doc" '## `sync-xcode-project-guidance`'
require_contains "$workflow_doc" '## `sync-swift-package-guidance`'
require_contains "$workflow_doc" '## `swift-package-workflow`'
require_contains "$workflow_doc" 'Direct docs access is the primary `explore` path'

echo "Validating reality audit guide..."
audit_doc="docs/maintainers/reality-audit.md"
require_contains "$audit_doc" "## Source-of-Truth Order"
require_contains "$audit_doc" "## Audit Procedure"
require_contains "$audit_doc" "## Local Discovery Smoke Test Flow"
require_contains "$audit_doc" "## Reporting Shape"
require_contains "$audit_doc" '`productivity-skills` owns the reusable `maintain-project-repo` toolkit contract'
require_contains "$audit_doc" 'this repository owns only the Apple-specific profile selection and Xcode MCP registration contract'
require_contains "$audit_doc" 'Historical milestone planning decisions that no longer need standalone docs should live in `ROADMAP.md`'
require_not_contains "$audit_doc" 'plugins/apple-dev-skills/'

echo "Validating customization consolidation review..."
customization_review_doc="docs/maintainers/customization-consolidation-review.md"
require_contains "$customization_review_doc" "## Current State Summary"
require_contains "$customization_review_doc" "## Decision"
require_contains "$customization_review_doc" "## Knob Classification"
require_contains "$customization_review_doc" "## Shared Helper Decision"
require_contains "$customization_review_doc" "## Follow-Up Plan"
require_contains "$customization_review_doc" "Milestone 20 concludes that the repo should shrink the customization surface rather than expand it."
require_contains "$customization_review_doc" "## Sync Skill Simplification Decision"
require_contains "$customization_review_doc" 'implemented replacement: `writeMode`'
execution_split_doc="docs/maintainers/execution-split-and-inference-plan.md"
require_contains "$execution_split_doc" "## Target Skill Matrix"
require_contains "$execution_split_doc" "## Guidance Preservation Contract"
require_contains "$execution_split_doc" "## AGENTS Expansion Strategy"
require_contains "$execution_split_doc" "## Repo-Maintenance Direction"
require_contains "$execution_split_doc" "## Implementation Plan"
require_contains "$execution_split_doc" '`productivity-skills/maintain-project-repo` as the canonical shipped repo-maintenance surface'
require_contains "ROADMAP.md" "Completed Milestones 22 and 23"
require_contains "ROADMAP.md" 'See `docs/maintainers/customization-consolidation-review.md`.'
require_contains "ROADMAP.md" "Completed Milestones 30 through 36"
require_contains "ROADMAP.md" "shrinking the customization surface"
require_contains "ROADMAP.md" "splitting execution workflows"
require_contains "ROADMAP.md" "preserving guidance through the refactor"

echo "Validating skill directory layout..."
active_skill_mds=(
  "./skills/xcode-app-project-workflow/SKILL.md"
  "./skills/xcode-build-run-workflow/SKILL.md"
  "./skills/xcode-testing-workflow/SKILL.md"
  "./skills/swift-package-build-run-workflow/SKILL.md"
  "./skills/swift-package-testing-workflow/SKILL.md"
  "./skills/swift-package-workflow/SKILL.md"
  "./skills/author-swift-docc-docs/SKILL.md"
  "./skills/swiftui-app-architecture-workflow/SKILL.md"
  "./skills/apple-ui-accessibility-workflow/SKILL.md"
  "./skills/explore-apple-swift-docs/SKILL.md"
  "./skills/format-swift-sources/SKILL.md"
  "./skills/structure-swift-sources/SKILL.md"
  "./skills/bootstrap-swift-package/SKILL.md"
  "./skills/bootstrap-xcode-app-project/SKILL.md"
  "./skills/sync-xcode-project-guidance/SKILL.md"
  "./skills/sync-swift-package-guidance/SKILL.md"
)
[[ ${#active_skill_mds[@]} -eq 16 ]] || fail "Expected exactly 16 active skills, found ${#active_skill_mds[@]}."

shared_xcode_snippet="./shared/agents-snippets/apple-xcode-project-core.md"
shared_package_snippet="./shared/agents-snippets/apple-swift-package-core.md"
[[ -f "$shared_xcode_snippet" ]] || fail "Missing shared snippet: $shared_xcode_snippet"
[[ -f "$shared_package_snippet" ]] || fail "Missing shared snippet: $shared_package_snippet"

for skill_md in "${active_skill_mds[@]}"; do
  skill_dir="${skill_md%/SKILL.md}"
  [[ -f "$skill_dir/agents/openai.yaml" ]] || fail "Missing $skill_dir/agents/openai.yaml"
  [[ -d "$skill_dir/references" ]] || fail "Missing $skill_dir/references/"

  case "$skill_dir" in
    ./skills/structure-swift-sources)
      ;;
    *)
      [[ -f "$skill_dir/references/customization.template.yaml" ]] || fail "Missing $skill_dir/references/customization.template.yaml"
      [[ -f "$skill_dir/references/customization-flow.md" ]] || fail "Missing $skill_dir/references/customization-flow.md"
      [[ -f "$skill_dir/scripts/customization_config.py" ]] || fail "Missing $skill_dir/scripts/customization_config.py"
      ;;
  esac

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
    ./skills/bootstrap-swift-package|./skills/sync-swift-package-guidance|./skills/swift-package-workflow|./skills/swift-package-build-run-workflow|./skills/swift-package-testing-workflow)
      local_snippet="$skill_dir/references/snippets/apple-swift-package-core.md"
      shared_snippet="$shared_package_snippet"
      snippet_ref='references/snippets/apple-swift-package-core.md'
      ;;
    ./skills/structure-swift-sources|./skills/author-swift-docc-docs)
      local_snippet=""
      shared_snippet=""
      snippet_ref=""
      ;;
    *)
      local_snippet="$skill_dir/references/snippets/apple-xcode-project-core.md"
      shared_snippet="$shared_xcode_snippet"
      snippet_ref='references/snippets/apple-xcode-project-core.md'
      ;;
  esac

  if [[ -n "$local_snippet" ]]; then
    [[ -f "$local_snippet" ]] || fail "Missing $local_snippet"
    cmp -s "$shared_snippet" "$local_snippet" || fail "Snippet drift detected between $shared_snippet and $local_snippet"

    grep -Fq "$snippet_ref" "$skill_md" || fail "Missing local snippet reference in $skill_md"
    grep -Eiq "recommend.{0,120}$snippet_ref|$snippet_ref.{0,120}recommend" "$skill_md" || fail "Missing snippet recommendation guidance in $skill_md"
  fi
done

echo "Validating Dash docs exploration references..."
dash_skill_dir="./skills/explore-apple-swift-docs"
[[ -f "$dash_skill_dir/references/dash_call_library.md" ]] || fail "Missing $dash_skill_dir/references/dash_call_library.md"
require_contains "$dash_skill_dir/SKILL.md" 'Prefer direct docs access methods in this order: Xcode MCP docs first, Dash MCP second, Dash localhost HTTP third, and official web docs last.'
require_contains "$dash_skill_dir/SKILL.md" 'Do not present `scripts/run_workflow.py` as the required first step'
require_contains "$dash_skill_dir/references/dash_call_library.md" '## Dash MCP Examples'
require_contains "$dash_skill_dir/references/dash_call_library.md" '## Dash Local HTTP Examples'
require_contains "$dash_skill_dir/references/dash_call_library.md" '## High-Value Docset Targets'

echo "Validating stale installer and nested-packaging guidance is gone..."
for file in \
  "skills/swift-package-workflow/SKILL.md" \
  "skills/swift-package-testing-workflow/SKILL.md" \
  "skills/swift-package-build-run-workflow/SKILL.md" \
  "skills/xcode-app-project-workflow/SKILL.md" \
  "skills/xcode-testing-workflow/SKILL.md" \
  "skills/xcode-build-run-workflow/SKILL.md" \
  "skills/author-swift-docc-docs/SKILL.md" \
  "skills/swiftui-app-architecture-workflow/SKILL.md" \
  "skills/sync-swift-package-guidance/SKILL.md" \
  "skills/sync-xcode-project-guidance/SKILL.md" \
  "docs/maintainers/workflow-atlas.md" \
  "ROADMAP.md"
do
  require_not_contains "$file" 'install-plugin-to-socket'
  require_not_contains "$file" 'plugins/apple-dev-skills/'
done

echo "Validating maintain-project-repo delegation..."
[[ ! -e "./shared/repo-maintenance-toolkit" ]] || fail "Did not expect apple-dev-skills to retain shared/repo-maintenance-toolkit."
for skill_dir in \
  "./skills/bootstrap-swift-package" \
  "./skills/bootstrap-xcode-app-project" \
  "./skills/sync-swift-package-guidance" \
  "./skills/sync-xcode-project-guidance"
do
  [[ ! -e "$skill_dir/scripts/install_repo_maintenance_toolkit.py" ]] || fail "Did not expect legacy toolkit installer in $skill_dir"
  [[ ! -e "$skill_dir/assets/repo-maintenance" ]] || fail "Did not expect vendored repo-maintenance assets in $skill_dir"
  [[ ! -e "$skill_dir/assets/github/repo-maintenance-workflows" ]] || fail "Did not expect vendored repo-maintenance workflow assets in $skill_dir"
  require_contains "$skill_dir/SKILL.md" 'maintain-project-repo'
done
require_contains "./skills/bootstrap-swift-package/scripts/bootstrap_swift_package.sh" 'productivity-skills/skills/maintain-project-repo/scripts/run_workflow.py'
require_contains "./skills/bootstrap-xcode-app-project/scripts/bootstrap_xcode_app_project.py" 'productivity-skills" / "skills" / "maintain-project-repo" / "scripts" / "run_workflow.py'
require_contains "./skills/sync-swift-package-guidance/scripts/sync_swift_package_guidance.py" 'productivity-skills" / "skills" / "maintain-project-repo" / "scripts" / "run_workflow.py'
require_contains "./skills/sync-xcode-project-guidance/scripts/sync_xcode_project_guidance.py" 'productivity-skills" / "skills" / "maintain-project-repo" / "scripts" / "run_workflow.py'

echo "Validating preserved guidance in AGENTS assets..."
package_agents_assets=(
  "./skills/bootstrap-swift-package/assets/AGENTS.md"
  "./skills/sync-swift-package-guidance/assets/AGENTS.md"
)
for agents_asset in "${package_agents_assets[@]}"; do
  require_contains "$agents_asset" 'Use `swift-package-build-run-workflow`'
  require_contains "$agents_asset" 'Use `swift-package-testing-workflow`'
  require_contains "$agents_asset" 'scripts/repo-maintenance/config/profile.env'
  require_contains "$agents_asset" '.swiftformat'
  require_contains "$agents_asset" 'scripts/repo-maintenance/hooks/pre-commit.sample'
  require_contains "$agents_asset" 'swiftformat --lint'
  require_contains "$agents_asset" 'Resource.process(...)'
  require_contains "$agents_asset" 'Resource.copy(...)'
  require_contains "$agents_asset" 'Resource.embedInCode(...)'
  require_contains "$agents_asset" 'Bundle.module'
  require_contains "$agents_asset" '.metallib'
  require_contains "$agents_asset" '.xctestplan'
  require_contains "$agents_asset" 'Debug and Release'
  require_contains "$agents_asset" 'sync-swift-package-guidance'
done

xcode_agents_assets=(
  "./skills/bootstrap-xcode-app-project/assets/AGENTS.md"
  "./skills/sync-xcode-project-guidance/assets/AGENTS.md"
)
for agents_asset in "${xcode_agents_assets[@]}"; do
  require_contains "$agents_asset" 'Use `xcode-build-run-workflow`'
  require_contains "$agents_asset" 'Use `xcode-testing-workflow`'
  require_contains "$agents_asset" 'scripts/repo-maintenance/config/profile.env'
  require_contains "$agents_asset" '.swiftformat'
  require_contains "$agents_asset" 'scripts/repo-maintenance/hooks/pre-commit.sample'
  require_contains "$agents_asset" 'swiftformat --lint'
  require_contains "$agents_asset" '.xctestplan'
  require_contains "$agents_asset" 'project membership, target membership, build phases, and resource inclusion'
  require_contains "$agents_asset" 'Debug and Release'
  require_contains "$agents_asset" 'Never edit `.pbxproj` files directly.'
  require_contains "$agents_asset" 'sync-xcode-project-guidance'
done

echo "Validating skill-creator contract..."
uv run python .github/scripts/validate_skill_creator_contract.py >/dev/null

echo "Validating workflow document content..."
grep -q '```mermaid' "$workflow_doc" || fail "$workflow_doc must contain Mermaid diagrams."
grep -q 'Agent ↔ User UX' "$workflow_doc" || fail "$workflow_doc must describe Agent ↔ User UX."
grep -q 'Failure / Fallback / Handoff States' "$workflow_doc" || fail "$workflow_doc must describe failure, fallback, and handoff states."
! grep -q 'apple-skills-router' "$workflow_doc" || fail "$workflow_doc must not mention apple-skills-router."

echo "All validation checks passed."
