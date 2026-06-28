# Symbol Selection and Rendering

Use this reference when the SF Symbols workflow needs concrete symbol choice, rendering, variant, variable-value, or accessibility guidance.

## Selection Rules

- Start from the intended meaning, not from a visually neat glyph.
- Prefer a built-in SF Symbol when it matches the user's action, state, object, or category and is available on the target platforms.
- Use the SF Symbols app to verify exact names, variants, categories, rendering support, variable behavior, and animation support when the task depends on current library details.
- Prefer a standard variant such as fill, slash, circle, square, or badge when the state is conventional and the variant exists.
- Prefer custom symbols only when a built-in symbol cannot carry the app-specific meaning or brand shape.
- Prefer ordinary vector artwork when the art is illustrative, complex, logo-like, or not intended to inherit SF Symbols metrics and rendering behavior.

## Rendering Rules

- Use monochrome when the symbol should inherit one semantic foreground style.
- Use hierarchical when one tint should create layered emphasis.
- Use palette when the app needs controlled multi-layer colors.
- Use multicolor when the built-in or custom symbol has meaningful inherent colors and Apple documents or the SF Symbols app confirms support.
- Use variable value when the symbol communicates progress, strength, amount, or signal with a continuous value.
- Verify rendering support in the SF Symbols app when visual behavior matters. If a symbol does not support the requested mode, the system may fall back to a simpler rendering behavior.

## SwiftUI Implementation Notes

- Use `Image(systemName:)` or `Label` for built-in symbols.
- Use `symbolRenderingMode(_:)` to choose the symbol rendering mode when the default is not right.
- Use `foregroundStyle(_:)` for hierarchical and palette styling.
- Use `symbolVariant(_:)` when applying a supported variant through the environment is clearer than hard-coding a variant name.
- Use symbol effects only when the motion is symbol-local and the target platform supports the effect.
- Keep symbol names centralized when the same semantic action appears in several views.

## UIKit and AppKit Notes

- Use framework symbol image APIs rather than importing copied artwork for built-in symbols.
- Use symbol configuration APIs for point size, weight, scale, rendering mode, palette colors, or multicolor preferences.
- Confirm platform availability before using newer symbol features in shared code.

## Accessibility Notes

- Give symbols semantic labels when the surrounding UI does not already provide the accessible name.
- Hide purely decorative symbols from accessibility when the adjacent text or control label already communicates the meaning.
- Do not use color alone to communicate status. Pair the symbol with shape, text, control state, or an accessibility label.
- Avoid choosing a clever symbol whose metaphor is likely to be unclear in VoiceOver or localization contexts.

## Common Failure Modes

- Misspelled symbol names.
- Choosing a symbol that exists in SF Symbols but is unavailable on the app's deployment target.
- Assuming every symbol has fill, slash, badge, palette, multicolor, variable, or animation support.
- Applying palette colors in an order that does not match the symbol's layer annotations.
- Using symbol motion for a state change that should be communicated in static UI as well.
