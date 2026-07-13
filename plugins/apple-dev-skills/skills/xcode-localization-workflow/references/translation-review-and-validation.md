# Translation Review and Validation

## Translation handoff

Use the catalog editor for small, directly reviewed language updates. For a localization service or language reviewer, export Xcode localizations as an `.xcloc` package, include the glossary and relevant screenshots, and import only the reviewed result. Check the import comparison editor and the repository diff before accepting the change.

Track, for every language and region:

- source language and catalog/table owner;
- translator or translation-service provenance;
- reviewer identity or explicit review gap;
- terminology and non-translatable names;
- unresolved entries, placeholder errors, and source changes after translation.

## Validation matrix

Run the narrowest relevant build and tests first, then inspect the app with the target language and region active. Cover at least the changed entry points plus:

- long labels and buttons at normal and large Dynamic Type sizes;
- plural values that exercise each meaningful form;
- date, number, measurement, currency, list, and name formatting;
- empty, loading, success, error, and destructive-confirmation states;
- a right-to-left language when the product supports one;
- compact and regular device classes when wording or layout differs.

Keep automated tests and visual inspection distinct. A test can prove a formatting or lookup contract; it cannot establish terminology quality, clipped text, bidirectional mirroring, or cultural suitability.

Apple documents localization export and import in [Exporting localizations](https://developer.apple.com/documentation/xcode/exporting-localizations) and [Importing localizations](https://developer.apple.com/documentation/xcode/importing-localizations).
