# Security Workflow Routing Map

| Primary question | Owning workflow | Common handoff |
| --- | --- | --- |
| What is this suspicious file, link, message, profile, package, or document? | `triage-suspicious-content` | Static malware analysis or script/document analysis |
| Is this artifact known, signed, reputable, or reported elsewhere? | `check-artifact-reputation` | Threat assessment |
| What could this artifact do without running it? | `perform-static-malware-analysis` | Reverse engineering for binary internals |
| What did it do in a disposable environment? | `perform-dynamic-malware-analysis` | Behavior mapping or detection content |
| Is this Mac affected and what should change now? | `assess-macos-threat` | Persistence/runtime inspection or containment |
| Is this vulnerability real and reachable here? | `validate-vulnerability` | Exposure assessment or stack remediation |
| May we actively test this target? | `scope-authorized-security-test` | Web/API or network-service testing |
| Is harm occurring across a system or organization? | `triage-security-incident` | Containment and recovery |
| How do I explain the result to the affected person? | `assess-and-explain-threat` | Security assessment report |

Do not route solely from a tool name. Start from the decision the user needs and the surface that may be affected.
