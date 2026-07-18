# Swift Compiler Inspection Surfaces

## Supported Driver Surfaces

Prefer `swift` or `swiftc` for parsing, type checking, compilation, module emission, dependency scanning, supported diagnostics, and driver job inspection. The driver coordinates frontend, module, linker, and auxiliary jobs; it is not the type checker itself.

Representative categories include:

- `-parse` and `-typecheck`
- driver job printing and parseable driver output
- dependency scanning
- emitted modules and module interfaces
- SIL and LLVM IR emission
- serialized diagnostics and supported-arguments inventory

Check the selected compiler's own help before using a flag. Options change across releases and Apple toolchains may carry additional behavior.

## Version-Sensitive Surfaces

- textual or structured AST dumps
- SIL and IR textual comparison across compiler versions
- diagnostic identifiers and formatting
- generated module interfaces outside their compatibility contract
- plugin and macro expansion implementation details

Capture the complete toolchain version and command beside any persisted fixture.

## Compiler-Internal Surfaces

Direct `swift-frontend` invocation bypasses driver planning and may require internal arguments normally supplied by the driver. Prefer obtaining a real frontend job from driver output before experimenting. Never turn an internal reproduction command into normal project build guidance.

## Phase Interpretation

- Parsed AST: grammar structure without completed semantic analysis.
- Type-checked AST: semantic analysis and inferred types have run.
- Raw SIL: lowering from the type-checked AST.
- Canonical SIL: mandatory transformations have run.
- Optimized SIL: optimization-dependent program representation.
- LLVM IR: Swift-specific lowering has moved into LLVM's representation.

Compare like with like: same toolchain, target, SDK, optimization, language mode, conditional flags, and inputs.

## Authoritative Sources

- [Swift compiler architecture](https://www.swift.org/documentation/swift-compiler/)
- [Swift compiler driver](https://github.com/swiftlang/swift-driver)
