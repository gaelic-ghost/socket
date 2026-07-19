# Evaluation Methods

Use exact matching only when formatting variation is genuinely incorrect. Normalize only transformations allowed by the task contract.

Use code execution for tests and schemas inside a constrained environment with explicit timeouts and side-effect boundaries.

Use model judges for semantic qualities that deterministic graders cannot express. Calibrate them, retain judge reasoning only when policy and privacy permit it, and report agreement rather than treating the judge as ground truth.

For paired cases, compute case-level deltas rather than comparing only independent aggregates. Slice by difficulty, source, language, length, and safety category when those dimensions affect the decision. Never discard errors or refusals from the denominator without reporting both denominators.
