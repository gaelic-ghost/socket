# Structure Swift Sources Glossary

- `feature`: a user-visible capability or cohesive product area, such as authentication, search, playback, or settings
- `layer`: a technical slice such as `API`, `Features`, `Models`, `Views`, or `Controllers`
- `concern`: one cohesive responsibility inside a file or directory, such as networking models, persistence adapters, SwiftUI view modifiers, or validation helpers
- `section group`: a declaration cluster inside one file, separated with `// MARK:` headings
- `file header`: the block-comment summary near the top of a managed Swift file that explains its purpose and concern in plain terms

Use `feature` language when grouping by product capability.
Use `layer` language when grouping by technical role.
Use `concern` language when deciding whether code should stay in one file or split into an extracted extension file.
