---
name: analyze-apple-silicon-arm64e
description: Analyze AArch64 and Apple arm64e instruction, calling-convention, pointer-authentication, tagged-pointer, Rosetta, and hardware-mitigation evidence. Use when Codex must interpret Apple Silicon disassembly, registers, stack frames, SIMD, compiler idioms, PAC instructions or authenticated pointers, CPU subtypes, top-byte handling, SPTM or PPL context, memory tagging, or Memory Integrity Enforcement without generalizing behavior across unsupported hardware or OS builds.
---

# Analyze Apple Silicon arm64e

## Overview

Interpret low-level evidence using the selected slice, exact hardware, OS build, and tool behavior. Separate the AArch64 ABI from Apple-specific `arm64e` and hardware-security claims.

Read [references/apple-silicon-arm64e.md](references/apple-silicon-arm64e.md) when decoding calling conventions, pointer authentication, tagged addresses, Rosetta boundaries, or hardware-scoped mitigations.

## Workflow

1. Establish execution identity.
   - Record artifact hash, CPU type and subtype, selected slice, UUID, minimum OS and SDK clues, tool and version, loader, and base address.
   - Record hardware model and SoC, OS build, and native, translated, Simulator, VM, or physical-device context for runtime evidence.

2. Apply the AArch64 ABI baseline.
   - Track argument and result registers, stack pointer alignment, frame and link registers, callee-saved state, SIMD or floating-point registers, and aggregate-return conventions.
   - Confirm the actual prologue, epilogue, and call sites before accepting a decompiler signature.

3. Identify compiler-generated patterns.
   - Separate ordinary branches, tail calls, thunks, stubs, outlined helpers, stack probes, reference-counting calls, async lowering, and switch or jump-table patterns.

4. Interpret pointer authentication.
   - Record PAC-related instructions, key and modifier clues available from the instruction, authenticated branch or return behavior, and whether a displayed pointer retains, strips, or misrepresents PAC or tag bits.
   - Do not treat authenticated control flow as proof that every pointer or data path is protected.

5. Normalize addresses deliberately.
   - Preserve the original displayed value.
   - Record any top-byte, tag-bit, PAC, sign-extension, or slide normalization used for a tool lookup.
   - Confirm that normalization matches the artifact and environment rather than applying a universal mask.

6. Bound hardware-security claims.
   - Tie PPL, SPTM, memory tagging, Memory Integrity Enforcement, and other mitigations to current Apple documentation, exact SoC family, and OS build.
   - Distinguish a compiler capability, hardware feature, OS policy, and observed enforcement.

7. Preserve Rosetta boundaries.
   - Record whether the artifact and process are Intel or Arm, where translation occurs, and which address space or generated code the observation represents.
   - Keep Intel-era preservation findings separate from native Apple Silicon behavior.

8. Cross-check important conclusions with disassembly, references, runtime registers, and a second tool when the first tool has incomplete `arm64e` support.

## Guardrails

- Do not silently analyze the wrong universal slice.
- Do not present `arm64` and `arm64e` as interchangeable.
- Do not erase PAC or tag information without preserving the original value and transformation.
- Do not generalize a mitigation from one SoC generation or product family to all Apple Silicon.
- Do not use Simulator or VM behavior as proof of physical-device secure boot, PAC, Secure Enclave, or memory-integrity enforcement.

## Output

Return execution identity, ABI interpretation, PAC and address-normalization observations, hardware-scoped mitigation context, tool limitations, and the next instruction or runtime check.
