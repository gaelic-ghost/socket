# Framework Bridging: UIKit and AppKit

## Why the bridge matters

- SwiftUI can host UIKit and AppKit views through `UIViewRepresentable` and `NSViewRepresentable`.
- When SwiftUI wraps a platform-native view, accessibility correctness depends on both the SwiftUI wrapper surface and the underlying UIKit or AppKit accessibility information.

## UIKit

- UIKit accessibility behavior is shaped through `UIAccessibility` and related view properties such as labels, values, hints, traits, and custom actions.
- If the wrapped UIKit view already has correct accessibility information, keep the SwiftUI wrapper from obscuring or duplicating it.
- If the wrapped UIKit control does not expose the needed semantics, fix the UIKit surface rather than trying to paper over everything from the outer SwiftUI wrapper.

### Worked example: avoid duplicate SwiftUI labels around a UIKit control

- If a wrapped UIKit view already exposes the right accessibility label and value, do not add a second outer SwiftUI label unless the wrapper is intentionally replacing that contract.

## AppKit

- AppKit accessibility behavior is shaped through `NSAccessibility`.
- AppKit controls often need more explicit accessibility attention because desktop interaction models and focus behavior can differ meaningfully from iOS expectations.
- When a SwiftUI wrapper hosts an AppKit view, make sure the native role, label, value, and actionable behavior remain discoverable to assistive technologies.

### Worked example: keep AppKit role semantics in the hosted view

- If a SwiftUI wrapper hosts a custom `NSView`, prefer setting the AppKit accessibility role, label, and value on that `NSView` when those semantics are native to the hosted control instead of inventing a parallel description one layer up.

## Review questions

- Is the accessibility contract authored in the right layer?
- Is SwiftUI duplicating or fighting the underlying platform-native accessibility description?
- Does the wrapper preserve the role and state the user actually experiences?
