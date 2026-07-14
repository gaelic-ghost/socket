---
name: report-apple-security-research
description: Turn Apple-platform security research evidence into a reproducible, exact-build technical report. Use when Codex must document affected hardware and OS builds, expected and observed behavior, a minimal test case, artifact hashes, crash or sysdiagnose evidence, impact, mitigations, version bounds, beta revalidation, unresolved questions, or a handoff to the current Apple Security Research, Security Bounty, or Security Research Device reporting process.
---

# Report Apple Security Research

## Overview

Write the technical evidence first and keep disclosure or program submission as a separate current-policy workflow. Make the report reproducible without overstating exploitability, affected versions, or source-level cause.

Read [references/apple-security-reporting.md](references/apple-security-reporting.md) for the evidence checklist, version language, privacy checks, and live Apple sources.

## Workflow

1. Define the finding.
   - State the affected component, security property, expected behavior, observed behavior, and why the difference matters.

2. Fix the tested environment.
   - Record product and hardware model, SoC, OS marketing version and build, Xcode or SDK build, security state, and native, translated, Simulator, VM, physical-device, or research-device context.

3. Fix artifact and tool identity.
   - Record hashes, UUIDs, bundle or component versions, signing and entitlement state, acquisition and transformation history, tool versions, scripts, and analysis projects.

4. Provide a minimal reproduction.
   - List prerequisites, setup, exact steps, expected result, observed result, timestamps, and cleanup.
   - Remove unrelated privileges, data, logging, and environmental assumptions.

5. Separate evidence layers.
   - Direct observations.
   - Generated tool output.
   - Inferences and confidence.
   - Unresolved alternative explanations.

6. Bound affected versions.
   - List every build tested and use `first observed`, `last observed`, or `changed between` accurately.
   - Revalidate beta findings on the newest publicly available build before making a current eligibility or impact claim.

7. Explain impact and mitigations.
   - Describe concrete confidentiality, integrity, availability, containment, or trust-boundary effect supported by evidence.
   - Separate a workaround, environmental constraint, and product fix.

8. Prepare disclosure only when requested.
   - Live-check current Apple Security Research, bounty, and research-device rules.
   - Review attachments for personal, customer, secret, or unrelated diagnostic data before transmission.

## Guardrails

- Do not turn a crash, static pattern, or decompiler warning into an exploitability claim without evidence.
- Do not claim an introducing or fixed build when only endpoints were tested.
- Do not claim program eligibility, reward, confidentiality, or disclosure terms from memory.
- Do not submit or transmit the report, diagnostics, or artifacts without explicit user authorization.

## Output

Return a report with summary, environment, artifact identity, reproduction, observations, generated evidence, inference, impact, affected-build bounds, mitigations, open questions, and disclosure-readiness checklist.
