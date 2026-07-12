# Intent, Entity, And Shortcut Shapes

Apple documents an app intent as an app action expressed to the system. Start from a real action people recognize, then choose the narrowest shape.

| Need | Preferred shape | Boundary |
| --- | --- | --- |
| Run a self-contained action | `AppIntent` | `perform()` delegates to the domain action or app handoff. |
| Select or search app-owned content | `AppEntity` plus an appropriate entity query | Keep stable identity and display data in the entity; retain domain ownership elsewhere. |
| Offer a repeatable phrase/action | `AppShortcutsProvider` | Ship only a small set of high-value shortcuts. |
| Show result or request confirmation visually | intent result snippet | Keep the snippet focused on intent output; it is not a replacement app screen. |

Prefer app intent templates when Apple provides a type that matches the action. Otherwise, model only the parameters, confirmation, and result information the system needs.

Do not mirror a feature service into a separate intent manager. The intent may call the same narrow operation the app uses, and should return a clear result or error when that operation cannot complete.
