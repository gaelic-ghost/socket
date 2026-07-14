---
name: scope-authorized-security-test
description: Define and verify authorization, targets, rules of engagement, data handling, safety controls, and stop conditions before active security testing. Use for penetration tests, vulnerability scans, exploit validation, web/API tests, network probing, red-team-like exercises, bug bounty work, or agent-driven testing where ownership and allowed techniques must be explicit.
---

# Scope Authorized Security Test

## Overview

Turn permission into an executable scope record before sending active traffic or running a proof of concept. Authorization must identify the owner and boundaries; access to a target or a public address is not permission.

Read [references/active-test-scope.md](references/active-test-scope.md) and complete every applicable field.

## Workflow

1. Identify authority.
   - Record target owner, authorizing person/record, tester, contacts, dates, jurisdiction or program policy, and evidence of permission.
2. Resolve targets precisely.
   - List domains, hosts, addresses/ranges, applications, APIs, repositories, accounts, environments, and third-party dependencies.
   - List exclusions explicitly and define how dynamic/cloud/CDN targets are resolved.
3. Define allowed techniques.
   - Separate passive review, discovery, authenticated testing, automated scanning, fuzzing, exploit validation, social/physical testing, persistence, credential access, data access, and denial-of-service.
   - Default unlisted techniques to disallowed.
4. Set operational controls.
   - Define source addresses, accounts, rate/concurrency, time windows, test data, logging, notification, emergency stop, cleanup, and restoration.
5. Define data handling.
   - Minimize accessed data; specify retention, encryption, screenshots/logs, secrets, evidence transfer, disclosure, and deletion.
6. Establish stop conditions.
   - Stop on target drift, third-party impact, instability, sensitive data beyond minimum proof, unexpected privileges, scope ambiguity, or an unapproved technique.
7. Approve the test plan.
   - Show exact targets and effects before tools run; update the scope record before expanding work.

## Output

Return authority, included/excluded targets, allowed/disallowed techniques, operational controls, data handling, stop/escalation contacts, and approval state.
