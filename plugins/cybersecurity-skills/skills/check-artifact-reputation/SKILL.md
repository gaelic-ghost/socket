---
name: check-artifact-reputation
description: Check local and external reputation for a suspicious artifact, signer, hash, URL, domain, certificate, package, or vendor. Use when provenance and threat-intelligence context could inform triage, while sample-upload privacy, stale intelligence, hash-only misses, false positives, and reputation-versus-behavior limits must remain explicit.
---

# Check Artifact Reputation

## Overview

Gather provenance and intelligence without treating popularity, valid signing, a clean lookup, or a vendor label as a safety verdict. Prefer local identity and vendor sources before sending data to third parties.

Read [references/reputation-evidence.md](references/reputation-evidence.md) for source ordering and interpretation.

## Workflow

1. Fix identity.
   - Record artifact hashes, signer/certificate, exact version, source URL, domain, resolved destinations, and acquisition time.

2. Check local evidence.
   - Inspect quarantine/provenance, signature/notarization, known installation records, local security detections, and expected vendor distribution paths.

3. Check authoritative sources.
   - Prefer vendor advisories, release checksums/signatures, certificate status, official repositories, and current platform security sources.
   - Date each lookup.

4. Decide whether external intelligence is appropriate.
   - Explain whether the service receives only a hash/domain or may upload/retain the artifact.
   - Obtain explicit approval before sending private artifacts, URLs, customer data, or unknown binaries.

5. Correlate results.
   - Record detection names, engines/sources, first/last seen, submission context, prevalence, relations, and conflicting classifications.
   - Distinguish “not present” from “known benign.”

6. Feed behavior analysis.
   - Use reputation to prioritize static/dynamic checks, not replace them.

## Output

Return identity, sources/date, privacy decision, reputation observations, conflicts, interpretation limits, confidence effect, and next behavioral check.
