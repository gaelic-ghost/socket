# Safari MCP Evidence And Validation

## Evidence Order

1. Record the Safari Technology Preview version, target URL, and relevant viewport or emulated media.
2. Capture the observed page state using the smallest suitable set of page content, DOM evaluation, console messages, network summaries, and screenshot evidence.
3. State the expected result and compare it to the observation.
4. Apply only authorized interactions or code changes.
5. Recheck the same state after the action and report what changed.

## Focused Checks

| Goal | Useful evidence | Do not claim |
| --- | --- | --- |
| Rendering bug | screenshot, DOM state, computed layout values | cross-browser compatibility |
| Console or network failure | console entries, request status/timing, targeted response detail | backend correctness beyond the observed request |
| Accessibility issue | labels, roles, ARIA, focusable controls, screenshot contrast context | complete accessibility compliance |
| Performance concern | navigation/resource timing and relevant request timings | a reproducible benchmark or regression result from one run |
| Form or flow verification | expected DOM/state plus the authorized interaction result | payment, account, or destructive-action safety without explicit confirmation |

## Reporting Shape

Separate observed facts from inference. Include the tab or URL, environment, exact interaction if any, evidence collected, result, and remaining uncertainty. Save screenshots only when they add visual proof and keep them out of source control unless the repository explicitly owns test fixtures.
