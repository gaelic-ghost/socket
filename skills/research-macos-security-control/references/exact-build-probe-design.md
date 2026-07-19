# Exact-Build Probe Design

## Probe ladder

1. Static/read-only: documentation, SDK, signature/entitlements, Mach-O/dyld metadata, symbols, strings, interface metadata, service ownership, existing logs.
2. Supported bounded observation: public preflight/status, one benign operation, focused log query, existing Endpoint Security telemetry.
3. Disposable SIP-enabled macOS guest: prompts, quarantine/Gatekeeper, signing identity, policy state, service restart, or repeatable failure injection.
4. Physical Mac or specialized environment: Secure Enclave, recoveryOS/boot policy, hardware, system/kernel extension, anti-VM, device, or customer-fidelity questions.
5. Explicitly approved transformation/protection change: only if lower steps cannot answer the narrow hypothesis.

## Design record

State the hypothesis, independent/dependent variables, exact actor/target/artifact/build, baseline, one intended change, expected confirming and contradicting result, required permission/telemetry, stop condition, cleanup, and fidelity limit. Preserve negative results with collection coverage.

Do not prompt or mutate Gale's active Mac without immediate explicit approval. Do not use a broad terminal/agent Full Disk Access grant when a narrow signed fixture can answer the question. If a guest cannot reproduce hardware, boot, recovery, Data Vault, anti-VM, or customer state, label the result lower fidelity rather than compensating with stronger host mutations.

For cross-build work, hold architecture, artifact role, signing class, security state, analysis tools, and probe method constant. Use `compare-binary-versions` to record correspondence and temporal bounds.
