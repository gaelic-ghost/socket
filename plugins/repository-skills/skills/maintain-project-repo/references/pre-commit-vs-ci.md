# Local Validation and CI

`just repo-validate` is the complete validation entrypoint for people, agents,
and CI. The managed GitHub workflow only installs the required runtime and
invokes that recipe. Repository-specific checks belong in root-owned
`scripts/repo-maintenance/validations/*.fsx` hooks.

Do not install pre-commit automation, duplicate checks in workflow YAML, or
introduce another command surface.
