#!/usr/bin/env zsh
emulate -L zsh
set -euo pipefail

usage() {
  cat <<USAGE
Usage:
  $(basename "$0") --name <service-name> [options]

Options:
  --name <name>                 Service/project/workspace name (required)
  --mode <project|workspace>    Bootstrap mode (default: project)
  --path <target-path>          Target directory (default: ./<name>)
  --python <version>            Python version (default: 3.13)
  --members "a,b,c"             Workspace members (workspace mode only)
  --profile-map "a=package,b=service"
                                Workspace profile assignments (workspace mode only)
  --config <path>               Explicit YAML config path
  --bypassing-all-profiles      Ignore global and repo profile files for this run
  --bypassing-repo-profile      Ignore repo-local profile file for this run
  --deleting-repo-profile       Delete repo-local profile file before execution
  --force                       Allow non-empty target directory
  --initial-commit              Create an initial git commit after scaffold
  --no-git-init                 Skip git initialization
  -h, --help                    Show help
USAGE
}

fail() {
  echo "[ERROR] $*" >&2
  exit 1
}

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || fail "Missing required command '$1'. Install it and re-run the FastAPI scaffold."
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

bool_to_int() {
  local value
  value="$(printf '%s' "$1" | tr '[:upper:]' '[:lower:]')"
  case "$value" in
    1|true|yes|on) printf '1\n' ;;
    0|false|no|off) printf '0\n' ;;
    *) fail "invalid boolean value '$1'" ;;
  esac
}

apply_config_value() {
  local key="$1"
  local value="$2"

  case "$key" in
    name) NAME="$value" ;;
    mode) MODE="$value" ;;
    path) TARGET_PATH="$value" ;;
    python) PYTHON_VERSION="$value" ;;
    members) MEMBERS="$value" ;;
    profile_map) PROFILE_MAP="$value" ;;
    force) FORCE="$(bool_to_int "$value")" ;;
    initial_commit) INITIAL_COMMIT="$(bool_to_int "$value")" ;;
    no_git_init) NO_GIT_INIT="$(bool_to_int "$value")" ;;
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

NAME=""
MODE="project"
TARGET_PATH=""
PYTHON_VERSION="3.13"
MEMBERS=""
PROFILE_MAP=""
FORCE=0
INITIAL_COMMIT=0
NO_GIT_INIT=0

SKILL_NAME="bootstrap-python-service"
SCRIPT_DIR="${0:A:h}"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
GLOBAL_PROFILE="$HOME/.config/gaelic-ghost/python-skills/$SKILL_NAME/customization.yaml"
REPO_PROFILE="$REPO_ROOT/.codex/profiles/$SKILL_NAME/customization.yaml"

CONFIG_PATH=""
BYPASS_ALL_PROFILES=0
BYPASS_REPO_PROFILE=0
DELETE_REPO_PROFILE=0

ORIGINAL_ARGS=("$@")

while [[ $# -gt 0 ]]; do
  case "$1" in
    --config)
      CONFIG_PATH="${2:-}"
      [[ -n "$CONFIG_PATH" ]] || fail "--config requires a value"
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
    -h|--help)
      usage
      exit 0
      ;;
    --name|--mode|--path|--python|--members|--profile-map)
      [[ $# -ge 2 ]] || fail "$1 requires a value"
      shift 2
      ;;
    --force|--initial-commit|--no-git-init)
      shift
      ;;
    *)
      shift
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

set -- "${ORIGINAL_ARGS[@]}"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --name)
      NAME="${2:-}"
      shift 2
      ;;
    --mode)
      MODE="${2:-}"
      shift 2
      ;;
    --path)
      TARGET_PATH="${2:-}"
      shift 2
      ;;
    --python)
      PYTHON_VERSION="${2:-}"
      shift 2
      ;;
    --members)
      MEMBERS="${2:-}"
      shift 2
      ;;
    --profile-map)
      PROFILE_MAP="${2:-}"
      shift 2
      ;;
    --force)
      FORCE=1
      shift
      ;;
    --initial-commit)
      INITIAL_COMMIT=1
      shift
      ;;
    --no-git-init)
      NO_GIT_INIT=1
      shift
      ;;
    --config)
      shift 2
      ;;
    --bypassing-all-profiles|--bypassing-repo-profile|--deleting-repo-profile)
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      fail "unknown argument '$1'"
      ;;
  esac
