from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Any

from app.applescript_client import AppleScriptThingsClient
from app.token_store import (
    TokenNotFoundError,
    TokenStoreError,
    clear_token as _keychain_clear_token,
    get_token as _keychain_get_token,
    has_token as _keychain_has_token,
    set_token as _keychain_set_token,
)
from app.things_client import (
    ThingsUrlClient,
    ensure_update_payload_has_changes,
    require_non_empty,
    ThingsValidationError,
)


def health_payload() -> dict[str, str]:
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def add_todo_payload(
    title: str,
    *,
    notes: str | None = None,
    when: str | None = None,
    deadline: str | None = None,
    tags: list[str] | None = None,
    list_id: str | None = None,
    reveal: bool | None = None,
    client: ThingsUrlClient | None = None,
) -> dict[str, Any]:
    client = client or ThingsUrlClient()
    payload = {
        "title": require_non_empty(title, "title"),
        "notes": notes,
        "when": when,
        "deadline": deadline,
        "tags": tags,
        "list-id": list_id,
        "reveal": reveal,
    }
    return client.execute("add", payload)


def update_todo_payload(
    id: str,
    *,
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
    client: ThingsUrlClient | None = None,
) -> dict[str, Any]:
    client = client or ThingsUrlClient()
    payload = {
        "id": require_non_empty(id, "id"),
        "title": title,
        "notes": notes,
        "prepend-notes": prepend_notes,
        "append-notes": append_notes,
        "when": when,
        "deadline": deadline,
        "tags": tags,
        "add-tags": add_tags,
        "checklist-items": checklist_items,
        "prepend-checklist-items": prepend_checklist_items,
        "append-checklist-items": append_checklist_items,
        "list": list_name,
        "list-id": list_id,
        "heading": heading,
        "heading-id": heading_id,
        "completed": completed,
        "canceled": canceled,
        "reveal": reveal,
        "duplicate": duplicate,
        "creation-date": creation_date,
        "completion-date": completion_date,
    }
    ensure_update_payload_has_changes(payload, ignored_keys={"id"})
    payload["auth-token"] = _resolve_auth_token(auth_token)
    return client.execute("update", payload)


def version_payload(*, client: ThingsUrlClient | None = None) -> dict[str, Any]:
    client = client or ThingsUrlClient()
    return client.execute("version", capture_callback=True)


def add_project_payload(
    title: str | None = None,
    *,
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
    client: ThingsUrlClient | None = None,
) -> dict[str, Any]:
    client = client or ThingsUrlClient()
    payload = {
        "title": title.strip() if title else None,
        "notes": notes,
        "when": when,
        "deadline": deadline,
        "tags": tags,
        "area": area,
        "area-id": area_id,
        "to-dos": to_dos,
        "completed": completed,
        "canceled": canceled,
        "reveal": reveal,
        "creation-date": creation_date,
        "completion-date": completion_date,
    }
    return client.execute("add-project", payload)


def show_payload(
    *,
    id: str | None = None,
    query: str | None = None,
    filter_tags: list[str] | None = None,
    client: ThingsUrlClient | None = None,
) -> dict[str, Any]:
    client = client or ThingsUrlClient()
    normalized_id = id.strip() if id else None
    normalized_query = query.strip() if query else None
    if not normalized_id and not normalized_query:
        raise ThingsValidationError("Either 'id' or 'query' is required")

    payload: dict[str, Any] = {"id": normalized_id, "filter": filter_tags}
    if not normalized_id:
        payload["query"] = normalized_query
    return client.execute("show", payload)


def search_payload(
    *,
    query: str | None = None,
    client: ThingsUrlClient | None = None,
) -> dict[str, Any]:
    client = client or ThingsUrlClient()
    payload = {"query": query.strip() if query else None}
    return client.execute("search", payload)


