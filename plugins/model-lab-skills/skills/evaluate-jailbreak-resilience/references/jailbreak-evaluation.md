# Jailbreak Evaluation Design

Measure at least attack success rate, correct refusal rate, benign over-refusal, invalid/empty outputs, and severe side effects. Define whether partial disclosure, planning, tool invocation, or completed harmful action counts as success before evaluation.

Keep attack development and held-out evaluation separate. Adaptive methods must report the number of target queries and evaluator feedback available to the attacker. When comparing defenses, use the same attack budget and distinguish robustness gains from degraded general capability or blanket refusal.

Useful official or primary research surfaces include [Inspect AI](https://github.com/UKGovernmentBEIS/inspect_ai), Apple's [ml-persona-red-teaming](https://github.com/apple/ml-persona-red-teaming), and Apple's [ml-mmtoolsandbox](https://github.com/apple/ml-mmtoolsandbox). Classify and pin each repository before use; research code is not automatically a maintained production harness.
