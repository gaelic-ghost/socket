---
name: assess-and-explain-threat
description: Assess whether suspicious evidence indicates a real threat and explain the result in practical language. Use when a person needs a confidence-calibrated conclusion, immediate protective actions, remaining uncertainty, impact, or understandable advice after artifact, endpoint, vulnerability, identity, or incident evidence has been collected.
---

# Assess And Explain Threat

## Overview

Turn mixed evidence into a proportionate conclusion and advice the affected person can follow. Do not collapse signatures, reputation, scanner output, or unusual behavior into a binary safe/malicious verdict.

Read [references/confidence-and-advice.md](references/confidence-and-advice.md) for conclusion vocabulary and the explanation shape.

## Workflow

1. Restate the decision.
   - Identify what the user must decide now and what can wait for more evidence.

2. Grade evidence by directness.
   - Separate direct observations, reproducible behaviors, vendor or threat-intelligence claims, weak indicators, absence of findings, and speculation.
   - Record contradicting evidence and coverage gaps.

3. Assess behavior and impact.
   - State what access, execution, persistence, collection, credential use, network behavior, or data exposure is observed or technically plausible.
   - Distinguish capability from intent and artifact presence from successful compromise.

4. Choose a calibrated classification.
   - Use one classification from the reference and state confidence separately.
   - Name the strongest supporting evidence and what would change the conclusion.

5. Give proportionate advice.
   - Put urgent harm-reduction actions first.
   - Separate containment, evidence preservation, recovery, credential actions, notification, and long-term hardening.
   - Avoid destructive cleanup when evidence is weak and reversible isolation is available.

6. Give a plain-language explanation.
   - Answer whether the concern is dangerous, what it appears to do, what is known versus inferred, what to do now, and when to escalate.
   - Define specialist terms at first use and avoid fear-amplifying language.

## Output

Return the conclusion, confidence, decisive evidence, contradictions/gaps, immediate actions, follow-up analysis, and a short non-specialist explanation.
