# System Surfaces And Validation

Choose the system surface after the action/entity contract is clear.

- Siri, Spotlight, and Shortcuts need actions and content that remain understandable without the app already open.
- Spotlight indexing should expose only content the user can legitimately open after the app launches.
- Widgets, controls, and Live Activities need their own extension and lifecycle validation; an intent declaration in the main app is not proof of their behavior.
- Hardware-triggered actions need an explicit availability and safety review; do not turn a destructive app action into a one-press system action without confirmation or reversible behavior.

Validate the exact surface: discovery, phrase or parameter resolution, cancellation, error reporting, result presentation, app handoff, and any privacy/authentication boundary. Test on the target OS and device class when the system owns discovery or presentation.
