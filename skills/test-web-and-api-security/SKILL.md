---
name: test-web-and-api-security
description: Test an explicitly authorized web application or API using current OWASP guidance and bounded manual or automated checks. Use for authentication, authorization, session, input, browser, API schema, business logic, file handling, server-side request, configuration, transport, error, and data-exposure tests when accounts, roles, target, rate, evidence, and stop conditions are defined.
---

# Test Web And API Security

## Overview

Test one scoped property at a time with role-aware accounts and reproducible requests. Use passive observation before active mutation and review automated scanner behavior before it reaches the target.

Read [references/web-api-test-plan.md](references/web-api-test-plan.md) and current OWASP WSTG/API guidance before execution.

## Workflow

1. Load the approved scope, environment, accounts/roles, data, rate limits, and stop conditions.
2. Map the application.
   - Record hosts, routes, APIs/schemas, roles, trust boundaries, sessions/tokens, browser controls, uploads, integrations, and state-changing operations.
3. Capture a baseline.
   - Preserve normal requests/responses and expected authorization for each role and resource owner.
4. Test by security property.
   - Cover identity/session, object/function authorization, input handling, browser/client boundaries, server-side fetches, files, configuration, errors, data exposure, business logic, and rate/resource controls as scope permits.
5. Use tools deliberately.
   - Keep proxy/browser history scoped; review ZAP or Nuclei configuration/templates; exclude destructive or broad checks; record exact versions and requests.
6. Validate candidates.
   - Reproduce with the smallest request, negative control, different role/owner, and fixed/mitigated state when available.
7. Clean up.
   - Remove test data/accounts/tokens, restore state, and report anything that could not be reverted.

## Output

Return scope/accounts, application map, tests and evidence, validated findings, negative results/coverage gaps, cleanup, and retest criteria.
