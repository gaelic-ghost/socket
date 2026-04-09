#!/usr/bin/env zsh
emulate -L zsh
set -euo pipefail

WORKSPACE_ROOT="$(pwd)"
PACKAGE_NAME=""
TEST_PATH=""

SKILL_NAME="uv-pytest-unit-testing"
SCRIPT_DIR="${0:A:h}"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
GLOBAL_PROFILE="$HOME/.config/gaelic-ghost/python-skills/$SKILL_NAME/customization.yaml"
REPO_PROFILE="$REPO_ROOT/.codex/profiles/$SKILL_NAME/customization.yaml"

CONFIG_PATH=""
BYPASS_ALL_PROFILES=0
BYPASS_REPO_PROFILE=0
DELETE_REPO_PROFILE=0

usage() {
  cat <<'USAGE'
Usage: run_pytest_uv.sh [--workspace-root PATH] [--package NAME] [--path TEST_PATH] [--config PATH] [-- <pytest args>]

Options:
  --workspace-root PATH      Repository root containing pyproject.toml (default: cwd)
  --package NAME             Workspace member package name for package-scoped run
  --path TEST_PATH           Optional test path selector (e.g., tests/unit)
  --config PATH              Explicit YAML config path
  --bypassing-all-profiles   Ignore global and repo profile files for this run
  --bypassing-repo-profile   Ignore repo-local profile file for this run
  --deleting-repo-profile    Delete repo-local profile file before execution
  --                         Pass remaining args directly to pytest
  -h, --help                 Show this help
USAGE
}

require_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "error: required command not found: $1" >&2
    exit 1
  fi
}

fail() {
  echo "error: $*" >&2
  exit 1
}

trim() {
  local value="$1"
  value="${value#"${value%%[![:space:]]*}"}"
  value="${value%"${value##*[![:space:]]}"}"
  printf '%s' "$value"
}

strip_quotes() {
  local value="$1"
  if [[ "$value" == \"*\" && "$value" == *\" ]]; then
    value="${value:1:${#value}-2}"
  elif [[ "$value" == \'*\' && "$value" == *\' ]]; then
    value="${value:1:${#value}-2}"
  fi
  printf '%s' "$value"
}

apply_config_value() {
  local key="$1"
  local value="$2"

  case "$key" in
    workspace_root) WORKSPACE_ROOT="$value" ;;
    package) PACKAGE_NAME="$value" ;;
    path) TEST_PATH="$value" ;;
    *) fail "unknown config key '$key'" ;;
  esac
}

load_config_file() {
  local path="$1"
  local required="$2"

  if [[ ! -f "$path" ]]; then
    [[ "$required" -eq 1 ]] && fail "config file not found: $path"
    return 0
  fi

  local line
  local lineno=0
  while IFS= read -r line || [[ -n "$line" ]]; do
    lineno=$((lineno + 1))
    line="$(trim "$line")"
    [[ -z "$line" || "$line" == \#* ]] && continue
    [[ "$line" == *:* ]] || fail "invalid config line at $path:$lineno"

    local key="${line%%:*}"
    local value="${line#*:}"
    key="$(trim "$key")"
    value="${value%%#*}"
    value="$(trim "$value")"
    value="$(strip_quotes "$value")"

    [[ -n "$key" ]] || fail "empty config key at $path:$lineno"
    apply_config_value "$key" "$value"
  done < "$path"
}

ORIGINAL_ARGS=("$@")

while [[ $# -gt 0 ]]; do
  case "$1" in
    --workspace-root|--package|--path|--config)
      [[ $# -ge 2 ]] || fail "$1 requires a value"
      if [[ "$1" == "--config" ]]; then
        CONFIG_PATH="$2"
      fi
      shift 2
      ;;
    --bypassing-all-profiles)
      BYPASS_ALL_PROFILES=1
      shift
      ;;
    --bypassing-repo-profile)
      BYPASS_REPO_PROFILE=1
      shift
      ;;
    --deleting-repo-profile)
      DELETE_REPO_PROFILE=1
      shift
      ;;
    --)
      break
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "error: unknown argument: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

if [[ "$DELETE_REPO_PROFILE" -eq 1 ]]; then
  rm -f "$REPO_PROFILE"
fi

if [[ "$BYPASS_ALL_PROFILES" -eq 0 ]]; then
  load_config_file "$GLOBAL_PROFILE" 0
  if [[ "$BYPASS_REPO_PROFILE" -eq 0 ]]; then
    load_config_file "$REPO_PROFILE" 0
  fi
fi

if [[ -n "$CONFIG_PATH" ]]; then
  load_config_file "$CONFIG_PATH" 1
fi

EXTRA_ARGS=()
set -- "${ORIGINAL_ARGS[@]}"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --workspace-root)
      WORKSPACE_ROOT="$2"
      shift 2
      ;;
    --package)
      PACKAGE_NAME="$2"
      shift 2
      ;;
    --path)
      TEST_PATH="$2"
      shift 2
      ;;
    --config)
      shift 2
      ;;
    --bypassing-all-profiles|--bypassing-repo-profile|--deleting-repo-profile)
      shift
      ;;
    --)
      shift
      EXTRA_ARGS=("$@")
      break
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "error: unknown argument: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

require_cmd uv

if [[ ! -d "$WORKSPACE_ROOT" ]]; then
  echo "error: workspace root does not exist: $WORKSPACE_ROOT" >&2
  exit 1
fi

if [[ ! -f "$WORKSPACE_ROOT/pyproject.toml" ]]; then
  echo "error: missing pyproject.toml at $WORKSPACE_ROOT/pyproject.toml" >&2
  exit 1
fi

cd "$WORKSPACE_ROOT"

CMD=(uv run)
if [[ -n "$PACKAGE_NAME" ]]; then
  CMD+=(--package "$PACKAGE_NAME")
fi
CMD+=(pytest)

if [[ -n "$TEST_PATH" ]]; then
  CMD+=("$TEST_PATH")
fi

if [[ "${#EXTRA_ARGS[@]}" -gt 0 ]]; then
  CMD+=("${EXTRA_ARGS[@]}")
fi

echo "info: running: ${CMD[*]}"
"${CMD[@]}"
