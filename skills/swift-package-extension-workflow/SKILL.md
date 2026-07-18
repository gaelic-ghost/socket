---
name: swift-package-extension-workflow
description: Plan and validate SwiftPM build or command plugins, macros, package traits, generated sources, permissions, and Xcode handoffs. Use for Package.swift extension work or Swiftly/Xcode capability differences.
---

# Swift Package Extension Workflow

## Purpose

Own SwiftPM extension work that does not belong in ordinary package build/run or testing workflows. Keep package plugins, macros, traits, generated-source policy, permission review, and toolchain comparison in one package-first path, then hand off when Xcode-managed project context becomes authoritative.

## When To Use

- Use this skill for build tool plugins, command plugins, plugin products, target plugin usage, and plugin commands.
- Use this skill for macro targets, macro declaration/implementation boundaries, expansion inspection, diagnostics, and macro tests.
- Use this skill for package traits, default traits, optional dependencies, conditional compilation, and trait-aware build/test matrices.
- Use this skill for generated sources, generated build products, plugin sandboxing, write access, or network permissions.
- Use this skill when the Swiftly-selected toolchain and Xcode-selected toolchain may differ.
- Recommend `swift-package-build-run-workflow` for ordinary manifests, dependencies, resources, builds, and executable runs.
- Recommend `swift-package-testing-workflow` when ordinary test organization or failure diagnosis is primary.
- Recommend `format-swift-sources` for formatter-specific plugin operation after this skill establishes plugin permissions and ownership.
- Recommend `xcode-build-run-workflow` or `xcode-testing-workflow` when schemes, destinations, app hosts, Xcode project context, or Xcode-only evidence controls the result.
- Recommend `explore-apple-swift-docs` when the task is documentation lookup rather than package mutation or execution.

## Single-Path Workflow

1. Inspect `Package.swift`, `Plugins/`, macro targets, generated outputs, test targets, and any Xcode project or workspace markers.
2. Establish both toolchain identities before planning commands:
   - Swiftly path: `swiftly use --print-location`, `swift --version`, and relevant `swift package`, `swift build`, or `swift test` help.
   - Xcode path: `xcode-select -p`, `xcrun --find swift`, `xcrun swift --version`, and matching `xcrun swift package`, build, or test help.
   - If Swiftly is set to `xcode`, record that bridge explicitly instead of presenting the two command paths as independent compiler distributions.
   - Do not assume the two toolchains expose identical SwiftPM commands, flags, manifest APIs, macro support, or plugin behavior.
3. Read the relevant official SwiftPM, Swift Evolution, or Apple/Xcode documentation and state the behavior relied on before editing.
4. Classify the primary extension concern as `build-tool-plugin`, `command-plugin`, `macro`, `traits`, or `generated-source`.
5. Run `scripts/run_workflow.py` for repo-shape inspection and a non-mutating command plan.
6. Load only the reference needed for the selected concern:
   - plugins: `references/package-plugins-build-command-and-xcode.md`
   - permissions: `references/plugin-permissions-sandbox-and-outputs.md`
   - macros: `references/swift-macros-package-shape.md`
   - traits: `references/package-traits-feature-flags.md`
   - generated files: `references/generated-source-and-build-products.md`
7. Use `references/cli-command-matrix.md` to keep Swiftly and Xcode commands distinct.
8. Apply `references/xcode-handoff-conditions.md` before using Xcode-managed execution or changing Xcode-owned project state.
9. Validate the smallest relevant matrix first, then the supported Swift minor window and both host toolchains when the package claims both.
10. Report the manifest/API floor, selected toolchain, commands run, generated or permission-sensitive outputs, and any handoff.

## Inputs

- `extension_type`: `build-tool-plugin`, `command-plugin`, `macro`, `traits`, or `generated-source`.
- `request`: optional natural-language request used to infer `extension_type`.
- `repo_root`: package path; defaults to the current directory.
- `toolchain_scope`: `swiftly`, `xcode`, or `both`; defaults to `both` for Apple ecosystem compatibility work.
- `mixed_root_opt_in`: allow package-first planning when Xcode markers share the package root.

## Outputs

- `status`: `success`, `handoff`, or `blocked`.
- `path_type`: `primary` or `fallback`.
- `output`: extension type, repo shape, toolchain scope, planned commands, evidence requirements, and one next step.

## Guards and Stop Conditions

- Stop when the package root or `Package.swift` cannot be resolved.
- Stop before raising the tools-version or manifest API floor without confirming the package support window.
- Keep beta or snapshot toolchain evidence separate from the latest-stable-plus-previous-stable support promise.
- Do not treat `swift --version` as evidence for the Xcode toolchain; inspect `xcrun swift --version` separately.
- Do not disable the plugin sandbox as a routine workaround. Name the required capability and grant the narrowest permission.
- Do not let build tool plugins modify package sources; generate into plugin-controlled build output locations.
- Do not check in derived output merely to hide a nondeterministic generator.
- Do not use traits to remove API when enabled; design traits as additive feature choices.
- Stop with a handoff when Xcode project context, scheme/destination state, app-hosted execution, or project membership determines correctness.

## Fallbacks and Handoffs

- Fall back to a command plan when execution would mutate the package or request permissions the user did not authorize.
- Hand ordinary package execution to `swift-package-build-run-workflow` after extension shape and flags are settled.
- Hand ordinary test diagnosis to `swift-package-testing-workflow`; retain ownership of macro/plugin test shape and trait matrices.
- Hand Xcode-managed builds to `xcode-build-run-workflow` and Xcode-native tests to `xcode-testing-workflow` with the exact package, plugin, macro, trait, scheme, and destination context.
- Use `format-swift-sources` for formatter-specific behavior without duplicating the general plugin permission model.

## Customization

- Use `references/customization.template.yaml` and `references/customization-flow.md`.
- `scripts/customization_config.py` stores and reports customization state.
- The workflow currently keeps fixed package-first and least-permission defaults.

## References

### Workflow References

- `references/package-plugins-build-command-and-xcode.md`
- `references/plugin-permissions-sandbox-and-outputs.md`
- `references/swift-macros-package-shape.md`
- `references/package-traits-feature-flags.md`
- `references/generated-source-and-build-products.md`
- `references/xcode-handoff-conditions.md`
- `references/cli-command-matrix.md`

### Contract References

- `references/customization.template.yaml`
- `references/customization-flow.md`

### Support References

- Recommend `references/snippets/apple-swift-package-core.md` when reusable package policy is needed in an end-user repo.
- `references/snippets/apple-swift-package-core.md`

### Script Inventory

- `scripts/run_workflow.py`
- `scripts/customization_config.py`
