#!/usr/bin/env python3
"""Check the canonical ACP Registry for an exact agent identifier or name."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


DEFAULT_REGISTRY = "https://cdn.agentclientprotocol.com/registry/v1/latest/registry.json"


def load_registry(url: str) -> dict[str, Any]:
    request = Request(url, headers={"User-Agent": "socket-acp-registry-check/1"})
    try:
        with urlopen(request, timeout=15) as response:  # noqa: S310 - caller controls reviewed registry URL
            payload = json.load(response)
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as error:
        raise RuntimeError(
            f"The ACP registry could not be read from {url}: {error}. "
            "Check network access and the registry URL before changing client configuration."
        ) from error
    if not isinstance(payload, dict) or not isinstance(payload.get("agents"), list):
        raise RuntimeError(
            f"The ACP registry response from {url} does not contain an agents array. "
            "The registry schema may have changed or the URL may not be canonical."
        )
    return payload


def find_agents(payload: dict[str, Any], query: str) -> list[dict[str, Any]]:
    folded = query.casefold()
    matches: list[dict[str, Any]] = []
    for value in payload["agents"]:
        if not isinstance(value, dict):
            continue
        identifier = value.get("id")
        name = value.get("name")
        if (isinstance(identifier, str) and identifier.casefold() == folded) or (
            isinstance(name, str) and name.casefold() == folded
        ):
            matches.append(value)
    return matches


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check whether an agent is currently published in the canonical ACP Registry."
    )
    parser.add_argument("query", help="Exact ACP agent id or display name")
    parser.add_argument("--registry-url", default=DEFAULT_REGISTRY)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        payload = load_registry(args.registry_url)
        matches = find_agents(payload, args.query)
    except RuntimeError as error:
        print(str(error), file=sys.stderr)
        return 2

    result = {
        "query": args.query,
        "registry_url": args.registry_url,
        "registry_version": payload.get("version"),
        "present": bool(matches),
        "matches": matches,
    }
    if args.format == "json":
        print(json.dumps(result, indent=2, sort_keys=True))
    elif matches:
        for match in matches:
            print(
                f"ACP Registry contains {match.get('name', '(unnamed)')} "
                f"({match.get('id', '(no id)')}) at version {match.get('version', '(unknown)')}."
            )
    else:
        print(
            f"ACP Registry does not currently contain an exact id or name match for {args.query!r}. "
            "Use an official custom launch command only if the client supports one."
        )
    return 0 if matches else 1


if __name__ == "__main__":
    raise SystemExit(main())
