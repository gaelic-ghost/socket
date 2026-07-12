# Model Evaluation, Performance, and Diagnostics

## Evaluation

Maintain a small representative fixture set with expected labels, boxes, masks, ambiguous cases, empty cases, and known failure modes. Record model version, request family, crop policy, thresholds, postprocessing, platform, OS, and device for each baseline. Re-run it after any model or integration change.

Accuracy claims require an appropriate dataset and metric for the product decision. A few passing fixtures prove integration stability, not general model quality. Review class balance, false positives, false negatives, threshold tradeoffs, and subgroup or environmental limitations relevant to the use case.

## Compute and Performance

Choose `MLModelConfiguration.computeUnits` from compatibility and measured latency, throughput, memory, energy, and thermal behavior. Do not infer the actual processing unit from the requested configuration alone. Warm-up, compilation, model loading, preprocessing, prediction, postprocessing, and UI publication are separate timing phases.

For live streams, bound in-flight frames and measure end-to-end age, not only inference duration. Profile representative release builds on target devices before claiming real-time behavior.

## Diagnostics

Report model identity and version, model URL or asset boundary without secrets, input constraint mismatch, actual source dimensions and format, crop policy, compute-unit configuration, request/API family, output names and types, elapsed phase, cancellation or stale-frame status, and the next value to inspect. Never reduce failures to "recognition failed" or an empty result without context.
