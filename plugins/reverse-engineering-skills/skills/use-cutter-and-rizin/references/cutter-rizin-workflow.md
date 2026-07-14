# Cutter And Rizin Workflow Reference

## Capability Record

- Cutter version and build identifier.
- Rizin version and libraries exposed inside Cutter.
- Working standalone Rizin version and resolved executable when used.
- Direct-launch result for any CLI executable found inside the app bundle; file presence alone is not CLI availability.
- Available decompiler and analysis plugins.
- Loader, architecture, debugger, Python, and `rzpipe` availability.
- Project/database path and selected analysis preset.

## GUI To CLI Handoff

Use Cutter for exploration and Rizin for repeatable questions. Translate a GUI observation into a command only after recording the same image, slice, base address, analysis state, and symbol inputs. Prefer structured output when the installed command supports it.

If Cutter's bundled CLI fails before analysis because of loader paths, signing, or packaging, preserve that failure and use Cutter's integrated surface or a separately installed working Rizin. Do not rewrite the application bundle, bypass platform protections, or report bundled libraries as successful CLI evidence.

Useful Rizin tool families include binary properties, analysis, strings, symbols, sections, imports, exports, references, disassembly, graphs, hashes, diffs, and scripting. Read installed help or the current handbook instead of embedding a large command catalog that will drift.

## Apple Boundaries

Complement Cutter/Rizin with `file`, `lipo`, `otool`, `vtool`, `nm`, `dwarfdump`, `codesign`, `dyld_info`, and the focused Apple skills. Explicit uncertainty sources include:

- encrypted App Store executables
- optimized or stripped Swift
- Objective-C runtime ownership reconstructed from partial metadata
- `arm64e` pointer authentication and tagged addresses
- chained fixups and dyld shared-cache images
- hardened, sandboxed, or device-only debugging

## Evidence Practice

Keep an original-name to proposed-name map with evidence and confidence. Store project files, screenshots, exports, scripts, and console output as generated analysis state. Export the smallest excerpt needed for a finding rather than whole pseudocode listings.

## Canonical Sources

- [Cutter](https://cutter.re/)
- [Cutter source](https://github.com/rizinorg/cutter)
- [Rizin handbook](https://book.rizin.re/)
- [Rizin source](https://github.com/rizinorg/rizin)
- [rz-ghidra](https://github.com/rizinorg/rz-ghidra)

Check the installed build and current release documentation before claiming a plugin or debugger is available.
