# Swift Package Index Workflow Research

This note captures the current source-backed guidance for the planned Swift Package Index workflow skill.

## Listing A Package

The supported path for getting an ordinary Swift package listed on Swift Package Index is the hosted Add Package issue-form flow, which opens an issue in [`SwiftPackageIndex/PackageList`](https://github.com/SwiftPackageIndex/PackageList/issues/new/choose).

Agents must not tell maintainers to start by hand-editing `packages.json` in a fork. `packages.json` remains the canonical backing list, but the public Add Package issue form collects package repository URLs in an issue and the PackageList automation owns any downstream pull request that updates `packages.json`.

Agents must also not create PackageList issues with `gh issue create`, try to apply the `Add Package` label manually, fork or clone `SwiftPackageIndex/PackageList`, push PackageList branches, open PackageList pull requests, or trigger validation and CLA automation through a manual contribution path. The only supported external add-package action is submitting the official Add Package issue form.

Use this practical sequence for a first listing:

1. Confirm the package satisfies the public SPI requirements from [Add a Package](https://swiftpackageindex.com/add-a-package) and the [`PackageList` README](https://github.com/SwiftPackageIndex/PackageList).
2. Use a public GitHub repository URL with the protocol and `.git` suffix, for example `https://github.com/owner/package.git`.
3. Use the Socket add-package script or the documented GitHub UI to open the official Add Package issue form.
4. Submit one URL per line through the `New Packages` field.
5. After submitting, verify the created issue has the `Add Package` label. If it does not, report that the documented form path did not complete and stop.
6. After the package appears on SPI, use the package page's maintainer flow to claim the package and copy SPI's generated compatibility badges if the repository wants them.
7. Review the rendered README after the badge change so the badge row still fits the package's existing README preamble.

The live click path is:

1. Start at <https://swiftpackageindex.com/add-a-package>.
2. Click Add Package(s), which opens <https://github.com/SwiftPackageIndex/PackageList/issues/new/choose>.
3. Choose the Add Package(s) template, which opens <https://github.com/SwiftPackageIndex/PackageList/issues/new?template=add_package.yml>.

The Add Package issue template currently asks for a title shaped as `Add <Package>` and a free-form textarea named `New Packages`. Put each package repository URL on its own line in that textarea:

```text
https://github.com/owner/package.git
https://github.com/owner/another-package.git
```

The issue form defines the `Add Package` label. The issue workflow runs only when that label is present, then SPI's repository automation owns `add_package.swift`, validation, and any generated pull request. Agents must treat those downstream artifacts as SPI-owned implementation details, not as a fallback action surface.

## Socket Add-Package Automation

Socket ships a one-shot guardrail script for agents and maintainers:

```bash
uv run /Users/galew/Workspace/gaelic-ghost/socket/scripts/spi_add_package.py hands-free /path/to/package
```

The script performs repo-local readiness, validates the live PackageList issue-form shape, opens the prefilled official Add Package issue form, and prints a Codex Computer Use handoff. Browser-opening modes require complete readiness and reject skip flags. The default browser target is Zen by bundle id `app.zen-browser.zen`.

The hands-free path is intentionally narrow:

1. The script opens the prefilled official issue form.
2. Codex Computer Use confirms the page is the `SwiftPackageIndex/PackageList` `Add Package(s)` issue form.
3. Codex Computer Use confirms the `New Packages` field contains the package URL exactly once.
4. Codex Computer Use clicks GitHub's `Submit new issue` button.
5. Codex verifies the created issue has the `Add Package` label and reports the issue URL.

If any step fails, stop and report the failure. Do not recover by creating an issue with `gh`, adding labels, forking PackageList, editing `packages.json`, or opening a PackageList PR.

## Requirements To Check Before Submission

Before recommending submission, verify the package against the live SPI requirements:

- The repository is publicly accessible.
- `Package.swift` exists at the repository root.
- The package is written in Swift 5.0 or later.
- The package has at least one semantically versioned release tag visible on the public remote.
- `swift package dump-package` emits valid JSON with the latest Swift toolchain available to the maintainer and reports at least one product.
- The package URL includes a protocol, usually `https`, and the `.git` suffix.
- The package compiles.
- The package content complies with SPI's code of conduct.

The current PackageList issue template also states that each package must contain at least one product and at least one product must be usable from other Swift apps. Keep that check in the workflow skill even though the shorter public Add Package page does not currently show it in the same list.

## Compatibility Badges

SPI recommends adding shields.io compatibility badges to a package README after the package is listed. The practical job of these badges is to show consumers the current Swift-version and platform compatibility that SPI computes from its own build matrix.

Use the package page's `Do you maintain this package?` maintainer flow as the source of truth for badge Markdown. Do not ask maintainers to hand-roll badge URLs as the default path. The maintainer page currently provides separate badges for:

- Swift version compatibility, using `type=swift-versions`
- platform compatibility, using `type=platforms`

When adding badges to a README:

- prefer both badges when the README already has a badge row or package-status preamble
- link each badge back to the package page on `swiftpackageindex.com`
- place the badges with the existing badge group, before the first major README section
- keep CI, release, documentation, and license badges separate from SPI compatibility badges because they answer different maintainer and consumer questions
- verify the rendered README after editing, especially in repositories with screenshots, callouts, or long first-viewport introductions

This is the generated Markdown shape currently used by SPI, with the owner and repository filled in by the maintainer page:

```markdown
[![](https://img.shields.io/endpoint?url=https%3A%2F%2Fswiftpackageindex.com%2Fapi%2Fpackages%2FOWNER%2FREPO%2Fbadge%3Ftype%3Dswift-versions)](https://swiftpackageindex.com/OWNER/REPO)
[![](https://img.shields.io/endpoint?url=https%3A%2F%2Fswiftpackageindex.com%2Fapi%2Fpackages%2FOWNER%2FREPO%2Fbadge%3Ftype%3Dplatforms)](https://swiftpackageindex.com/OWNER/REPO)
```

Use that shape only as an explanation or fallback when the maintainer page is unavailable. For normal package work, copy the generated Markdown directly from SPI so repository, casing, and URL escaping match the live package page.

## Package Collections Are Separate

Do not confuse SPI listing with Swift package collections.

Package collections are a discovery and curation surface for packages that are already known to consumers. Swift Package Index dynamically provides author or organization collections, and SwiftPM can add them with `swift package-collection add`.

SPI also supports custom package collections for community-maintained lists, but that is not the ordinary way to get a single package indexed. Custom collections are proposed by adding a collection index URL to `custom-package-collections.json`; SPI then matches collection package URLs against packages already known to the index.

## Skill Boundary

The future SPI workflow skill should own:

- listing readiness checks
- Add Package issue-flow guidance
- Socket add-package script handoff
- `.spi.yml` and DocC hosting readiness handoff
- package page review after SPI ingestion
- maintainer claim and SPI-generated badge follow-through
- README badge placement and rendering review
- package collection clarification when users ask for curated package lists

It should not replace the core Swift package build and testing skills. For compile, test, and `dump-package` verification, hand off to the existing Swift package execution workflows.

## Source Notes

- [Swift Package Index Add a Package](https://swiftpackageindex.com/add-a-package)
- [`SwiftPackageIndex/PackageList` README](https://github.com/SwiftPackageIndex/PackageList)
- [`SwiftPackageIndex/PackageList` Add Package issue template](https://github.com/SwiftPackageIndex/PackageList/blob/main/.github/ISSUE_TEMPLATE/add_package.yml)
- [`SwiftPackageIndex/PackageList` issue automation](https://github.com/SwiftPackageIndex/PackageList/blob/main/.github/workflows/issues.yml)
- [`SwiftPackageIndex/PackageList` add-package script](https://github.com/SwiftPackageIndex/PackageList/blob/main/.github/add_package.swift)
- [Socket SPI add-package automation plan](../../../../docs/maintainers/spi-add-package-automation-plan.md)
- [GitHub Docs: creating an issue from a URL query](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/creating-an-issue#creating-an-issue-from-a-url-query)
- [GitHub Docs: syntax for issue forms](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms)
- [`SwiftPackageIndex/SwiftPackageIndex-Server` maintainer badge view](https://github.com/SwiftPackageIndex/SwiftPackageIndex-Server/blob/main/Sources/App/Views/PackageController/MaintainerInfo/MaintainerInfoIndex%2BView.swift)
- [`SwiftPackageIndex/SwiftPackageIndex-Server` maintainer badge model](https://github.com/SwiftPackageIndex/SwiftPackageIndex-Server/blob/main/Sources/App/Views/PackageController/MaintainerInfo/MaintainerInfoIndex%2BModel.swift)
- [Swift Forums: Shields.io build badges for your packages](https://forums.swift.org/t/shields-io-build-badges-swift-versions-platforms-for-your-packages/54535)
- [Swift Package Index Package Collections](https://swiftpackageindex.com/package-collections)
- [Swift.org Package Collections](https://www.swift.org/blog/package-collections/)
- [Swift Package Index custom package collections announcement](https://swiftpackageindex.com/blog/introducing-custom-package-collections)
