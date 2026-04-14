# SwiftFormat for Xcode Config Export

Authoritative sources:

- [SwiftFormat README](https://github.com/nicklockwood/SwiftFormat/blob/main/README.md)
- [SwiftFormat AppDelegate.swift](https://github.com/nicklockwood/SwiftFormat/blob/main/EditorExtension/Application/Source/AppDelegate.swift)
- [SwiftFormat OptionsStore.swift](https://github.com/nicklockwood/SwiftFormat/blob/main/EditorExtension/Shared/OptionsStore.swift)
- [SwiftFormat RulesStore.swift](https://github.com/nicklockwood/SwiftFormat/blob/main/EditorExtension/Shared/RulesStore.swift)

## Preferred Supported Path

Use the `SwiftFormat for Xcode` host app and choose `File > Export Configuration`.

Why this is the preferred path:

- It is the tool's supported export workflow.
- It serializes the currently loaded host-app configuration into a normal SwiftFormat config file.
- It matches the upstream app behavior rather than depending on local reverse engineering.

## Deterministic Fallback Path

Use `scripts/export_swiftformat_xcode_config.py` when you need a scriptable export from the SwiftFormat shared defaults state.

Example:

```bash
skills/format-swift-sources/scripts/export_swiftformat_xcode_config.py --output .swiftformat
```

If `defaults export com.charcoaldesign.SwiftFormat -` does not produce a useful payload on the current machine, point the script at the actual shared plist inside the SwiftFormat group container instead:

```bash
skills/format-swift-sources/scripts/export_swiftformat_xcode_config.py \
  --input-plist "/path/to/SwiftFormat-group-container/.../com.charcoaldesign.SwiftFormat.plist" \
  --output .swiftformat
```

The script reconstructs a config file from:

- `rules`
- `format-options`
- `infer-options`

## Behavioral Notes

- When `infer-options` is enabled, the host app intentionally avoids exporting the full option set. The script mirrors that behavior by exporting only explicit Swift-version or language-mode values plus the selected rules.
- The script produces an explicit, deterministic config file. It is optimized for reproducibility and reviewability rather than minimal diff size.
- In practice, the real shared plist in the SwiftFormat group container is often a more reliable source than the defaults-domain export path when you are trying to capture what the extension is actually using.
- Treat the generated `.swiftformat` as a starting point for repository config. Review it before checking it in, because extension state may include stale alias keys or other values that do not belong in a portable repo config.
- If the host app cannot see the current project config automatically, export the file, add it to the project root, then re-import it into the host app when you want the extension to use that config again.
