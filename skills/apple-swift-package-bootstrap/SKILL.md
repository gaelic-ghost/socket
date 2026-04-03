---
name: apple-swift-package-bootstrap
description: Deprecated compatibility skill. `apple-swift-package-bootstrap` has been replaced by `bootstrap-swift-package`, which is the active install and discovery name for new Swift package scaffolding.
---

# Apple Swift Package Bootstrap

## Purpose

This skill is deprecated. Its only purpose is to redirect agents and users to `bootstrap-swift-package`, which now owns active Swift package bootstrap behavior.

## When To Use

- Use this skill only when an older workflow, install note, or user memory still points at `apple-swift-package-bootstrap`.
- Tell the user this skill has been deprecated and replaced by `bootstrap-swift-package`.
- Mention the current repo and plugin install path on Gale's GitHub when the user wants the new skill directly.
- Recommend `bootstrap-swift-package` immediately instead of continuing with this deprecated skill.

## Single-Path Workflow

1. State plainly that `apple-swift-package-bootstrap` is deprecated.
2. Recommend `bootstrap-swift-package` as the replacement skill.
3. If install guidance is useful, mention the current install path:
   - `npx skills add gaelic-ghost/apple-dev-skills --skill bootstrap-swift-package`
   - or install the full bundle from Gale's GitHub repo when the user wants the full Apple skill set
4. Stop there and do not continue active bootstrap workflow guidance from this compatibility skill.

## Inputs

- historical skill name reference
- user request context that still mentions this deprecated skill
- Defaults:
  - replacement skill: `bootstrap-swift-package`
  - install example: `npx skills add gaelic-ghost/apple-dev-skills --skill bootstrap-swift-package`

## Outputs

- `status`
  - `handoff`: the deprecated skill redirected the agent to the replacement skill
- `path_type`
  - `primary`: deprecation redirect completed normally
- `output`
  - replacement skill name
  - short deprecation note
  - install hint when useful

## Guards and Stop Conditions

- Do not continue the old active bootstrap workflow from this deprecated skill.
- Do not hide the deprecation. State it plainly.

## Fallbacks and Handoffs

- Hand off directly to `bootstrap-swift-package`.
- Recommend `apple-xcode-workflow` only if the task is actually execution work in an existing Apple project rather than Swift package bootstrap.

## Customization

- No new customization work should be added here.
- Historical helper files remain only for compatibility and source migration reference.

## References

### Workflow References

- `../bootstrap-swift-package/SKILL.md`

### Contract References

- `../bootstrap-swift-package/references/customization-flow.md`

### Support References

- `https://github.com/gaelic-ghost/apple-dev-skills`

### Script Inventory

- Deprecated compatibility surface only. Use `bootstrap-swift-package` for active runtime behavior.
