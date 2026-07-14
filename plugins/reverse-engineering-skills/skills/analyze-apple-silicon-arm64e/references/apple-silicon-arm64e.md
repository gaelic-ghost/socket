# Apple Silicon And arm64e Reference

## AArch64 Baseline

Use the current Arm Procedure Call Standard for register roles, parameter and result passing, stack alignment, callee-saved state, SIMD and floating-point conventions, and aggregate returns. Then verify the artifact's compiler-generated code; optimization, thunks, language runtimes, and platform conventions can obscure source-level boundaries.

## Pointer Authentication Evidence

Pointer Authentication Codes can protect selected pointers by signing and authenticating them with architectural keys and modifiers. Interpret the instruction sequence and use context rather than reducing PAC to one mnemonic.

Record:

- instruction and address
- pointer source and destination register
- apparent key and modifier source when encoded or inferable
- branch, load, store, sign, authenticate, or strip behavior
- original pointer representation
- tool normalization or masking
- runtime failure or success evidence when available

Tool displays can strip, preserve, or mishandle authenticated and tagged pointer bits. A successful symbol lookup after masking is a correlation clue, not proof that the mask is universally correct.

## Hardware And Policy Boundaries

- PPL and SPTM are platform integrity mechanisms whose use depends on SoC generation and OS architecture.
- Memory tagging and Memory Integrity Enforcement depend on hardware, compiler, runtime, and OS support.
- Xcode capabilities can request or enable supported build features but do not prove enforcement on every target.
- Rosetta translates Intel code and changes which instruction stream and address evidence are under inspection.

Live-check product scope before making a current claim. Record exact device, SoC, OS build, Xcode or compiler build, and whether the observation is static or runtime.

## Common Uncertainty Sources

- CPU subtype flattened to generic `arm64` by a loader.
- Pointer-authentication instructions rendered as unknown or simplified operations.
- Tagged or authenticated runtime addresses copied directly into a static database.
- Tail calls and authenticated returns obscuring function boundaries.
- Swift async, closures, and witness thunks mistaken for source functions.
- Translated Intel frames mixed with native Arm frames.

## Authoritative Sources

- [Arm ABI specifications](https://github.com/ARM-software/abi-aa)
- [Apple operating-system integrity and pointer authentication](https://support.apple.com/guide/security/sec8b776536b/web)
- [Apple Memory Integrity Enforcement](https://security.apple.com/blog/memory-integrity-enforcement/)
- [Xcode Enhanced Security capability](https://developer.apple.com/documentation/xcode/enabling-enhanced-security-for-your-app)
- [Apple Platform Security](https://support.apple.com/guide/security/welcome/web)

Use the current Arm ABI release and current Apple documentation for build-sensitive claims. Preserve older documentation when analyzing historical hardware rather than rewriting history around current behavior.
