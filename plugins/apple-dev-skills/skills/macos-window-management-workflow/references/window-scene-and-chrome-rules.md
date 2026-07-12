# Window Scene and Chrome Rules

Xcode-local SwiftUI documentation checked on 2026-07-12 makes the following distinctions:

- `WindowGroup` represents a group of windows and its title contributes to the New and Window menus, title bar, and window identification.
- `Window`, `Settings`, and `DocumentGroup` each describe a narrower scene responsibility; choose the scene shape before styling it.
- SwiftUI's macOS window customization APIs support toolbar visibility/background changes, `WindowDragGesture`, zoom placement, and restoration behavior. Apple documents these customizations for macOS 15 and later, so availability must match the app's deployment target.
- A hidden toolbar or background needs a usable drag region. `WindowDragGesture` can extend that region, while `allowsWindowActivationEvents(true)` permits an initial click-and-drag to activate and move a background window.
- Removing visible title/chrome is visual only: the system still exposes a title to accessibility and the Window menu. Preserve a meaningful title rather than treating that as an excuse to omit one.

Sources read through Xcode-local documentation:

- `doc://com.apple.documentation/documentation/SwiftUI/Customizing-window-styles-and-state-restoration-behavior-in-macOS`
- `doc://com.apple.documentation/documentation/SwiftUI/Windows`
- `doc://com.apple.documentation/documentation/SwiftUI/WindowGroup`
