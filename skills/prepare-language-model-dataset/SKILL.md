---
name: prepare-language-model-dataset
description: Prepare and document language-model training, preference, calibration, red-team, or evaluation datasets. Use when collecting, filtering, normalizing, deduplicating, templating, splitting, sampling, or auditing examples and when leakage, provenance, consent, licensing, or sensitive-data handling affects the result.
---

# Prepare Language Model Dataset

## Workflow

1. Define the dataset's task, unit of observation, schema, and intended use.
2. Record every source, revision, retrieval date, license, consent basis, and transformation.
3. Validate parseability and required fields before semantic filtering.
4. Normalize text and chat templates without erasing distinctions the task needs.
5. Remove secrets and unapproved personal or sensitive data before logging or upload.
6. Deduplicate before splitting. Use content hashes plus near-duplicate analysis where paraphrases matter.
7. Split by contamination boundary—document, conversation, author, repository, or time—not merely by row.
8. Search train data for evaluation overlap and record the matching method and threshold.
9. Measure language, length, label, source, safety, and quality distributions for every split.
10. Copy `assets/dataset-card.md` and document exclusions, known biases, and redistribution limits.
11. Freeze a versioned artifact or deterministic build recipe and record checksums.

## Acceptance Gates

- Every example is traceable to a source or a documented synthetic generator.
- Train, validation, and test boundaries match the leakage model.
- The tokenizer and chat template used for length checks match the intended model.
- Rejected records and filter counts are retained without retaining removed secrets.
- A human can reconstruct the released split from the documented inputs and transformations.

## Resources

- `assets/dataset-card.md`: dataset provenance and quality template.
- `references/dataset-controls.md`: split, leakage, and sensitive-data controls.
