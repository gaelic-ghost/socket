# Customization Guide

## What To Customize First

- Workspace root (`settings.workspaceRoot`).
- Noise floor (`settings.minMb`).
- Staleness threshold (`settings.staleDays`).
- Result cap (`settings.maxFindings`).
- Directory/file pattern overrides.
- Severity scoring boundaries (`settings.severityCutoffs`).

## Personalization Points

- Workspace scope
  - Default: scans repositories under `~/Workspace`.
  - Why customize: users often keep repos elsewhere or want a narrower scan target.
  - Where to change: `settings.workspaceRoot`.
- Threshold tuning
  - Default: `minMb=50`, `staleDays=90`, `maxFindings=200`.
  - Why customize: large monorepos may need higher thresholds to reduce noise.
  - Where to change: `settings.minMb`, `settings.staleDays`, `settings.maxFindings`.
- Pattern coverage
  - Default: predefined build/dependency/cache directories and transient/archive extensions.
  - Why customize: different stacks generate different artifact patterns.
  - Where to change: `settings.dirRuleOverrides`, `settings.fileExtRuleOverrides`.
- Scoring and severity
  - Default: size-based score plus category/age weighting with cutoffs `45/70/85`.
  - Why customize: teams may prefer fewer critical alerts or stronger stale-artifact emphasis.
  - Where to change: `settings.severityCutoffs`.

## Common Customization Profiles

- Strict hygiene
  - Lower `minMb`, lower `staleDays`, increase cache/dependency weights.
- Low-noise enterprise monorepo
  - Increase `minMb`, increase stale days, lower noisy artifact weights.
- Language-specific tuning
  - Add stack-specific build/cache directories and extensions.
- Archive-sensitive cleanup
  - Increase archive weights and lower stale threshold for old compressed files.

## Example Prompts For Codex

- "Customize workspace cleanup defaults for a monorepo with `minMb=200` and `staleDays=120`."
- "Add Rust and Go artifact overrides and reduce archive weighting."
- "Set severity cutoffs to medium 50, high 75, critical 90."

## Validation Checklist

- Confirm active config has `isCustomized: true`.
- Run a scan with defaults and verify workspace root/threshold behavior.
- Confirm custom override patterns appear in findings or are intentionally excluded.
- Confirm severity labels align with configured cutoffs.
