# Malimite Workflow Reference

## Verified Positioning

Malimite is an Apple-focused package analysis interface built around Ghidra headless decompilation. Its useful surface includes IPA and bundle-oriented import, executable discovery from bundle metadata, resource and provisioning views, class and function navigation, strings, references, and heuristic Swift and Objective-C presentation.

Do not assume:

- reliable bare Mach-O input
- direct `.app` selection in every build
- decryption or encryption preflight
- bulk decompiled-source export
- pinned compatibility with every Ghidra release
- complete FAT64, `arm64e`, PAC, chained-fixup, or current-beta behavior
- source reconstruction from Swift heuristics or LLM translation

## Current Failure Routing

- Bare Mach-O: use Cutter, Ghidra, or Hopper.
- `.app` picker failure: try drag and drop, then a copied ZIP wrapper.
- Encrypted executable: stop and obtain an analyzable working artifact through the owning acquisition workflow.
- Ghidra analyzer or bridge failure: record versions and logs; test the exact supported option set.
- Need symbols, graphing, analyzer control, scripting, patching, or persistent Ghidra state: use the direct tool adapter.

## Generated State

Preserve the adjacent Malimite project directory, `project.json`, SQLite database, screenshots, and selected excerpts. Record the input hash and exact versions because the temporary Ghidra project may not remain available after Malimite analysis.

## Security And Privacy

Current source research found the Ghidra bridge using an unauthenticated socket range without an explicit loopback bind. Confirm the active listener in the installed build and prefer offline or firewall isolation for hostile artifacts.

Optional hosted-model actions transmit selected generated code. Record the destination, model, source method, and settings. Prefer a local model or omit the feature for sensitive material. Do not rely on the built-in credential storage as Keychain-grade protection.

## Canonical Sources

- [Malimite repository](https://github.com/LaurieWired/Malimite)
- [Malimite releases](https://github.com/LaurieWired/Malimite/releases)
- [Malimite wiki](https://github.com/LaurieWired/Malimite/wiki)
- [Supported formats documentation](https://lauriewired-malimite.mintlify.app/reference/supported-formats)
- [Bare Mach-O issue](https://github.com/LaurieWired/Malimite/issues/7)
- [App-bundle picker issue](https://github.com/LaurieWired/Malimite/issues/16)
- [Export request](https://github.com/LaurieWired/Malimite/issues/26)
- [Ghidra compatibility issue](https://github.com/LaurieWired/Malimite/issues/17)

Reconcile generated documentation against live source and issues when they disagree.
