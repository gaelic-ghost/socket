#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

SERVER_SPEC="${SERVER_SPEC:-app/server.py}"
HOST="${HOST:-127.0.0.1}"
PORT="${PORT:-8123}"
MCP_URL="${MCP_URL:-http://${HOST}:${PORT}/mcp}"

usage() {
  cat <<USAGE
Usage:
  scripts/local_fastmcp.sh <command> [tool] [args-json]

Commands:
  inspect         Inspect FastMCP server metadata
  run-http        Run server over HTTP (streamable) at HOST:PORT
  list-http       List tools from MCP_URL
  call-health     Call health tool over MCP_URL
  call            Call an arbitrary tool over MCP_URL
  test            Run pytest
  smoke-http      Start HTTP server, list tools, call health, then stop
  smoke-json      Start HTTP server in dry-run mode and smoke test json create/update calls
  smoke-read      Start HTTP server and smoke test AppleScript-backed read calls
USAGE
}

inspect() {
  env PYTHONPATH=. uv run fastmcp inspect --server-spec "$SERVER_SPEC"
}

run_http() {
  env PYTHONPATH=. uv run fastmcp run --server-spec "$SERVER_SPEC" --transport http --host "$HOST" --port "$PORT"
}

list_http() {
  uv run fastmcp list --server-spec "$MCP_URL" --transport http --json
}

call_health() {
  uv run fastmcp call --server-spec "$MCP_URL" --transport http --target health --json
}

call_tool() {
  local tool_name="${1:-}"
  local args_json="${2:-}"

  if [[ -z "$tool_name" ]]; then
    echo "Usage: scripts/local_fastmcp.sh call <tool-name> [args-json]" >&2
    exit 1
  fi

  if [[ -n "$args_json" ]]; then
    uv run fastmcp call --server-spec "$MCP_URL" --transport http --target "$tool_name" --input-json "$args_json" --json
    return
  fi

  uv run fastmcp call --server-spec "$MCP_URL" --transport http --target "$tool_name" --json
}

call_tool_with_retry() {
  local tool_name="${1:-}"
  local args_json="${2:-}"
  local attempts=5
  local attempt=1

  while (( attempt <= attempts )); do
    if output="$(call_tool "$tool_name" "$args_json" 2>&1)"; then
      printf '%s\n' "$output"
      return 0
    fi
    if [[ "$output" != *"Client failed to connect: All connection attempts failed"* ]]; then
      printf '%s\n' "$output" >&2
      return 1
    fi
    if (( attempt == attempts )); then
      printf '%s\n' "$output" >&2
      return 1
    fi
    sleep 0.25
    (( attempt++ ))
  done
}

test_cmd() {
  uv run pytest
}

smoke_http() {
  log_file="$(mktemp)"
  server_pid=""

  cleanup() {
    if [[ -n "${server_pid:-}" ]] && kill -0 "$server_pid" 2>/dev/null; then
      kill "$server_pid" >/dev/null 2>&1 || true
      wait "$server_pid" 2>/dev/null || true
    fi
    if [[ -n "${log_file:-}" ]]; then
      rm -f "$log_file"
    fi
  }

  trap cleanup EXIT

  env PYTHONPATH=. uv run fastmcp run --server-spec "$SERVER_SPEC" --transport http --host "$HOST" --port "$PORT" >"$log_file" 2>&1 &
  server_pid=$!

  for _ in {1..30}; do
    if uv run fastmcp list --server-spec "$MCP_URL" --transport http --json >/dev/null 2>&1; then
      break
    fi
    sleep 0.2
  done

  if ! uv run fastmcp list --server-spec "$MCP_URL" --transport http --json >/dev/null 2>&1; then
    echo "Server did not start. Log output:" >&2
    cat "$log_file" >&2
    exit 1
  fi

  echo "--- list-http ---"
  list_http

  echo "--- call-health ---"
  call_health
}


