# Code Smells And Remediation

| Evidence class | Inspect | Prefer |
| --- | --- | --- |
| Invalidation fan-out | broad environment reads and observable ownership | read narrow values; localize state and observation. |
| Identity churn | `ForEach` identifiers, recreated collections, top-level branch swaps | stable, domain-derived identity and a stable view tree. |
| Body work | sorting, filtering, decoding, formatting, sync I/O in `body` | derive/precompute from explicit inputs outside rendering. |
| Layout churn | nested geometry/preference chains and unconstrained hierarchies | simpler hierarchy and fixed constraints where honest. |
| Image cost | full-size decode/resize on the main path | downsample/preprocess for the rendered size. |
| Animation cost | broad implicit animation or large transition scope | narrow the animated value and affected subtree. |

These are audit hypotheses, not measurements. Use a trace before claiming impact or selecting a tradeoff that makes code less clear.
