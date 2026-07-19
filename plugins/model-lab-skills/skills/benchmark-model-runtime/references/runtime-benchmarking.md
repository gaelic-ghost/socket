# Runtime Benchmarking Definitions

- Cold load: process/runtime initialization plus first artifact load under a stated cache condition.
- Warm load: repeated artifact readiness after intended caches exist.
- Time to first token: request start through availability of the first generated token; state whether tokenization and compilation are included.
- Prompt throughput: processed input tokens divided by prompt-processing time.
- Decode throughput: generated tokens after the first divided by decode time; state batch/concurrency.
- Peak memory: maximum comparable process or system allocation during the declared interval.
- Energy: measured joules or energy impact over a declared workload and tool; do not substitute instantaneous power without duration.

Report device model, memory, OS, runtime commit/version, artifact checksum, power state, thermal state, background-load policy, warm-up count, measured count, median, p90/p95 where useful, failures, and raw-sample location. When runtimes tokenize or sample differently, report that confound and avoid a single winner claim.