done

[[ -n "$NAME" ]] || {
  usage >&2
  fail "--name is required"
}
[[ "$MODE" == "project" || "$MODE" == "workspace" ]] || fail "--mode must be 'project' or 'workspace'"
[[ "$NO_GIT_INIT" -eq 1 && "$INITIAL_COMMIT" -eq 1 ]] && fail "--initial-commit requires git initialization"

if [[ -z "$TARGET_PATH" ]]; then
  TARGET_PATH="./$NAME"
fi

SHARED_PROJECT_SCRIPT="$SCRIPT_DIR/../../bootstrap-uv-python-workspace/scripts/init_uv_python_project.sh"
SHARED_WORKSPACE_SCRIPT="$SCRIPT_DIR/../../bootstrap-uv-python-workspace/scripts/init_uv_python_workspace.sh"

[[ -x "$SHARED_PROJECT_SCRIPT" ]] || fail "shared script not found or not executable: $SHARED_PROJECT_SCRIPT"
[[ -x "$SHARED_WORKSPACE_SCRIPT" ]] || fail "shared script not found or not executable: $SHARED_WORKSPACE_SCRIPT"

require_cmd uv
if [[ "$NO_GIT_INIT" -eq 0 || "$INITIAL_COMMIT" -eq 1 ]]; then
  require_cmd git
fi

if [[ "$MODE" == "project" ]]; then
  [[ -z "$MEMBERS" ]] || fail "--members is only valid with --mode workspace"
  [[ -z "$PROFILE_MAP" ]] || fail "--profile-map is only valid with --mode workspace"

  cmd=(
    "$SHARED_PROJECT_SCRIPT"
    --name "$NAME"
    --profile service
    --path "$TARGET_PATH"
    --python "$PYTHON_VERSION"
    --bypassing-all-profiles
  )

  [[ "$FORCE" -eq 1 ]] && cmd+=(--force)
  [[ "$INITIAL_COMMIT" -eq 1 ]] && cmd+=(--initial-commit)
  [[ "$NO_GIT_INIT" -eq 1 ]] && cmd+=(--no-git-init)

  "${cmd[@]}"

  echo "Bootstrap complete: $TARGET_PATH"
  echo "Run (dev): cd $TARGET_PATH && uv run fastapi dev app/main.py"
  echo "Run (prod-style): cd $TARGET_PATH && uv run fastapi run app/main.py"
  echo "Checks: cd $TARGET_PATH && uv run pytest && uv run ruff check . && uv run mypy ."
  echo "Config: keep committed defaults in $TARGET_PATH/.env and local or secret overrides in $TARGET_PATH/.env.local"
  exit 0
fi

cmd=(
  "$SHARED_WORKSPACE_SCRIPT"
  --name "$NAME"
  --path "$TARGET_PATH"
  --python "$PYTHON_VERSION"
  --bypassing-all-profiles
)

[[ -n "$MEMBERS" ]] && cmd+=(--members "$MEMBERS")
[[ -n "$PROFILE_MAP" ]] && cmd+=(--profile-map "$PROFILE_MAP")
[[ "$FORCE" -eq 1 ]] && cmd+=(--force)
[[ "$INITIAL_COMMIT" -eq 1 ]] && cmd+=(--initial-commit)
[[ "$NO_GIT_INIT" -eq 1 ]] && cmd+=(--no-git-init)

"${cmd[@]}"

echo "Workspace bootstrap complete: $TARGET_PATH"
echo "Dev run example: cd $TARGET_PATH/packages/<service-member> && uv run fastapi dev app/main.py"
echo "Checks: cd $TARGET_PATH && uv run --all-packages pytest; (cd packages/<member> && uv run ruff check . && uv run mypy .)"
echo "Config: each workspace member now includes a committed .env plus an ignored .env.local override file."