def update_project_payload(
    id: str,
    *,
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
    client: ThingsUrlClient | None = None,
) -> dict[str, Any]:
    client = client or ThingsUrlClient()
    payload = {
        "id": require_non_empty(id, "id"),
        "title": title,
        "notes": notes,
        "prepend-notes": prepend_notes,
        "append-notes": append_notes,
        "when": when,
        "deadline": deadline,
        "tags": tags,
        "add-tags": add_tags,
        "area": area,
        "area-id": area_id,
        "completed": completed,
        "canceled": canceled,
        "reveal": reveal,
        "duplicate": duplicate,
        "creation-date": creation_date,
        "completion-date": completion_date,
    }
    ensure_update_payload_has_changes(payload, ignored_keys={"id"})
    payload["auth-token"] = _resolve_auth_token(auth_token)
    return client.execute("update-project", payload)


def import_json_payload(
    data: str | list[Any] | dict[str, Any],
    *,
    auth_token: str | None = None,
    reveal: bool | None = None,
    client: ThingsUrlClient | None = None,
) -> dict[str, Any]:
    client = client or ThingsUrlClient()

    if isinstance(data, str):
        try:
            parsed_data: Any = json.loads(data)
        except json.JSONDecodeError as exc:
            raise ThingsValidationError(f"'data' must be valid JSON: {exc.msg}") from exc
    else:
        parsed_data = data

    if parsed_data is None:
        raise ThingsValidationError("'data' cannot be null")

    _validate_import_json_shape(parsed_data)

    resolved_token: str | None
    if _contains_update_operation(parsed_data):
        resolved_token = _resolve_auth_token(auth_token)
    else:
        resolved_token = auth_token

    payload: dict[str, Any] = {
        "data": json.dumps(parsed_data, separators=(",", ":"), ensure_ascii=False),
        "reveal": reveal,
    }
    if resolved_token:
        payload["auth-token"] = resolved_token
    return client.execute("json", payload)


def _contains_update_operation(value: Any) -> bool:
    if isinstance(value, dict):
        operation = value.get("operation")
        if isinstance(operation, str) and operation.lower() == "update":
            return True
        return any(_contains_update_operation(v) for v in value.values())
    if isinstance(value, list):
        return any(_contains_update_operation(item) for item in value)
    return False


def _validate_import_json_shape(value: Any) -> None:
    if isinstance(value, list):
        for index, item in enumerate(value):
            _validate_import_json_item(item, path=f"data[{index}]")
        return

    if isinstance(value, dict):
        if "items" in value and isinstance(value["items"], list):
            for index, item in enumerate(value["items"]):
                _validate_import_json_item(item, path=f"data.items[{index}]")
            return
        _validate_import_json_item(value, path="data")
        return

    raise ThingsValidationError("'data' must be an object or an array of objects")


def _validate_import_json_item(item: Any, *, path: str) -> None:
    if not isinstance(item, dict):
        raise ThingsValidationError(f"{path} must be an object")

    item_type = item.get("type")
    if item_type is not None and (not isinstance(item_type, str) or not item_type.strip()):
        raise ThingsValidationError(f"{path}.type must be a non-empty string when provided")

    operation = item.get("operation")
    if operation is not None:
        if not isinstance(operation, str) or operation.lower() not in {"create", "update"}:
            raise ThingsValidationError(f"{path}.operation must be 'create' or 'update'")
        if operation.lower() == "update":
            item_id = item.get("id")
            if not isinstance(item_id, str) or not item_id.strip():
                raise ThingsValidationError(f"{path}.id is required for update operations")

    attributes = item.get("attributes")
    if attributes is not None and not isinstance(attributes, dict):
        raise ThingsValidationError(f"{path}.attributes must be an object when provided")

    for child_key in ("to-dos", "headings", "items"):
        children = item.get(child_key)
        if children is None:
            continue
        if not isinstance(children, list):
            raise ThingsValidationError(f"{path}.{child_key} must be an array when provided")
        for index, child in enumerate(children):
            _validate_import_json_item(child, path=f"{path}.{child_key}[{index}]")


