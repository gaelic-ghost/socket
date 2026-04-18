SHELL := /bin/bash

HOST ?= 127.0.0.1
PORT ?= 8123
MCP_URL ?= http://$(HOST):$(PORT)/mcp
SERVER_SPEC ?= app/server.py

.PHONY: help inspect run-http list-http call-health call test lint typecheck check smoke-http smoke-json smoke-read

TOOL ?= health
ARGS_JSON ?=

help:
	@echo "Targets:"
	@echo "  make inspect"
	@echo "  make run-http [HOST=127.0.0.1 PORT=8123]"
	@echo "  make list-http [MCP_URL=http://127.0.0.1:8123/mcp]"
	@echo "  make call-health [MCP_URL=http://127.0.0.1:8123/mcp]"
	@echo "  make call TOOL=things_capabilities [ARGS_JSON='{"id":"abc"}'] [MCP_URL=http://127.0.0.1:8123/mcp]"
	@echo "  make test"
	@echo "  make lint"
	@echo "  make typecheck"
	@echo "  make check"
	@echo "  make smoke-http"
	@echo "  make smoke-json"
	@echo "  make smoke-read"

inspect:
	@SERVER_SPEC=$(SERVER_SPEC) ./scripts/local_fastmcp.sh inspect

run-http:
	@HOST=$(HOST) PORT=$(PORT) SERVER_SPEC=$(SERVER_SPEC) ./scripts/local_fastmcp.sh run-http

list-http:
	@MCP_URL=$(MCP_URL) ./scripts/local_fastmcp.sh list-http

call-health:
	@MCP_URL=$(MCP_URL) ./scripts/local_fastmcp.sh call-health

call:
	@MCP_URL=$(MCP_URL) ./scripts/local_fastmcp.sh call "$(TOOL)" "$(ARGS_JSON)"

test:
	@./scripts/local_fastmcp.sh test

lint:
	@uv run ruff check .

typecheck:
	@uv run mypy .

check: test lint typecheck

smoke-http:
	@HOST=$(HOST) PORT=$(PORT) MCP_URL=$(MCP_URL) SERVER_SPEC=$(SERVER_SPEC) ./scripts/local_fastmcp.sh smoke-http

smoke-json:
	@HOST=$(HOST) PORT=$(PORT) MCP_URL=$(MCP_URL) SERVER_SPEC=$(SERVER_SPEC) ./scripts/local_fastmcp.sh smoke-json

smoke-read:
	@HOST=$(HOST) PORT=$(PORT) MCP_URL=$(MCP_URL) SERVER_SPEC=$(SERVER_SPEC) ./scripts/local_fastmcp.sh smoke-read
