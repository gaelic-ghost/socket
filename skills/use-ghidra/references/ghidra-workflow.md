# Ghidra Workflow Reference

## Project Record

- Ghidra and Java versions.
- Release source and installed extensions.
- Project type, path, and archive status.
- Artifact hash and import name.
- Loader, language, compiler specification, image base, and memory map.
- Analyzer names, options, and analysis timestamps.
- Symbol, type-library, script, and external-library inputs.
- Comments, bookmarks, function edits, data types, and renames.

## Interactive And Automated Boundaries

Use CodeBrowser for interactive navigation, annotation, typing, graphs, and decompiler comparison. Use scripts, PyGhidra, or headless analysis for repeatable queries, batch import, controlled analyzers, and structured exports. Record which surface produced each observation.

Use `analyzeHeadless` for a deterministic project-and-script workflow, not as a replacement for recording loader and analyzer choices. Preserve its command arguments, project state, logs, script source, and structured outputs. Use PyGhidra when a Python query or transformation is the smallest useful automation surface; record the Python environment as well as the Ghidra release.

When a script changes program state, record the before/after project state and treat it as an analysis transformation. Keep a read-only or archived checkpoint before bulk edits.

## Security Checks

Ghidra's canonical repository warns that some versions have known vulnerabilities. Check the current advisory list before processing hostile artifacts, keep releases isolated rather than overlaying installations, and limit extension sources. Analyze untrusted inputs in a constrained working environment appropriate to the risk.

## Canonical Sources

- [Ghidra repository](https://github.com/NationalSecurityAgency/ghidra)
- [Ghidra releases](https://github.com/NationalSecurityAgency/ghidra/releases)
- [Ghidra security advisories](https://github.com/NationalSecurityAgency/ghidra/security/advisories)
- [Ghidra documentation tree](https://github.com/NationalSecurityAgency/ghidra/tree/master/GhidraDocs)

Use the Getting Started and help content shipped with the installed release for version-specific UI, headless, script, and analyzer behavior.
