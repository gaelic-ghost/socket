from typing import Literal

from fastmcp import FastMCP

from app.tools import (
    CARDHOP_SCHEMA_BUNDLE,
    cardhop_add,
    cardhop_healthcheck,
    cardhop_parse,
    cardhop_update,
)

mcp = FastMCP("Cardhop.app Socket")


@mcp.tool
def schema() -> dict[str, object]:
    """Return the locked Cardhop MCP schema bundle."""
    return CARDHOP_SCHEMA_BUNDLE


@mcp.tool
def parse(
    sentence: str,
    transport: Literal["auto", "applescript", "url_scheme"] = "auto",
    add_immediately: bool = False,
    dry_run: bool = False,
) -> dict[str, object]:
    """Send a parse sentence to Cardhop using documented macOS routes."""
    return cardhop_parse(
        sentence=sentence,
        transport=transport,
        add_immediately=add_immediately,
        dry_run=dry_run,
    )


@mcp.tool
def add(
    sentence: str,
    transport: Literal["auto", "applescript", "url_scheme"] = "auto",
    dry_run: bool = False,
) -> dict[str, object]:
    """Convenience add tool: parse with add_immediately=true."""
    return cardhop_add(sentence=sentence, transport=transport, dry_run=dry_run)


@mcp.tool
def update(
    instruction: str,
    transport: Literal["auto", "applescript", "url_scheme"] = "auto",
    add_immediately: bool = False,
    dry_run: bool = False,
) -> dict[str, object]:
    """Freeform update tool mapped to parse sentence semantics."""
    return cardhop_update(
        instruction=instruction,
        transport=transport,
        add_immediately=add_immediately,
        dry_run=dry_run,
    )


@mcp.tool
def healthcheck() -> dict[str, object]:
    """Report local Cardhop and transport readiness."""
    return cardhop_healthcheck()


if __name__ == "__main__":
    mcp.run()
