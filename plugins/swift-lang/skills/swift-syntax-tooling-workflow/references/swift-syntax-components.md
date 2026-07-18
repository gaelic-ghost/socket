# SwiftSyntax Component Selection

| Product | Responsibility |
| --- | --- |
| `SwiftParser` | Parse source text into a source-accurate syntax tree, including recovery for malformed input. |
| `SwiftSyntax` | Represent and inspect syntax nodes, tokens, trivia, positions, visitors, and rewriters. |
| `SwiftSyntaxBuilder` | Construct syntax through builders and syntax-oriented literals. |
| `SwiftParserDiagnostics` | Produce parser-focused diagnostics for recovered syntax. |
| `SwiftDiagnostics` | Model diagnostics, notes, highlights, and fix-its emitted by syntax tooling and macros. |
| `SwiftOperators` | Fold parsed operator sequences when precedence-aware structure is required. |
| `SwiftSyntaxMacros` | Implement macro expansion roles and return generated syntax. |
| `SwiftSyntaxMacrosTestSupport` | Test macro expansions and diagnostics. |

Use the smallest product set that expresses the task. Keep collection and transformation code independent from filesystem traversal and reporting.

SwiftSyntax major releases align with Swift language and tooling releases. Check the repository's release guidance and the target compiler rather than guessing compatibility from API spelling.

SwiftSyntax is source accurate, but it does not independently provide the compiler's fully type-checked semantic AST. Route inferred types, overload resolution, and project-wide references to semantic or index tooling.

## Verification Fixture Set

- positive transformation
- structurally similar negative case
- comments and unusual trivia
- malformed or incomplete source
- conditional compilation
- repeated execution for idempotence
- generated code policy
- selected Swift language version

## Authoritative Source

- [SwiftSyntax repository and release guidance](https://github.com/swiftlang/swift-syntax)
