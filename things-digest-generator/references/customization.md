# Customization Guide

## What To Customize First

- Due-soon horizon (`settings.dueSoonDays`).
- Planning window (`settings.daysAhead`).
- Scoring weights (`settings.scoringWeights`).
- Number of top projects/areas in output.
- Suggestion cap and output style.

## Personalization Points

- Time windows
  - Default: due-soon is 3 days; planning window is 4 days.
  - Why customize: users may plan in rolling 7-day, workweek-only, or monthly windows.
  - Where to change: `settings.dueSoonDays`, `settings.daysAhead`.
- Scoring formula
  - Default: weights prioritize completions and overdue risk with checklist signals.
  - Why customize: different users prioritize momentum, risk, or workload differently.
  - Where to change: `settings.scoringWeights`, `settings.openCountCap`.
- Top-N inclusion rules
  - Default: top 3 projects and top 2 areas.
  - Why customize: some users prefer narrower focus or broader coverage.
  - Where to change: `settings.topProjects`, `settings.topAreas`.
- Output style constraints
  - Default: concise operational tone.
  - Why customize: some users want executive summary-first output.
  - Where to change: `settings.outputStyle`, `settings.maxSuggestions`.

## Common Customization Profiles

- Ultra-concise daily triage
  - Lower top-N counts and suggestions; emphasize overdue items.
- Weekly planner
  - Use a 7-day horizon and include more tasks in `Week/Weekend Ahead`.
- Momentum-first coaching
  - Increase `completed7d` weight.
- Risk-first operational mode
  - Increase overdue and due-soon weights.

## Example Prompts For Codex

- "Set this digest skill to a 7-day planning window with executive output style."
- "Increase top areas to 4 and suggestions to 6."
- "Reweight scoring so overdue counts less and completions count more."

## Validation Checklist

- Confirm active config file has `isCustomized: true`.
- Generate a sample digest and verify section ordering and counts.
- Confirm horizon and due-soon behavior match configured values.
- Confirm scoring/ordering changes are reflected in top projects and suggestions.
