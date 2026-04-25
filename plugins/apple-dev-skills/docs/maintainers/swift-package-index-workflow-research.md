# Swift Package Index Workflow Research

This note captures the current source-backed guidance for the planned Swift Package Index workflow skill.

## Listing A Package

The supported path for getting an ordinary Swift package listed on Swift Package Index is the hosted Add a Package flow, which opens an issue in [`SwiftPackageIndex/PackageList`](https://github.com/SwiftPackageIndex/PackageList/issues/new/choose).

Agents should not tell maintainers to start by hand-editing `packages.json` in a fork. `packages.json` remains the canonical backing list, but the public Add Package flow collects package repository URLs in an issue and the PackageList automation opens the pull request that updates `packages.json`.

Use this practical sequence for a first listing:

1. Confirm the package satisfies the public SPI requirements from [Add a Package](https://swiftpackageindex.com/add-a-package) and the [`PackageList` README](https://github.com/SwiftPackageIndex/PackageList).
2. Use a public GitHub repository URL with the protocol and `.git` suffix, for example `https://github.com/owner/package.git`.
3. Submit one URL per line through the Add Package issue form.
4. Wait for the PackageList automation to validate the issue body and open the generated pull request.
5. After the package appears on SPI, use the package page's maintainer flow to claim the package and copy SPI's generated compatibility badges if the repository wants them.

The Add Package issue template currently accepts a free-form textarea named `New Packages` and asks for one repository URL per line. The issue workflow then runs `add_package.swift`, validates the updated package list, and creates a pull request that changes `packages.json` when there is real work to do.

## Requirements To Check Before Submission

Before recommending submission, verify the package against the live SPI requirements:

- The repository is publicly accessible.
- `Package.swift` exists at the repository root.
- The package is written in Swift 5.0 or later.
- The package has at least one semantically versioned release tag.
- `swift package dump-package` emits valid JSON with the latest Swift toolchain available to the maintainer.
- The package URL includes a protocol, usually `https`, and the `.git` suffix.
- The package compiles.
- The package content complies with SPI's code of conduct.

The current PackageList issue template also states that each package must contain at least one product and at least one product must be usable from other Swift apps. Keep that check in the workflow skill even though the shorter public Add Package page does not currently show it in the same list.

## Package Collections Are Separate

Do not confuse SPI listing with Swift package collections.

Package collections are a discovery and curation surface for packages that are already known to consumers. Swift Package Index dynamically provides author or organization collections, and SwiftPM can add them with `swift package-collection add`.

SPI also supports custom package collections for community-maintained lists, but that is not the ordinary way to get a single package indexed. Custom collections are proposed by adding a collection index URL to `custom-package-collections.json`; SPI then matches collection package URLs against packages already known to the index.

## Skill Boundary

The future SPI workflow skill should own:

- listing readiness checks
- Add Package issue-flow guidance
- `.spi.yml` and DocC hosting readiness handoff
- package page review after SPI ingestion
- maintainer claim and badge follow-through
- package collection clarification when users ask for curated package lists

It should not replace the core Swift package build and testing skills. For compile, test, and `dump-package` verification, hand off to the existing Swift package execution workflows.

## Source Notes

- [Swift Package Index Add a Package](https://swiftpackageindex.com/add-a-package)
- [`SwiftPackageIndex/PackageList` README](https://github.com/SwiftPackageIndex/PackageList)
- [`SwiftPackageIndex/PackageList` Add Package issue template](https://github.com/SwiftPackageIndex/PackageList/blob/main/.github/ISSUE_TEMPLATE/add_package.yml)
- [`SwiftPackageIndex/PackageList` issue automation](https://github.com/SwiftPackageIndex/PackageList/blob/main/.github/workflows/issues.yml)
- [`SwiftPackageIndex/PackageList` add-package script](https://github.com/SwiftPackageIndex/PackageList/blob/main/.github/add_package.swift)
- [Swift Package Index Package Collections](https://swiftpackageindex.com/package-collections)
- [Swift.org Package Collections](https://www.swift.org/blog/package-collections/)
- [Swift Package Index custom package collections announcement](https://swiftpackageindex.com/blog/introducing-custom-package-collections)
