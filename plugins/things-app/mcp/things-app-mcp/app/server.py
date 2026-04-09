from __future__ import annotations

from typing import Any

from fastmcp import FastMCP

from app.things_client import ThingsClientError, ThingsValidationError
from app.tools import (
    add_project_payload,
    add_todo_payload,
    auth_clear_token_payload,
    auth_set_token_payload,
    auth_status_payload,
    find_todos_payload,
    health_payload,
    import_json_payload,
    read_headings_payload,
    read_areas_payload,
    read_projects_payload,
    read_todo_payload,
    read_todos_payload,
    search_payload,
    show_payload,
    update_project_payload,
    update_todo_payload,
    version_payload,
)

mcp = FastMCP("things-mcp")


@mcp.tool
def health() -> dict[str, str]:
    """Return a lightweight health payload for smoke testing."""
    return health_payload()


@mcp.tool
def things_add_todo(
    title: str,
    notes: str | None = None,
    when: str | None = None,
    deadline: str | None = None,
    tags: list[str] | None = None,
    list_id: str | None = None,
    reveal: bool | None = None,
) -> dict[str, Any]:
    """Create a to-do in Things using the URL scheme add command."""
    return add_todo_payload(
        title,
        notes=notes,
        when=when,
        deadline=deadline,
        tags=tags,
        list_id=list_id,
        reveal=reveal,
    )


@mcp.tool
def things_add_project(
    title: str | None = None,
    notes: str | None = None,
    when: str | None = None,
    deadline: str | None = None,
    tags: list[str] | None = None,
    area: str | None = None,
    area_id: str | None = None,
    to_dos: list[str] | None = None,
    completed: bool | None = None,
    canceled: bool | None = None,
    reveal: bool | None = None,
    creation_date: str | None = None,
    completion_date: str | None = None,
) -> dict[str, Any]:
    """Create a project in Things via things:///add-project."""
    return add_project_payload(
        title,
        notes=notes,
        when=when,
        deadline=deadline,
        tags=tags,
        area=area,
        area_id=area_id,
        to_dos=to_dos,
        completed=completed,
        canceled=canceled,
        reveal=reveal,
        creation_date=creation_date,
        completion_date=completion_date,
    )


@mcp.tool
def things_update_todo(
    id: str,
    title: str | None = None,
    notes: str | None = None,
    prepend_notes: str | None = None,
    append_notes: str | None = None,
    when: str | None = None,
    deadline: str | None = None,
    tags: list[str] | None = None,
    add_tags: list[str] | None = None,
    checklist_items: list[str] | None = None,
    prepend_checklist_items: list[str] | None = None,
    append_checklist_items: list[str] | None = None,
    list_name: str | None = None,
    list_id: str | None = None,
    heading: str | None = None,
    heading_id: str | None = None,
    completed: bool | None = None,
    canceled: bool | None = None,
    auth_token: str | None = None,
    reveal: bool | None = None,
    duplicate: bool | None = None,
    creation_date: str | None = None,
    completion_date: str | None = None,
) -> dict[str, Any]:
    """Update an existing to-do in Things (requires auth token)."""
    return update_todo_payload(
        id,
        title=title,
        notes=notes,
        prepend_notes=prepend_notes,
        append_notes=append_notes,
        when=when,
        deadline=deadline,
        tags=tags,
        add_tags=add_tags,
        checklist_items=checklist_items,
        prepend_checklist_items=prepend_checklist_items,
        append_checklist_items=append_checklist_items,
        list_name=list_name,
        list_id=list_id,
        heading=heading,
        heading_id=heading_id,
        completed=completed,
        canceled=canceled,
        auth_token=auth_token,
        reveal=reveal,
        duplicate=duplicate,
        creation_date=creation_date,
        completion_date=completion_date,
    )


@mcp.tool
def things_version() -> dict[str, Any]:
    """Return Things app version details using x-callback-url."""
    return version_payload()


@mcp.tool
def things_show(
    id: str | None = None,
    query: str | None = None,
    filter_tags: list[str] | None = None,
) -> dict[str, Any]:
    """Navigate to a Things list/item/view via things:///show."""
    return show_payload(id=id, query=query, filter_tags=filter_tags)


@mcp.tool
def things_search(query: str | None = None) -> dict[str, Any]:
    """Open Things search UI with an optional pre-filled query."""
    return search_payload(query=query)


@mcp.tool
def things_update_project(
    id: str,
    title: str | None = None,
    notes: str | None = None,
    prepend_notes: str | None = None,
    append_notes: str | None = None,
    when: str | None = None,
    deadline: str | None = None,
    tags: list[str] | None = None,
    add_tags: list[str] | None = None,
    area: str | None = None,
    area_id: str | None = None,
    completed: bool | None = None,
    canceled: bool | None = None,
    reveal: bool | None = None,
    duplicate: bool | None = None,
    creation_date: str | None = None,
    completion_date: str | None = None,
    auth_token: str | None = None,
) -> dict[str, Any]:
    """Update a project in Things via things:///update-project."""
    return update_project_payload(
        id,
        title=title,
        notes=notes,
        prepend_notes=prepend_notes,
        append_notes=append_notes,
        when=when,
        deadline=deadline,
        tags=tags,
        add_tags=add_tags,
        area=area,
        area_id=area_id,
        completed=completed,
        canceled=canceled,
        reveal=reveal,
        duplicate=duplicate,
        creation_date=creation_date,
        completion_date=completion_date,
        auth_token=auth_token,
    )