def read_todos_payload(
    *,
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
    client: AppleScriptThingsClient | None = None,
) -> dict[str, Any]:
    client = client or AppleScriptThingsClient()
    todos = client.list_todos(
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
    return {"ok": True, "count": len(todos), "items": todos}


def read_todo_payload(
    *,
    todo_id: str,
    include_notes: bool = True,
    client: AppleScriptThingsClient | None = None,
) -> dict[str, Any]:
    client = client or AppleScriptThingsClient()
    item = client.get_todo(todo_id=todo_id, include_notes=include_notes)
    return {"ok": True, "item": item}


def find_todos_payload(
    *,
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
    client: AppleScriptThingsClient | None = None,
) -> dict[str, Any]:
    client = client or AppleScriptThingsClient()
    todos = client.search_todos(
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
    return {"ok": True, "count": len(todos), "items": todos}


def read_projects_payload(
    *,
    limit: int = 50,
    offset: int = 0,
    status: str | None = None,
    area_id: str | None = None,
    deadline_before: str | None = None,
    deadline_after: str | None = None,
    completed_before: str | None = None,
    completed_after: str | None = None,
    include_notes: bool = False,
    client: AppleScriptThingsClient | None = None,
) -> dict[str, Any]:
    client = client or AppleScriptThingsClient()
    projects = client.list_projects(
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
    return {"ok": True, "count": len(projects), "items": projects}


def read_areas_payload(*, client: AppleScriptThingsClient | None = None) -> dict[str, Any]:
    client = client or AppleScriptThingsClient()
    areas = client.list_areas()
    return {"ok": True, "count": len(areas), "items": areas}


def read_headings_payload(
    *,
    limit: int = 200,
    offset: int = 0,
    project_id: str | None = None,
    query: str | None = None,
    client: AppleScriptThingsClient | None = None,
) -> dict[str, Any]:
    client = client or AppleScriptThingsClient()
    headings = client.list_headings(
        limit=limit,
        offset=offset,
        project_id=project_id,
        query=query,
    )
    return {"ok": True, "count": len(headings), "items": headings}


def auth_set_token_payload(token: str) -> dict[str, Any]:
    normalized = require_non_empty(token, "token")
    try:
        _keychain_set_token(normalized)
    except TokenStoreError as exc:
        raise ThingsValidationError(str(exc)) from exc
    return {"ok": True, "token_stored": True}


def auth_clear_token_payload() -> dict[str, Any]:
    try:
        _keychain_clear_token()
    except TokenStoreError as exc:
        raise ThingsValidationError(str(exc)) from exc
    return {"ok": True, "token_cleared": True}


def auth_status_payload() -> dict[str, Any]:
    has_env = bool(os.getenv("THINGS_AUTH_TOKEN"))
    try:
        has_keychain = _keychain_has_token()
    except TokenStoreError as exc:
        raise ThingsValidationError(str(exc)) from exc
    source = "env" if has_env else ("keychain" if has_keychain else "none")
    return {
        "ok": True,
        "has_env_token": has_env,
        "has_keychain_token": has_keychain,
        "active_source": source,
    }


def _resolve_auth_token(explicit_token: str | None) -> str:
    if explicit_token and explicit_token.strip():
        return explicit_token.strip()

    env_token = os.getenv("THINGS_AUTH_TOKEN")
    if env_token and env_token.strip():
        return env_token.strip()

    try:
        keychain_token = _keychain_get_token()
    except TokenNotFoundError:
        keychain_token = None
    except TokenStoreError as exc:
        raise ThingsValidationError(str(exc)) from exc

    if keychain_token and keychain_token.strip():
        return keychain_token.strip()

    raise ThingsValidationError(
        "THINGS_AUTH_MISSING: 'auth_token' is required for update commands. Set THINGS_AUTH_TOKEN, store one with things_auth_set_token, or pass auth_token."
    )
