# Focus, Layout, and Input

Apple TV is an indirect-input platform. A person uses the Siri Remote, a game
controller, voice, or a companion device; focus communicates which control will
receive selection. Focus is not merely an accessibility decoration and it is
not a cursor the app should direct around a menu.

## SwiftUI-First Layout

For normal shelves and catalog screens, use native focusable controls and leave
SwiftUI room to animate the focused item. A shelf needs unclipped scrolling,
spacing around lockups, and labels that remain readable while artwork enlarges.
Use `focusSection()` when a broad visual region must provide a reliable route to
its children; do not use it as a substitute for a coherent layout.

Large, fixed grids are fragile. On tvOS 27, Large Text can require fewer
columns, a different lockup aspect, or a vertical presentation. Use text styles
and the dynamic type environment rather than fixed font sizes and rigid height
constraints.

## UIKit Escape Hatch

Use `UIFocusGuide` when a geometrically valid directional move has no nearby
candidate but a specific destination is semantically correct. Use preferred
focus environments when a container should nominate its initial or restored
child. The app may request focus reevaluation after a state change, but it must
not attempt to issue a directional focus command on the person's behalf.

## Input Boundaries

- Preserve `Menu`/Back as a predictable retreat or dismissal action.
- Test both Siri Remote and controller input if the app claims controller
  support; button mapping and navigation feel can differ.
- Provide an alternative to lengthy text entry. The tvOS keyboard is a costly
  interaction, not a neutral form field.
- In full-screen content, direct gestures toward content interaction rather
  than focus movement.
- Do not introduce a tiny free-form pointer for ordinary navigation.
