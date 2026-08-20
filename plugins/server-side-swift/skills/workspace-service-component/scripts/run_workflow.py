#!/usr/bin/env python3
"""Add a framework-owned Swift service package to a canonical product workspace."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path


def emit(status: str, root: Path, name: str, framework: str, *, message: str | None = None, actions: list[str] | None = None) -> int:
    payload = {
        "status": status,
        "path_type": "primary",
        "output": {
            "workspace_root": str(root),
            "service_root": str(root / "Services" / name),
            "name": name,
            "framework": framework,
            "actions": actions or [],
            "next_step": message,
        },
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if status == "success" else 1


def add_service_mapping(root: Path, name: str) -> None:
    shared = root / "Services/services-shared.yml"
    content = shared.read_text(encoding="utf-8")
    if f"  {name}:\n" in content:
        return
    if content.strip() == "packages: {}":
        content = "packages:\n"
    elif not content.endswith("\n"):
        content += "\n"
    shared.write_text(content + f"  {name}:\n    path: Services/{name}\n", encoding="utf-8")


def local_services_script() -> str:
    return """#!/usr/bin/env sh
set -eu
command -v brew >/dev/null 2>&1 || { echo "Homebrew is required for native local service dependencies." >&2; exit 1; }
formula=${SERVICE_POSTGRES_FORMULA:-}
if [ -z "$formula" ]; then
  installed=$(brew list --formula | awk '/^postgresql(@[0-9]+)?$/')
  count=$(printf '%s\n' "$installed" | awk 'NF { count += 1 } END { print count + 0 }')
  [ "$count" -eq 1 ] || { echo "Set SERVICE_POSTGRES_FORMULA to the one installed PostgreSQL formula this repository uses. Installed candidates: ${installed:-none}. Current standard install: brew install postgresql@18" >&2; exit 1; }
  formula=$installed
fi
brew list --formula "$formula" >/dev/null 2>&1 || { echo "Missing $formula. Install it explicitly with: brew install $formula" >&2; exit 1; }
case ${1:-status} in
  status) ;;
  start) brew services start "$formula" ;;
  *) echo "Usage: $0 [status|start]" >&2; exit 1 ;;
esac
brew services list | awk -v formula="$formula" '$1 == formula && $2 == "started" { found=1 } END { exit found ? 0 : 1 }' || { echo "$formula is not running. Start it with: brew services start $formula" >&2; exit 1; }
echo "$formula is installed and running natively through Homebrew services."
"""


def github_workflow(name: str) -> str:
    image_name = name.lower()
    return f"""name: {name} service

on:
  pull_request:
    paths: ["Services/{name}/**", ".github/workflows/{name}-service.yml"]
  push:
    branches: [main]
    paths: ["Services/{name}/**", ".github/workflows/{name}-service.yml"]
  workflow_dispatch:
    inputs:
      environment:
        type: choice
        options: [live-test, production]
        default: live-test

permissions:
  contents: read
  id-token: write
  packages: write

concurrency:
  group: {name}-${{{{ github.event.inputs.environment || 'validation' }}}}
  cancel-in-progress: false

jobs:
  validate-linux:
    runs-on: ubuntu-latest
    outputs:
      image: ${{{{ steps.identity.outputs.image }}}}
      digest: ${{{{ steps.build.outputs.digest }}}}
    defaults:
      run:
        working-directory: Services/{name}
    steps:
      - uses: actions/checkout@v6.0.2
      - uses: swift-actions/setup-swift@v2
      - run: swift build -c release
      - run: swift test
      - id: identity
        working-directory: .
        run: echo "image=ghcr.io/${{{{ github.repository_owner }}}}/{image_name}" >> "$GITHUB_OUTPUT"
      - uses: docker/login-action@v4
        if: github.event_name != 'pull_request'
        with:
          registry: ghcr.io
          username: ${{{{ github.actor }}}}
          password: ${{{{ github.token }}}}
      - uses: docker/setup-buildx-action@v4
        if: github.event_name != 'pull_request'
      - id: build
        if: github.event_name != 'pull_request'
        uses: docker/build-push-action@v7
        with:
          context: Services/{name}
          push: true
          tags: ${{{{ steps.identity.outputs.image }}}}:${{{{ github.sha }}}}
          provenance: true
          sbom: true
      - name: Smoke-test the exact published digest
        if: github.event_name != 'pull_request'
        working-directory: .
        run: Scripts/smoke-{name}-image.sh "${{{{ steps.identity.outputs.image }}}}@${{{{ steps.build.outputs.digest }}}}"
      - name: Record immutable image identity
        if: github.event_name != 'pull_request'
        working-directory: .
        run: printf '%s@%s\n' "${{{{ steps.identity.outputs.image }}}}" "${{{{ steps.build.outputs.digest }}}}" > Services/{name}/image.identity
      - uses: actions/upload-artifact@v4
        if: github.event_name != 'pull_request'
        with:
          name: {name}-image-identity
          path: Services/{name}/image.identity

  deploy:
    if: github.event_name == 'workflow_dispatch'
    needs: validate-linux
    runs-on: ubuntu-latest
    environment: ${{{{ inputs.environment }}}}
    steps:
      - uses: actions/checkout@v6.0.2
      - name: Deploy the GitHub-built revision
        run: Scripts/deploy-{name}.sh "${{{{ needs.validate-linux.outputs.image }}}}@${{{{ needs.validate-linux.outputs.digest }}}}" "${{{{ inputs.environment }}}}"
