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
