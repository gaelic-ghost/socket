# CLI Command Matrix

Run one toolchain at a time and preserve the prefix in captured evidence.

| Concern | Swiftly-selected toolchain | Xcode-selected toolchain |
| --- | --- | --- |
| Identity | `swiftly use --print-location`; `swift --version` | `xcode-select -p`; `xcrun --find swift`; `xcrun swift --version` |
| Plugin templates | `swift package init --type build-tool-plugin`; `swift package init --type command-plugin` | `xcrun swift package init --type build-tool-plugin`; `xcrun swift package init --type command-plugin` |
| Plugin discovery | `swift package plugin --list` | `xcrun swift package plugin --list` |
| Plugin execution | `swift package plugin [permissions] <verb>` | `xcrun swift package plugin [permissions] <verb>` |
| Macro template | `swift package init --type macro` | `xcrun swift package init --type macro` |
| Trait inventory | `swift package show-traits`; add `--format json` for automation | `xcrun swift package show-traits`; add `--format json` for automation |
| Trait build | `swift build --traits A,defaults`; `swift build --disable-default-traits`; `swift build --enable-all-traits` | Same flags through `xcrun swift build`, after checking help |
| Trait tests | `swift test --traits A,defaults`; `swift test --disable-default-traits`; `swift test --enable-all-traits` | Same flags through `xcrun swift test`, after checking help |

Do not rewrite an Xcode command as a `DEVELOPER_DIR=` override. Use the configured Xcode command-line tools selection.
Run `swift package init` templates only in disposable empty directories. If Swiftly reports that it is using Xcode, label the Swiftly row as an Xcode bridge rather than independent Swift.org-toolchain evidence. Keep beta or snapshot Xcode results outside the stable support window until that Swift minor is released.
