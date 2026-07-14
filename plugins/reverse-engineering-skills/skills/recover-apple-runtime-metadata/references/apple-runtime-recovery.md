# Apple Runtime Recovery Reference

## Evidence Classes

- Binary or debug symbol: stored in a symbol table or debug information.
- Objective-C runtime metadata: class, category, protocol, selector, method, property, or ivar data used by the runtime.
- Swift runtime metadata: type descriptors, field metadata, conformances, witness tables, and related ABI records.
- Demangled presentation: a readable rendering of a recorded mangled identity.
- Tool inference: a guessed function boundary, type, variable, or source-like construct.
- Analyst proposal: a documented rename or relationship supported by cited evidence.

## Objective-C Clues

Common Mach-O sections and references can expose class lists, category lists, protocol lists, selector references, class references, constant strings, and method encodings. Section names and layouts can vary by platform, linker, optimization, and tool presentation. Prefer the current runtime source and the artifact's actual load commands over a memorized section inventory.

Validate method ownership and signatures against:

- selector and class references
- method type encodings when present
- message-send call sites and receiver construction
- superclass and protocol relationships
- category metadata and load behavior

## Swift Clues

Preserve the mangled identity before demangling. Swift metadata and symbols can expose types, modules, functions, protocol conformances, witness tables, generic specializations, async functions, closures, and compiler-generated thunks. Optimization can merge, outline, specialize, or remove source-level boundaries.

Common uncertainty sources include:

- reflection metadata stripped or reduced
- generic specialization replacing a reusable source function
- async lowering producing resumable state-machine functions
- closure contexts and partial-application thunks
- witness and bridging thunks rendered as ordinary functions
- resilience boundaries hiding field or layout assumptions
- tool demanglers and Swift ABI knowledge lagging the artifact toolchain

## Cross-Checks

- Confirm a name at more than one reference when possible.
- Confirm a proposed field with access width, offset use, initialization, and metadata.
- Confirm a proposed type with multiple callers or witness/conformance evidence.
- Compare a decompiler's signature with the actual calling convention and register use.

## Authoritative Sources

- [Swift ABI documentation in the Swift repository](https://github.com/swiftlang/swift/tree/main/docs/ABI)
- [Swift runtime source](https://github.com/swiftlang/swift/tree/main/stdlib/public/runtime)
- [Apple Objective-C runtime source](https://github.com/apple-oss-distributions/objc4)
- [Apple Mach-O APIs](https://developer.apple.com/documentation/kernel/mach-o)

Use the Swift version and local toolchain sources that match the artifact when possible. Current `main` documentation is architectural guidance, not proof that an older or beta compiler emitted the same shape.
