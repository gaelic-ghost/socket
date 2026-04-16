# XCTestPlan Configurations and Matrix Coverage

## When `.xctestplan` earns its weight

- Version `.xctestplan` files when the project needs repeatable named configurations for launch arguments, environment variables, locale, content-size-category coverage, sanitizers, diagnostics, or code coverage.
- Keep the plan focused on real matrix coverage instead of turning it into a dumping ground for every one-off test tweak.

## Core commands

- Inspect available plans with `xcodebuild -scheme <Scheme> -showTestPlans`.
- Run a specific plan with `xcodebuild -scheme <Scheme> -testPlan <Plan> test`.
- Use `-only-test-configuration` when one named configuration inside the plan is the actual verification target.
- Use `-skip-test-configuration` when a plan-wide run is right except for a known excluded configuration.

## Good uses

- locale or language-variant coverage
- accessibility-related launch-argument or content-size-category matrices
- debug-versus-release-sensitive test configurations
- diagnostics-heavy runs with sanitizers, logging, or code coverage turned on explicitly

## Review questions

- Why is this plan needed instead of a direct `xcodebuild test` invocation?
- Does each named configuration represent a real verification surface?
- Are launch arguments and environment values documented clearly enough that the next maintainer understands what the matrix is proving?
