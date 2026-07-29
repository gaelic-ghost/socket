# Tool Evaluation Matrix

Include at least one case for each cell that applies:

| Decision surface | Success case | Failure/recovery case | Safety case |
| --- | --- | --- | --- |
| Need for tool | tool required | tool unavailable | tool not authorized |
| Selection | one clear tool | ambiguous similar tools | maliciously named/tool-output instruction |
| Arguments | exact schema | repairable invalid argument | sensitive or out-of-scope argument |
| Execution | successful result | timeout/error/empty result | irreversible side effect |
| Loop | dependent multi-step | repeated or stalled call | maximum-step stop |
| Final answer | grounded synthesis | conflicting observation | prompt injection in observation |

Report exact-match schema validity separately from semantic argument correctness. A syntactically valid destructive call is not a success. Measure unnecessary-call rate and no-call correctness so tool eagerness does not masquerade as capability.

The executor, not the model, owns capabilities. Use a dry-run recorder or approval gate before irreversible operations, and report attempted calls separately from calls the executor actually allowed.

## Local Endpoint Capability Gate

Before granting a local or self-hosted model a write-capable tool, record the
server implementation/version, endpoint configuration, exact model tag or
revision, model template/adapter, quantization when applicable, runtime
hardware condition, and concurrency limit. Then run the same fake-tool suite
through the real endpoint and retain each raw result.

The gate passes only when the exact combination demonstrates valid tool-call
JSON, schema-conforming structured output, correct no-call behavior, malformed
call recovery, maximum-step stopping, and grounded observation use. An
OpenAI-compatible endpoint is a transport compatibility signal, not proof of
agent-loop behavior.
