# String Catalog Foundations

## What a catalog solves

An Xcode String Catalog is a versioned `.xcstrings` source file that keeps a development-language string, its translations, state, and supported variations together. Xcode updates it from recognized localizable APIs during a build. It is the right default for current Xcode projects because it keeps source extraction, language coverage, plural forms, device-specific wording, and translation editing in one reviewed artifact.

It does not replace internationalization. The source must still pass full sentences, typed values, and meaningful context to localizable APIs; dates, numbers, measurements, lists, and names must still use locale-aware Foundation formatting; and the UI must still accommodate translated length and direction.

## Minimal adoption sequence

1. Add a String Catalog from Xcode's Resource template, normally named `Localizable.xcstrings`.
2. Build each target that owns user-visible strings.
3. Inspect new extracted entries, source locations, and comments.
4. Add each requested language or language-and-region variant.
5. Translate directly or export/import an Xcode Localization Catalog (`.xcloc`).
6. Review translation state and the source-control diff.
7. Test the running app in each relevant locale and layout direction.

## Variations

For a count, localize one interpolated sentence and add plural variants in the catalog. Xcode supplies the plural categories for each language; a language can have categories beyond English's one and other. Add a device variant only when product wording is intentionally different on that device class. Do not use a device variant to conceal clipped text, and do not use a plural variant for arbitrary conditional copy.

## Source evidence

Apple documents the catalog setup, build-based extraction, language/region additions, comments, tables, plurals, device variants, and translation state in [Localizing and varying text with a string catalog](https://developer.apple.com/documentation/xcode/localizing-and-varying-text-with-a-string-catalog). Apple identifies String Catalogs as the recommended Xcode 15-and-later plural-localization path in [Localizing strings that contain plurals](https://developer.apple.com/documentation/xcode/localizing-strings-that-contain-plurals).
