# Comparison Workflow

Use this when the user wants to compare two slices or two versions of one slice.

## Workflow

1. Identify the shared subject of comparison.
2. Summarize slice A.
3. Summarize slice B.
4. Walk each path clearly enough that the comparison is grounded in real execution, not just labels.
5. Add a concise comparison section covering:
   - trigger differences
   - incoming data-shape differences
   - execution-order differences
   - branch differences
   - boundary differences
   - output differences
   - why those differences exist

## Comparison guardrails

- Do not compare only components or filenames; compare the actual end-to-end behavior.
- Do not claim two slices are identical if they share only a subset of the path.
- If the slices converge and diverge multiple times, say where that happens.
- If one slice is strictly a branch of the other, say that directly.