smoke_json() {
  log_file="$(mktemp)"
  server_pid=""

  cleanup() {
    if [[ -n "${server_pid:-}" ]] && kill -0 "$server_pid" 2>/dev/null; then
      kill "$server_pid" >/dev/null 2>&1 || true
      wait "$server_pid" 2>/dev/null || true
    fi
    if [[ -n "${log_file:-}" ]]; then
      rm -f "$log_file"
    fi
  }

  trap cleanup EXIT

  env PYTHONPATH=. THINGS_MCP_DRY_RUN=1 uv run fastmcp run --server-spec "$SERVER_SPEC" --transport http --host "$HOST" --port "$PORT" >"$log_file" 2>&1 &
  server_pid=$!

  for _ in {1..30}; do
    if uv run fastmcp list --server-spec "$MCP_URL" --transport http --json >/dev/null 2>&1; then
      break
    fi
    sleep 0.2
  done

  if ! uv run fastmcp list --server-spec "$MCP_URL" --transport http --json >/dev/null 2>&1; then
    echo "Server did not start. Log output:" >&2
    cat "$log_file" >&2
    exit 1
  fi

  echo "--- import-json create (dry-run) ---"
  call_tool "things_import_json" '{"data":[{"type":"to-do","attributes":{"title":"Smoke create from CLI"}}]}'

  echo "--- import-json update (dry-run) ---"
  call_tool "things_import_json" '{"data":[{"type":"to-do","operation":"update","id":"SMOKE_TODO_ID","attributes":{"title":"Smoke update from CLI"}}],"auth_token":"SMOKE_TOKEN"}'
}


smoke_read() {
  log_file="$(mktemp)"
  server_pid=""

  cleanup() {
    if [[ -n "${server_pid:-}" ]] && kill -0 "$server_pid" 2>/dev/null; then
      kill "$server_pid" >/dev/null 2>&1 || true
      wait "$server_pid" 2>/dev/null || true
    fi
    if [[ -n "${log_file:-}" ]]; then
      rm -f "$log_file"
    fi
  }

  trap cleanup EXIT

  env PYTHONPATH=. uv run fastmcp run --server-spec "$SERVER_SPEC" --transport http --host "$HOST" --port "$PORT" >"$log_file" 2>&1 &
  server_pid=$!

  for _ in {1..30}; do
    if uv run fastmcp list --server-spec "$MCP_URL" --transport http --json >/dev/null 2>&1; then
      break
    fi
    sleep 0.2
  done

  if ! uv run fastmcp list --server-spec "$MCP_URL" --transport http --json >/dev/null 2>&1; then
    echo "Server did not start. Log output:" >&2
    cat "$log_file" >&2
    exit 1
  fi

  echo "--- read-todos (today) ---"
  call_tool_with_retry "things_read_todos" '{"list_id":"today","limit":5}'

  echo "--- find-todos ('inbox') ---"
  call_tool_with_retry "things_find_todos" '{"query":"inbox","limit":5}'

  echo "--- read-projects (open) ---"
  call_tool_with_retry "things_read_projects" '{"status":"open","limit":5}'

  echo "--- read-areas ---"
  call_tool_with_retry "things_read_areas"

  echo "--- read-headings (query='plan') ---"
  call_tool_with_retry "things_read_headings" '{"query":"plan","limit":5}'

  echo "--- invalid status check (expect THINGS_INVALID_STATUS) ---"
  if call_tool "things_read_todos" '{"list_id":"today","status":"pending","limit":5}' >/tmp/things_smoke_read_invalid.out 2>&1; then
    echo "Expected invalid status call to fail, but it succeeded." >&2
    cat /tmp/things_smoke_read_invalid.out >&2
    rm -f /tmp/things_smoke_read_invalid.out
    exit 1
  fi
  if ! rg -q "THINGS_INVALID_STATUS" /tmp/things_smoke_read_invalid.out; then
    echo "Invalid status call failed, but did not include THINGS_INVALID_STATUS." >&2
    cat /tmp/things_smoke_read_invalid.out >&2
    rm -f /tmp/things_smoke_read_invalid.out
    exit 1
  fi
  rm -f /tmp/things_smoke_read_invalid.out
}

main() {
  if [[ $# -lt 1 ]]; then
    usage
    exit 1
  fi

  case "$1" in
    inspect) inspect ;;
    run-http) run_http ;;
    list-http) list_http ;;
    call-health) call_health ;;
    call) call_tool "${2:-}" "${3:-}" ;;
    test) test_cmd ;;
    smoke-http) smoke_http ;;
    smoke-json) smoke_json ;;
    smoke-read) smoke_read ;;
    -h|--help|help) usage ;;
    *)
      echo "Unknown command: $1" >&2
      usage
      exit 1
      ;;
  esac
}

main "$@"
