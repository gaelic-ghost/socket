---
name: preserve-security-evidence
description: Preserve and document security evidence before analysis, containment, or remediation changes it. Use for suspicious artifacts, volatile host state, vulnerability validation, incident records, logs, screenshots, commands, hashes, timelines, transformations, and analyst handoffs that need reproducible provenance without claiming legal-forensics certification.
---

# Preserve Security Evidence

## Overview

Create a reproducible security record while keeping originals and observations distinct from transformed working material. Prioritize volatile evidence when delay would erase it, but state when urgent harm reduction must take precedence.

Read [references/security-record.md](references/security-record.md) for the shared record and transformation shapes.

## Workflow

1. Define the question and evidence owner.
   - Record the affected person/system, requested decision, acquisition source, time, and analyst.
   - Record authorization and disclosure limits when they matter.

2. Separate original and working material.
   - Avoid opening active content during preservation.
   - Copy artifacts into a clearly named working area when analysis requires mutation.
   - Record every extraction, decoding, re-sign, patch, conversion, or replay as a transformation that creates a new artifact identity.

3. Capture stable identity.
   - Record paths or logical identifiers, sizes, timestamps, cryptographic hashes, versions, bundle/package identifiers, UUIDs, signer identity, and source URLs when applicable.
   - Record tool name, version, command, configuration, and environment for consequential observations.

4. Prioritize volatile state.
   - Capture time, logged-in users, processes and ancestry, open files, network state, relevant memory or runtime telemetry, and transient logs only when authorized and proportionate.
   - Do not collect unrelated personal or secret data merely because access is available.

5. Maintain evidence quality.
   - Store observations, external intelligence, hypotheses, conclusions, and disproven hypotheses separately.
   - Preserve raw output alongside summaries when safe.
   - Mark missing data, collection failures, time skew, incomplete coverage, and evidence destroyed by containment.

6. Produce a handoff.
   - State which inputs are originals, which are working copies, what changed, and which next workflow should consume them.

## Guardrails

- Do not call ordinary engineering notes a legally sufficient chain of custody.
- Do not upload evidence to a third party without explicit approval and a data-egress explanation.
- Do not overwrite an original with a cleaned, extracted, or transformed copy.
