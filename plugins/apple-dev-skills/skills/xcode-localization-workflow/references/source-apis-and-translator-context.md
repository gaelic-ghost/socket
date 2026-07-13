# Source APIs and Translator Context

## Select the API from the output you need

| Need | Preferred shape |
| --- | --- |
| SwiftUI text in a view | `Text("Continue", comment: "Moves to the next setup step")` |
| Resolved Foundation string | `String(localized: "Welcome, \\(name)!", comment: "Greeting on the account screen")` |
| Localized attributed or Markdown text | `AttributedString(localized: "Read the [guide](...)" )` |
| Deferred resource for an API/process boundary | `LocalizedStringResource("Retry", comment: "Retries the failed upload")` |
| Explicit stable key and evolving default | `String(localized: "settings.signOut", defaultValue: "Sign Out", comment: "Account menu action")` |

For a named catalog, use `tableName` in SwiftUI and `table` in Foundation. For framework or Swift Package resources, use the owning bundle. A source call must contain static extractable values; Xcode cannot discover a key, table, default, or comment assembled at runtime.

## Good source shape

```swift
Text("\\(itemCount) saved items", comment: "Count shown in the Saved tab")

let message = String(
    localized: "Unable to save \\(documentName).",
    table: "Errors",
    bundle: .module,
    comment: "Error after a document save request fails"
)
```

The first entry lets the catalog model plural categories. The second tells Xcode, translators, and future maintainers which catalog and resource bundle own the text.

## Context is part of the interface

Comments should explain what a translator cannot infer from the words alone: control role, surrounding screen, placeholder meaning, grammatical gender, character limit, product terminology, and whether a name stays untranslated. A generated screenshot can add visual context to an XLIFF handoff, but it does not replace a concise source comment or a project glossary.

Apple documents the Foundation localizable initializers and their comments in [Preparing your app's text for translation](https://developer.apple.com/documentation/xcode/preparing-your-apps-text-for-translation), and documents catalog-generated `LocalizedStringResource` symbols in [Using generated localizable symbols in your code](https://developer.apple.com/documentation/xcode/using-generated-localizable-symbols-in-your-code).
