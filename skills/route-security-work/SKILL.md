---
name: route-security-work
description: Route an ambiguous cybersecurity request before tools run. Use for suspicious files, links, messages, host behavior, malware questions, vulnerability reports, authorized pentests, security incidents, threat hunting, detection work, or security advice when the correct workflow and specialist owner are not yet clear.
---

# Route Security Work

## Overview

Turn the user's concern into one bounded security question, identify the affected surface, and select the smallest safe owner workflow. Do not begin active probing or execute suspicious content during routing.

Read [references/routing-map.md](references/routing-map.md) when ownership or the difference between investigation, testing, response, and remediation is unclear.

## Workflow

1. State the requested decision.
   - Capture what the user needs to know or do now.
   - Separate “is this dangerous?” from “how does it work?”, “am I affected?”, and “how do I fix it?”.

2. Identify the surface.
   - Classify the primary subject as content or artifact, endpoint, identity, network/service, application/source, vulnerability report, or active incident.
   - Record the relevant artifact, host, account, service, repository, target, and time window.

3. Establish authority and urgency.
   - For inspection and defensive response, confirm the user controls or is responsible for the affected surface.
   - Before active testing, require the target owner, allowed targets, exclusions, time window, techniques, stop conditions, and contacts.
   - If harm is ongoing, route immediate containment separately from evidence preservation.

4. Choose the next owner.
   - Use `preserve-security-evidence` before transformations or volatile state disappears.
   - Use `select-analysis-isolation` before opening or executing untrusted content.
   - Use `assess-and-explain-threat` when evidence exists but the practical conclusion is unclear.
   - Route deep binary work to `reverse-engineering-skills` and repository-wide source scans to Codex Security when available.
   - Route ordinary implementation or remediation to the owning Apple, protocol, language, or framework skill after the security acceptance criteria are explicit.

5. Report the route.
   - Name the selected workflow, why it fits, what is intentionally deferred, and the first non-destructive action.
   - Preserve uncertainty rather than selecting a dramatic path from weak evidence.

## Output

Return the security question, affected surface, urgency, authority/scope state, selected owner, first safe action, and any immediate stop condition.
