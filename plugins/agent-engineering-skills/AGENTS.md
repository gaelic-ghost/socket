# AGENTS.md

This plugin owns reusable agent-system design and operating workflows. Follow
root Socket guidance for general Git, release, dependency, safety, and
documentation rules.

## Scope

- Own coordinator/worker contracts, external-agent handoffs, scheduling,
  orchestration, and agent-system evaluation.
- Keep host compatibility adapters in `agent-portability-skills` and language
  implementation in the owning stack plugin.
- Keep plugin manifests, marketplace wiring, and plugin repository maintenance
  in `agent-plugin-skills`.
- Root `skills/` is the authored source of truth; plugin metadata is packaging.

## Validation

Run from the Socket repository root so the shared maintainer environment and
cache policy apply:

```text
just repo-validate
just test
```
