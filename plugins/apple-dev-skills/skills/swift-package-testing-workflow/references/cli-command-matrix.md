# SwiftPM Command Matrix

## Inspection and shape

- `swift package describe`
- `swift package dump-package`
- `swift package show-dependencies`

## Build, test, and run

- `swift build`
- `swift test`
- `swift run <target>`
- `xcodebuild -scheme <PackageName> -showTestPlans` when package-facing Xcode test plans exist
- `xcodebuild -scheme <PackageName> -testPlan <Plan> test` when a package contract depends on an `.xctestplan`
- `xcodebuild -scheme <PackageName> -configuration Release build` when Release-path validation matters

## Manifest and dependency work

- `swift package add-dependency <url>`
- `swift package update`
- `swift package resolve`
- `swift package reset`

## Plugins and tools

- `swift package plugin --list`
- `swift package plugin --allow-writing-to-package-directory <plugin>`
- `swift package clean`

## Toolchain checks

- `swift --version`
- `swift package --help`
- `xcrun --find swift` when Apple toolchain location matters
- `xcodebuild -version` when Apple-managed SDK or Xcode component state matters
- `xcodebuild -showComponent metalToolchain` when Metal toolchain availability is relevant
- `xcrun --find xctrace` when Instruments trace capture or export is relevant
- `xcrun xctrace version` when the active Instruments command-line tool version matters
- `xcrun xctrace list templates` before assuming an Instruments template exists on the current Xcode version

## Performance profiling

- `swift build -c release --product <ExecutableProduct>` before profiling an optimized package executable
- `xcrun xctrace record --template 'Time Profiler' --output traces/<name>.trace --launch -- .build/release/<ExecutableProduct> <args>` for CPU profile capture
- `xcrun xctrace record --template 'Metal System Trace' --time-limit 30s --output traces/<name>.trace --launch -- .build/release/<ExecutableProduct> <args>` for Metal CPU/GPU timeline capture
- `xcrun xctrace record --template 'Allocations' --output traces/<name>.trace --launch -- .build/release/<ExecutableProduct> <args>` for allocation capture
- Prefer profiling the built executable over profiling `swift run` when the measurement target is runtime behavior rather than build or package-driver overhead.
