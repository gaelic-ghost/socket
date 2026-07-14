---
name: author-yara-x-rules
description: Author, test, tune, and document YARA-X detection rules from validated artifact evidence. Use when malware, suspicious files, scripts, documents, or binary features need local pattern detection with stable discriminators, metadata, positive and negative fixtures, performance checks, false-positive review, rule provenance, and regression testing.
---

# Author YARA-X Rules

## Overview

Create rules that detect the validated property the evidence supports, not a broader malware-family claim. Prefer structural combinations over unique-looking strings copied from one sample.

Read [references/yara-x-rule-quality.md](references/yara-x-rule-quality.md) before selecting patterns or declaring coverage.

## Workflow

1. Define the detection objective and non-goals.
2. Build the fixture set.
   - Preserve representative positive samples and near-miss benign negatives with hashes and provenance.
   - Use synthetic or redistributable fixtures for repository tests.
3. Select discriminators.
   - Prefer format/module facts, byte structures, stable code/config fragments, and combinations of independently meaningful strings.
   - Avoid mutable infrastructure, compiler boilerplate, paths, timestamps, or one generic API name as decisive evidence.
4. Author metadata and conditions.
   - Include purpose, author, date, source/evidence reference, scope, confidence, and known limitations.
   - Bound file type and size where it improves correctness or performance.
5. Validate with current YARA-X.
   - Record version; compile/lint the rule; test all positives, negatives, malformed inputs, and a bounded benign corpus.
   - Investigate timeouts, warnings, and module-undefined behavior.
6. Review false positives and coverage.
   - Tune by improving evidence combinations, not by accumulating arbitrary exclusions.
7. Preserve regression evidence.
   - Store allowed fixtures or deterministic generators, expected matches/non-matches, and rule revision.

## Output

Return the rule, objective, evidence basis, fixture results, performance notes, known misses/false positives, and deployment limits.