@mcp.tool
def things_import_json(
    data: str | list[Any] | dict[str, Any],
    auth_token: str | None = None,
    reveal: bool | None = None,
) -> dict[str, Any]:
    """Create or update items in batch via things:///json."""
    return import_json_payload(data, auth_token=auth_token, reveal=reveal)


@mcp.tool
def things_read_todos(
    list_id: str | None = None,
    limit: int = 50,
    offset: int = 0,
    status: str | None = None,
    project_id: str | None = None,
    area_id: str | None = None,
    deadline_before: str | None = None,
    deadline_after: str | None = None,
    completed_before: str | None = None,
    completed_after: str | None = None,
    include_notes: bool = False,
) -> dict[str, Any]:
    """Read to-dos from Things via AppleScript for unattended workflows."""
    return read_todos_payload(
        list_id=list_id,
        limit=limit,
        offset=offset,
        status=status,
        project_id=project_id,
        area_id=area_id,
        deadline_before=deadline_before,
        deadline_after=deadline_after,
        completed_before=completed_before,
        completed_after=completed_after,
        include_notes=include_notes,
    )


@mcp.tool
def things_read_todo(todo_id: str, include_notes: bool = True) -> dict[str, Any]:
    """Read a single to-do from Things by ID via AppleScript."""
    return read_todo_payload(todo_id=todo_id, include_notes=include_notes)


@mcp.tool
def things_find_todos(
    query: str,
    limit: int = 50,
    offset: int = 0,
    status: str | None = None,
    project_id: str | None = None,
    area_id: str | None = None,
    deadline_before: str | None = None,
    deadline_after: str | None = None,
    completed_before: str | None = None,
    completed_after: str | None = None,
    include_notes: bool = False,
) -> dict[str, Any]:
    """Search to-dos by title text via AppleScript."""
    return find_todos_payload(
        query=query,
        limit=limit,
        offset=offset,
        status=status,
        project_id=project_id,
        area_id=area_id,
        deadline_before=deadline_before,
        deadline_after=deadline_after,
        completed_before=completed_before,
        completed_after=completed_after,
        include_notes=include_notes,
    )


@mcp.tool
def things_read_projects(
    limit: int = 50,
    offset: int = 0,
    status: str | None = None,
    area_id: str | None = None,
    deadline_before: str | None = None,
    deadline_after: str | None = None,
    completed_before: str | None = None,
    completed_after: str | None = None,
    include_notes: bool = False,
) -> dict[str, Any]:
    """Read projects from Things via AppleScript."""
    return read_projects_payload(
        limit=limit,
        offset=offset,
        status=status,
        area_id=area_id,
        deadline_before=deadline_before,
        deadline_after=deadline_after,
        completed_before=completed_before,
        completed_after=completed_after,
        include_notes=include_notes,
    )


@mcp.tool
def things_read_areas() -> dict[str, Any]:
    """Read areas from Things via AppleScript."""
    return read_areas_payload()


@mcp.tool
def things_read_headings(
    limit: int = 200,
    offset: int = 0,
    project_id: str | None = None,
    query: str | None = None,
) -> dict[str, Any]:
    """Read headings from Things via AppleScript."""
    return read_headings_payload(
        limit=limit,
        offset=offset,
        project_id=project_id,
        query=query,
    )


@mcp.tool
def things_validate_token_config(auth_token: str | None = None) -> dict[str, Any]:
    """Check whether auth token config is available for update commands."""
    has_explicit = bool(auth_token)
    status = auth_status_payload()
    has_env = status["has_env_token"]
    has_keychain = status["has_keychain_token"]
    return {
        "ok": has_explicit or has_env or has_keychain,
        "has_explicit_token": has_explicit,
        "has_env_token": has_env,
        "has_keychain_token": has_keychain,
        "active_source": "explicit" if has_explicit else status["active_source"],
    }


@mcp.tool
def things_auth_set_token(token: str) -> dict[str, Any]:
    """Store Things auth token in macOS keychain."""
    return auth_set_token_payload(token)


@mcp.tool
def things_auth_get_status() -> dict[str, Any]:
    """Get auth token status across env and keychain sources."""
    return auth_status_payload()


@mcp.tool
def things_auth_clear_token() -> dict[str, Any]:
    """Clear stored Things auth token from macOS keychain."""
    return auth_clear_token_payload()


@mcp.tool
def things_capabilities() -> dict[str, Any]:
    """Describe currently implemented Things MCP capabilities."""
    return {
        "implemented_tools": [
            "things_add_todo",
            "things_add_project",
            "things_update_todo",
            "things_version",
            "things_show",
            "things_search",
            "things_update_project",
            "things_import_json",
            "things_read_todos",
            "things_read_todo",
            "things_find_todos",
            "things_read_projects",
            "things_read_areas",
            "things_read_headings",
            "things_validate_token_config",
            "things_auth_set_token",
            "things_auth_get_status",
            "things_auth_clear_token",
        ],
        "notes": [
            "Service dispatches actions through things:/// URL scheme.",
            "Update commands resolve auth token from auth_token arg, THINGS_AUTH_TOKEN, then keychain.",
            "Read operations use AppleScript and require macOS automation permissions.",
        ],
    }


if __name__ == "__main__":
    try:
        mcp.run()
    except (ThingsValidationError, ThingsClientError):
        raise
