# Detail Levels

The user controls density, not completeness.

## `quick`

Use short prose and keep commentary tight, but still include every meaningful step in order.

Good fit for:

- first-pass orientation
- small code paths
- quick checks during active debugging

Do not:

- skip intermediate functions that materially transform or route data
- replace the walkthrough with only a summary

## `standard`

This is the default level.

Use enough detail for a careful read-through:

- meaningful step-by-step narrative
- clear data-shape commentary
- branch and boundary callouts
- concise reasons for transformations

Good fit for most code-reading tasks.

## `thorough`

Use the same full step chain, but add more context around:

- why the initial contract looks the way it does
- why each boundary exists
- how shared versus specialized logic is split
- branch-specific behavior
- why data is normalized, adapted, validated, or repackaged
- what assumptions or invariants the path relies on

Good fit for:

- unfamiliar systems
- onboarding
- debugging subtle behavior
- review of architectural intent

## Invariant

No detail level may intentionally omit meaningful steps from the requested slice.