"""


def blocked_cloud_script(kind: str, name: str) -> str:
    return f"""#!/usr/bin/env sh
set -eu
echo "The {kind} adapter for {name} is not configured. Replace this fail-closed script with the repository's reviewed provider command; keep immutable identity, GitHub environment, OIDC, health, and rollback ownership intact." >&2
exit 1
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--name", required=True)
    parser.add_argument("--framework", required=True, choices=("hummingbird", "vapor"))
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--skip-validation", action="store_true")
    args = parser.parse_args()
    root = Path(args.repo_root).expanduser().resolve()
    target = root / "Services" / args.name
    required = (root / "project.yml", root / "Services/services-shared.yml")
    if not root.is_dir() or any(not path.is_file() for path in required):
        return emit("blocked", root, args.name, args.framework, message="Use the canonical workspace entrypoint and point it at a workspace containing project.yml and Services/services-shared.yml.")
    if target.exists():
        return emit("blocked", root, args.name, args.framework, message=f"Services/{args.name} already exists.")
    command = ["hb", "init", args.name] if args.framework == "hummingbird" else ["vapor", "new", args.name]
    tool = command[0]
    actions = [f"run {' '.join(command)} under Services/", "remove generated Compose files and nested Git metadata", "add the service package to Services/services-shared.yml", "install native Homebrew and GitHub Actions boundaries"]
    if args.dry_run:
        return emit("success", root, args.name, args.framework, actions=actions, message="Run through bootstrap-xcode-workspace add-component; local dependencies will use native brew services and cloud builds will use GitHub Actions.")
    if not shutil.which(tool):
        install = "brew tap hummingbird-project/tap && brew install hb" if tool == "hb" else "brew install vapor"
        return emit("blocked", root, args.name, args.framework, actions=actions, message=f"Missing {tool}. Install it with: {install}")
    (root / "Services").mkdir(parents=True, exist_ok=True)
    generated = subprocess.run(command, cwd=root / "Services", capture_output=True, text=True, check=False)
    if generated.returncode != 0 or not (target / "Package.swift").is_file():
        return emit("failed", root, args.name, args.framework, actions=actions, message=f"{tool} generation failed: {generated.stderr or generated.stdout}")
    nested_git = target / ".git"
    if nested_git.is_dir():
        shutil.rmtree(nested_git)
    elif nested_git.exists():
        nested_git.unlink()
    for filename in ("compose.yaml", "compose.yml", "docker-compose.yaml", "docker-compose.yml"):
        path = target / filename
        if path.is_file():
            path.unlink()
    scripts = target / "Scripts"
    scripts.mkdir(exist_ok=True)
    local_script = scripts / "check-local-services.sh"
    local_script.write_text(local_services_script(), encoding="utf-8")
    local_script.chmod(0o755)
    workflow = root / f".github/workflows/{args.name}-service.yml"
    workflow.parent.mkdir(parents=True, exist_ok=True)
    workflow.write_text(github_workflow(args.name), encoding="utf-8")
    for kind in ("smoke", "deploy"):
        cloud_script = root / f"Scripts/{kind}-{args.name}-image.sh" if kind == "smoke" else root / f"Scripts/deploy-{args.name}.sh"
        cloud_script.parent.mkdir(parents=True, exist_ok=True)
        cloud_script.write_text(blocked_cloud_script(kind, args.name), encoding="utf-8")
        cloud_script.chmod(0o755)
    add_service_mapping(root, args.name)
    if not args.skip_validation:
        for command in (["swift", "build"], ["swift", "test"]):
            checked = subprocess.run(command, cwd=target, capture_output=True, text=True, check=False)
            if checked.returncode != 0:
                return emit("failed", root, args.name, args.framework, actions=actions, message=f"{' '.join(command)} failed: {checked.stderr or checked.stdout}")
    return emit("success", root, args.name, args.framework, actions=actions, message="Use native Swift and brew services locally; use the generated GitHub workflow for Linux artifacts and deployments.")


if __name__ == "__main__":
    raise SystemExit(main())
