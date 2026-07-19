---
name: evaluate-tool-calling-model
description: Evaluate tool selection, arguments, schemas, execution, observation use, recovery, and side effects. Use when comparing tool-capable checkpoints, prompts, parsers, agent loops, function schemas, or harnesses.
---

# Evaluate Tool-Calling Model

## Model The Whole Loop

Evaluate these stages separately: whether a tool is needed, which tool is selected, whether arguments are semantically correct and schema-valid, whether execution is authorized, whether the observation is interpreted correctly, whether the loop stops, and whether the final answer reflects the tool result.

## Workflow

1. Inventory tools, schemas, side effects, auth requirements, error modes, and name/description ambiguities.
2. Build cases for correct calls, no-call answers, ambiguous choices, parallel calls, dependent calls, invalid arguments, tool errors, empty results, malicious tool output, authorization denial, and recovery.
3. Use deterministic fake tools with recorded inputs and outputs for the core suite.
4. Enforce authorization in the executor independently of model output. The model cannot grant itself a capability; intercept denied and irreversible calls before execution and record attempted versus executed side effects separately.
5. Pin model, prompt, schema serialization, parser, retry policy, maximum steps, and harness revision.
6. Score selection, arguments, ordering, execution result, recovery, final answer, latency, token use, attempted side effects, and executed side effects independently.
7. Detect invalid JSON, hallucinated tools, repeated calls, ignored errors, premature answers, and non-termination explicitly.
8. Run live integration cases only after the fake-tool suite passes and only inside approved side-effect boundaries.
9. Attribute failures to model, prompt, schema, parser, executor, or orchestration rather than collapsing everything into model accuracy.

## Ownership Boundary

This skill evaluates a model plus harness interface. Use `productivity-skills` when the primary artifact is an agent skill or plugin package, and `agent-portability-skills` when the question is host compatibility rather than behavioral quality.

## References

Read `references/tool-evaluation-matrix.md` for minimum cases and metrics.
