# Swift Package Index Add-Package Automation Plan

## Purpose

This document records the Socket-level guardrail for adding Swift packages to Swift Package Index.

The real job is to make the valid SPI path boring and impossible to improvise around. SPI submission uses the documented `SwiftPackageIndex/PackageList` `Add Package(s)` issue form. Socket agents must not replace that form with GitHub CLI issue creation, manual labels, PackageList forks, `packages.json` edits, PackageList pull requests, or any other contribution path.

## Failure Mode To Prevent

The SwiftASB SPI attempt failed because an agent treated SPI readiness and SPI submission as if they were the same job, then improvised around the documented form path.

The concrete bad sequence was:

1. Create a `SwiftPackageIndex/PackageList` issue with `gh issue create`.
2. Try to attach the `Add Package` label without permission.
3. Observe that SPI automation did not run.
4. Fork `SwiftPackageIndex/PackageList`.
5. Edit `packages.json`.
6. Open a PackageList pull request.
7. Trigger external validation and CLA automation.
8. Describe the package as SPI set up even though it was not indexed.

None of those steps are acceptable as the default SPI submission path.

## Source-Of-Truth Process

The single documented add-package path is:

1. Confirm the package satisfies SPI requirements.
2. Open the official `Add Package(s)` issue form:
   <https://github.com/SwiftPackageIndex/PackageList/issues/new?template=add_package.yml>
3. Put one public GitHub package URL per line in the `New Packages` field.
4. Submit the issue through the form.
5. Let SPI's own automation create whatever PackageList follow-up it owns.

Socket tooling may inspect the public issue form definition before opening it. Socket tooling may not create or mutate any PackageList labels, forks, branches, files, or pull requests.

## One-Shot Script Contract

The script lives at:

```bash
scripts/spi_add_package.py
```

The intended one-shot command for a package checkout is:

```bash
uv run /Users/galew/Workspace/gaelic-ghost/socket/scripts/spi_add_package.py hands-free /path/to/package
```

The script performs these repo-local checks before any browser action:

- `Package.swift` exists at the package root.
- `Package.swift` declares Swift tools version 5.0 or later.
- The package remote resolves to a public GitHub HTTPS `.git` URL.
- At least one semantic-version tag exists locally and is visible on the public GitHub remote.
- `swift package dump-package` succeeds, emits parseable JSON, and includes at least one product.
- `swift build` succeeds unless explicitly skipped.
- `swift test` succeeds unless explicitly skipped.
- The package is not already indexed on SPI when the indexed-state check is available.

The script then fetches the live `SwiftPackageIndex/PackageList` issue form and refuses to continue unless it still contains:

- form name `Add Package(s)`
- default title `Add <Package>`
- default label `Add Package`
- required `New Packages` field with id `list`

If the form shape changes, the script stops. It must not invent a replacement submission path.

Browser-opening modes require complete readiness and the live form-shape check. Skip flags are allowed only for `readiness` and `url` diagnostic runs. They are rejected for `open` and `hands-free`.

## Modes

`readiness`

Runs local readiness and form-shape checks. It prints the official issue-form URL but does not open a browser.

`url`

Same checks as `readiness`; the important output is the prefilled official issue-form URL.

`open`

Runs checks, then opens the prefilled official issue form in the configured browser. The default browser target is Zen by bundle id:

```text
app.zen-browser.zen
```

`hands-free`

Runs checks, opens the prefilled official issue form in Zen, and prints a Codex Computer Use handoff. The handoff is the only permitted browser automation plan:

1. Use Computer Use against `app.zen-browser.zen`.
2. Confirm the page is the `SwiftPackageIndex/PackageList` `Add Package(s)` issue form.
3. Confirm the `New Packages` field contains the package URL exactly once.
4. Click GitHub's `Submit new issue` button.
5. Verify the created issue has the `Add Package` label and report the issue URL.

If any of those checks fail, stop and report the failure. Do not recover by creating labels, editing the issue through an API, creating a fork, or opening a PR.

## Forbidden Actions

The script and any agent using it must not:

- run `gh issue create` against `SwiftPackageIndex/PackageList`
- add or edit PackageList labels
- fork `SwiftPackageIndex/PackageList`
- clone `SwiftPackageIndex/PackageList`
- edit `packages.json`
- create or push PackageList branches
- open PackageList pull requests
- trigger PackageList validation or CLA automation through a manual contribution path
- call a blocked PackageList issue or PR a successful SPI submission

## Success Language

Use exact state language:

- `SPI-ready locally`: readiness checks passed, but no external SPI issue has been submitted.
- `SPI Add Package issue submitted`: the official issue form was submitted and the created issue has the `Add Package` label.
- `indexed on SPI`: the package page exists on `swiftpackageindex.com`.

Do not say `submitted`, `set up`, or `indexed` unless the corresponding external state has actually been verified.

## Future Skill Integration

Milestone 39 in `plugins/apple-dev-skills/ROADMAP.md` should treat this script contract as the implementation model for the planned Swift Package Index workflow skill.

The eventual skill should call or re-export this script instead of restating the process in prose. If the script and skill disagree, the script is the safer operating surface until the skill is corrected.
