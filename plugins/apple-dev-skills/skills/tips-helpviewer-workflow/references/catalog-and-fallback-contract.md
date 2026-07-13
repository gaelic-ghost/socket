# Tips HelpViewer Catalog and Fallback Contract

## Observed Mac Surface

On 2026-07-13, `com.apple.helpviewer` opened a window titled Tips with a search field, catalog headings, and task-specific Apple-app results. The same machine's `com.apple.tips` app was an empty shell, so the HelpViewer bundle is the primary local UI target.

The HelpViewer catalog search `Compressor export movie` produced a `Compressor User Guide` heading and Compressor-specific results, including built-in presets and caption export. The installed Compressor Creator Studio app reported version 5.3. This establishes a usable discovery fixture, not universal coverage or version authority for every topic.

## Match Contract

| Check | Required evidence | Result when absent |
| --- | --- | --- |
| Installed app | Product name and installed version | `unavailable` |
| Catalog guide | Guide heading names the requested app | `unavailable` |
| Task result | Topic is about the requested Mac task | `incomplete` |
| Answer source | Report the UI or fallback source actually inspected | `incomplete` |

Do not treat a generic Apple app name, a related product, a stale browser tab, or an uninspected release note as an exact guide match.

## Fallback Contract

Use a single next source rather than blending results:

1. Use the app's in-app Help for current operator guidance when it is available.
2. Use `explore-apple-swift-docs` for Apple developer APIs and documentation-source routing; prefer Xcode-local documentation, then Dash, before web sources.
3. Use the applicable app workflow for a task that needs an actual project, library, device, build, test, or export action.
4. Use readable official vendor documentation only when the local authoritative path is unavailable or incomplete.

Record why the handoff occurred and do not represent fallback content as a HelpViewer result.
