# Transitions, Effects, and Accessibility

Use this reference when SwiftUI animation work touches transitions, symbol effects, reduce motion, or user comfort.

## Transition Rules

- Use insertion/removal transitions only when the view identity actually appears or disappears.
- Use content transitions for text, number, image, and symbol changes inside a stable view.
- Use matched geometry when the user should perceive the same item moving between layouts.
- Use navigation transitions when the motion is tied to navigation and the target OS supports the API.
- Keep fallback behavior acceptable when a platform does not support the desired transition.

## Symbol Effects

- Treat symbol effects as SwiftUI motion only after the symbol choice and rendering behavior are valid.
- Verify effect availability and support in Apple docs or the SF Symbols app.
- Use `sf-symbols-workflow` when the task is mainly about choosing the symbol, rendering mode, variable color, custom symbol, or effect support.
- Use this skill when the task is mainly about how the symbol effect participates in broader SwiftUI state or transition behavior.

## Reduce Motion and Comfort

- Check whether motion communicates required meaning. If yes, provide static text, shape, or state fallback.
- Respect reduce-motion expectations by disabling, simplifying, or replacing large spatial motion where appropriate.
- Avoid repeated decorative motion in dense productivity UI unless it serves a clear purpose.
- Prefer short, responsive feedback for controls.
- Prefer continuity over spectacle in navigation and layout changes.

## Validation Notes

- Xcode previews are useful for tuning phase and keyframe values.
- Simulator or device validation is better for interaction timing, navigation transitions, performance, and reduce-motion behavior.
- Screenshots cannot prove motion quality. Use them only for static before/after evidence.
- Report manual-validation gaps plainly when haptics, device feel, refresh rate, or comfort cannot be validated in the current environment.
