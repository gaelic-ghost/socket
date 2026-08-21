# Socket Integration Validation

Socket intentionally keeps one essential validation path and one root E2E.

## Live Gates

- `just repo-validate` checks managed repository assets, all four canonical
  documents, marketplace-to-plugin resolution, aligned plugin versions, Claude
  marketplace references, and root-only test placement.
- `just test` installs the repository-maintenance payload into a temporary Git
  repository and exercises docs apply, byte-idempotence, docs check, the exact
  Just recipe surface, and installed validation end to end.
- `.github/workflows/validate-repo-maintenance.yml` invokes
  `just repo-validate` without duplicating repository policy.

## Test Ownership

All tests live directly under the Socket root [`tests/`](../../tests/). Socket
does not retain nested plugin tests, skill-local tests, unit suites, per-file
docs tests, or permanent-absence regression tests. Shipped behavior is proved
through the current install-and-operate path.

## Commands

```bash
just docs-check
just repo-validate
just test
```
