from __future__ import annotations

from typing import Any

import pytest

from app.things_client import ThingsValidationError
from app.tools import (
    add_project_payload,
    add_todo_payload,
    auth_clear_token_payload,
    auth_set_token_payload,
    auth_status_payload,
    find_todos_payload,
    health_payload,
    import_json_payload,
    read_areas_payload,
    read_headings_payload,
    read_projects_payload,
    read_todo_payload,
    read_todos_payload,
    search_payload,
    show_payload,
    update_project_payload,
    update_todo_payload,
)


class StubClient:
    def __init__(self) -> None:
        self.calls: list[tuple[str, dict, bool]] = []

    def execute(self, command: str, params: dict, capture_callback: bool = False) -> dict:
        self.calls.append((command, params, capture_callback))
        return {"ok": True, "command": command, "params": params, "capture_callback": capture_callback}


class StubAppleScriptClient:
    def __init__(self) -> None:
        self.list_calls: list[dict[str, Any]] = []
        self.get_calls: list[dict[str, Any]] = []
        self.search_calls: list[dict[str, Any]] = []
        self.project_calls: list[dict[str, Any]] = []
        self.area_calls: int = 0
        self.heading_calls: list[dict[str, Any]] = []

    def list_todos(
        self,
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
    ) -> list[dict[str, str]]:
        self.list_calls.append(
            {
                "list_id": list_id,
                "limit": limit,
                "offset": offset,
                "status": status,
                "project_id": project_id,
                "area_id": area_id,
                "deadline_before": deadline_before,
                "deadline_after": deadline_after,
                "completed_before": completed_before,
                "completed_after": completed_after,
                "include_notes": include_notes,
            }
        )
        return [{"id": "1", "title": "Todo", "status": "open", "status_raw": "open", "notes": "N"}]

    def get_todo(self, *, todo_id: str, include_notes: bool = True) -> dict[str, str]:
        self.get_calls.append({"todo_id": todo_id, "include_notes": include_notes})
        return {"id": todo_id, "title": "Todo", "status": "open", "status_raw": "open", "notes": "N"}

    def search_todos(
        self,
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
    ) -> list[dict[str, str]]:
        self.search_calls.append(
            {
                "query": query,
                "limit": limit,
                "offset": offset,
                "status": status,
                "project_id": project_id,
                "area_id": area_id,
                "deadline_before": deadline_before,
                "deadline_after": deadline_after,
                "completed_before": completed_before,
                "completed_after": completed_after,
                "include_notes": include_notes,
            }
        )
        return [{"id": "2", "title": query, "status": "open", "status_raw": "open", "notes": "N"}]

    def list_projects(
        self,
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
    ) -> list[dict[str, str]]:
        self.project_calls.append(
            {
                "limit": limit,
                "offset": offset,
                "status": status,
                "area_id": area_id,
                "deadline_before": deadline_before,
                "deadline_after": deadline_after,
                "completed_before": completed_before,
                "completed_after": completed_after,
                "include_notes": include_notes,
            }
        )
        return [{"id": "p1", "title": "Project", "status": "open", "status_raw": "open", "notes": "N"}]

    def list_areas(self) -> list[dict[str, str]]:
        self.area_calls += 1
        return [{"id": "a1", "title": "Area"}]

    def list_headings(
        self,
        *,
        limit: int = 200,
        offset: int = 0,
        project_id: str | None = None,
        query: str | None = None,
    ) -> list[dict[str, str]]:
        self.heading_calls.append(
            {
                "limit": limit,
                "offset": offset,
                "project_id": project_id,
                "query": query,
            }
        )
        return [{"id": "h1", "title": "Heading", "project_id": "p1", "project_title": "Project"}]


def test_health_payload() -> None:
    payload = health_payload()
    assert payload["status"] == "ok"
    assert payload["timestamp"]


def test_add_todo_payload_builds_expected_params() -> None:
    client = StubClient()

    result = add_todo_payload(
        "Ship release",
        notes="note",
        tags=["work", "urgent"],
        client=client,
    )

    assert result["ok"] is True
    command, params, capture_callback = client.calls[0]
    assert command == "add"
    assert capture_callback is False
    assert params["title"] == "Ship release"
    assert params["tags"] == ["work", "urgent"]


def test_update_todo_payload_uses_env_token(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("THINGS_AUTH_TOKEN", "env-token")
    client = StubClient()

    update_todo_payload("abc123", title="Updated", client=client)

    _, params, _ = client.calls[0]
    assert params["auth-token"] == "env-token"
    assert params["id"] == "abc123"


def test_update_todo_payload_uses_keychain_token_when_env_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("THINGS_AUTH_TOKEN", raising=False)
    monkeypatch.setattr("app.tools._keychain_get_token", lambda: "kc-token")
    client = StubClient()

    update_todo_payload("abc123", title="Updated", client=client)

    _, params, _ = client.calls[0]
    assert params["auth-token"] == "kc-token"


def test_update_todo_payload_maps_high_value_fields() -> None:
    client = StubClient()

    update_todo_payload(
        "abc123",
        prepend_notes="P",
        append_notes="A",
        add_tags=["extra"],
        checklist_items=["a", "b"],
        prepend_checklist_items=["first"],
        append_checklist_items=["last"],
        list_name="Today",
        heading_id="head-1",
        duplicate=True,
        auth_token="token",
        client=client,
    )

    _, params, _ = client.calls[0]
    assert params["prepend-notes"] == "P"
    assert params["append-notes"] == "A"
    assert params["add-tags"] == ["extra"]
    assert params["checklist-items"] == ["a", "b"]
    assert params["prepend-checklist-items"] == ["first"]
    assert params["append-checklist-items"] == ["last"]
    assert params["list"] == "Today"
    assert params["heading-id"] == "head-1"
    assert params["duplicate"] is True


def test_update_todo_payload_requires_changes() -> None:
    client = StubClient()

    with pytest.raises(ThingsValidationError, match="At least one field"):
        update_todo_payload("abc123", auth_token="token", client=client)


def test_update_todo_payload_requires_token(monkeypatch: pytest.MonkeyPatch) -> None:
    client = StubClient()
    monkeypatch.delenv("THINGS_AUTH_TOKEN", raising=False)
    monkeypatch.setattr("app.tools._keychain_get_token", lambda: None)

    with pytest.raises(ThingsValidationError, match="auth_token"):
        update_todo_payload("abc123", title="Updated", auth_token=None, client=client)


def test_add_project_payload_uses_project_command() -> None:
    client = StubClient()

    add_project_payload(title="Launch Project", area_id="area-1", client=client)

    command, params, _ = client.calls[0]
    assert command == "add-project"
    assert params["title"] == "Launch Project"
    assert params["area-id"] == "area-1"


def test_add_project_payload_maps_todos_and_dates() -> None:
    client = StubClient()

    add_project_payload(
        title="Launch Project",
        to_dos=["Task 1", "Task 2"],
        creation_date="2026-01-01",
        completion_date="2026-01-02T12:00:00Z",
        client=client,
    )

    _, params, _ = client.calls[0]
    assert params["to-dos"] == ["Task 1", "Task 2"]
    assert params["creation-date"] == "2026-01-01"
    assert params["completion-date"] == "2026-01-02T12:00:00Z"


def test_show_payload_requires_id_or_query() -> None:
    client = StubClient()

    with pytest.raises(ThingsValidationError, match="Either 'id' or 'query'"):
        show_payload(client=client)


def test_show_payload_prefers_id_when_both_provided() -> None:
    client = StubClient()

    show_payload(id="project-1", query="Today", filter_tags=["work"], client=client)

    command, params, _ = client.calls[0]
    assert command == "show"
    assert params["id"] == "project-1"
    assert "query" not in params
    assert params["filter"] == ["work"]


def test_search_payload_uses_search_command() -> None:
    client = StubClient()

    search_payload(query="inbox", client=client)

    command, params, _ = client.calls[0]
    assert command == "search"
    assert params["query"] == "inbox"


def test_update_project_payload_requires_token(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("THINGS_AUTH_TOKEN", raising=False)
    client = StubClient()

    with pytest.raises(ThingsValidationError, match="auth_token"):
        update_project_payload("project-1", title="Updated", client=client)


def test_update_project_payload_uses_update_project_command() -> None:
    client = StubClient()

    update_project_payload(
        "project-1",
        title="Updated",
        add_tags=["ops"],
        auth_token="token-1",
        client=client,
    )

    command, params, _ = client.calls[0]
    assert command == "update-project"
    assert params["id"] == "project-1"
    assert params["auth-token"] == "token-1"
    assert params["add-tags"] == ["ops"]


def test_import_json_payload_create_only_does_not_require_token() -> None:
    client = StubClient()

    import_json_payload(
        [{"type": "to-do", "attributes": {"title": "Buy milk"}}],
        client=client,
    )

    command, params, _ = client.calls[0]
    assert command == "json"
    assert "auth-token" not in params
    assert "\"title\":\"Buy milk\"" in params["data"]


def test_import_json_payload_update_requires_token(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("THINGS_AUTH_TOKEN", raising=False)
    client = StubClient()

    with pytest.raises(ThingsValidationError, match="auth_token"):
        import_json_payload(
            [{"type": "to-do", "operation": "update", "id": "abc", "attributes": {"title": "X"}}],
            client=client,
        )


def test_import_json_payload_uses_env_token_for_update(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("THINGS_AUTH_TOKEN", "env-token")
    client = StubClient()

    import_json_payload(
        [{"type": "to-do", "operation": "update", "id": "abc", "attributes": {"title": "X"}}],
        client=client,
    )

    _, params, _ = client.calls[0]
    assert params["auth-token"] == "env-token"


def test_import_json_payload_uses_keychain_token_for_update(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("THINGS_AUTH_TOKEN", raising=False)
    monkeypatch.setattr("app.tools._keychain_get_token", lambda: "kc-token")
    client = StubClient()

    import_json_payload(
        [{"type": "to-do", "operation": "update", "id": "abc", "attributes": {"title": "X"}}],
        client=client,
    )

    _, params, _ = client.calls[0]
    assert params["auth-token"] == "kc-token"


def test_import_json_payload_validates_json_string() -> None:
    client = StubClient()

    with pytest.raises(ThingsValidationError, match="valid JSON"):
        import_json_payload("{invalid-json", client=client)


def test_import_json_payload_detects_nested_update_operations(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("THINGS_AUTH_TOKEN", raising=False)
    client = StubClient()

    nested_payload = [
        {
            "type": "project",
            "attributes": {"title": "Parent"},
            "to-dos": [
                {
                    "type": "to-do",
                    "operation": "update",
                    "id": "todo-1",
                    "attributes": {"title": "Child update"},
                }
            ],
        }
    ]

    with pytest.raises(ThingsValidationError, match="auth_token"):
        import_json_payload(nested_payload, client=client)


def test_import_json_payload_allows_explicit_token_without_updates() -> None:
    client = StubClient()

    import_json_payload(
        [{"type": "to-do", "attributes": {"title": "Create only"}}],
        auth_token="token-optional",
        reveal=True,
        client=client,
    )

    _, params, _ = client.calls[0]
    assert params["auth-token"] == "token-optional"
    assert params["reveal"] is True


def test_import_json_payload_rejects_null_data() -> None:
    client = StubClient()

    with pytest.raises(ThingsValidationError, match="cannot be null"):
        import_json_payload(None, client=client)  # type: ignore[arg-type]


def test_import_json_payload_rejects_invalid_operation_value() -> None:
    client = StubClient()

    with pytest.raises(ThingsValidationError, match="operation must be 'create' or 'update'"):
        import_json_payload(
            [{"type": "to-do", "operation": "delete", "attributes": {"title": "X"}}],
            client=client,
        )


def test_import_json_payload_rejects_update_without_id_even_with_token() -> None:
    client = StubClient()

    with pytest.raises(ThingsValidationError, match=r"\.id is required for update operations"):
        import_json_payload(
            [{"type": "to-do", "operation": "update", "attributes": {"title": "X"}}],
            auth_token="token-1",
            client=client,
        )


def test_import_json_payload_rejects_non_object_attributes() -> None:
    client = StubClient()

    with pytest.raises(ThingsValidationError, match=r"\.attributes must be an object"):
        import_json_payload(
            [{"type": "to-do", "attributes": "not-an-object"}],
            client=client,
        )


def test_read_todos_payload_returns_items() -> None:
    client = StubAppleScriptClient()

    payload = read_todos_payload(
        list_id="today",
        limit=10,
        offset=1,
        status="open",
        project_id="p1",
        area_id="a1",
        deadline_before="2026-03-01",
        deadline_after="2026-02-01",
        completed_before="2026-03-15",
        completed_after="2026-02-15",
        include_notes=True,
        client=client,
    )

    assert payload["ok"] is True
    assert payload["count"] == 1
    assert payload["items"][0]["id"] == "1"
    assert client.list_calls == [
        {
            "list_id": "today",
            "limit": 10,
            "offset": 1,
            "status": "open",
            "project_id": "p1",
            "area_id": "a1",
            "deadline_before": "2026-03-01",
            "deadline_after": "2026-02-01",
            "completed_before": "2026-03-15",
            "completed_after": "2026-02-15",
            "include_notes": True,
        }
    ]


def test_read_todo_payload_returns_single_item() -> None:
    client = StubAppleScriptClient()

    payload = read_todo_payload(todo_id="abc", include_notes=False, client=client)

    assert payload["ok"] is True
    assert payload["item"]["id"] == "abc"
    assert client.get_calls == [{"todo_id": "abc", "include_notes": False}]


def test_find_todos_payload_returns_matches() -> None:
    client = StubAppleScriptClient()

    payload = find_todos_payload(
        query="release",
        limit=5,
        offset=2,
        status="completed",
        project_id="p2",
        area_id="a2",
        deadline_before="2026-03-20",
        deadline_after="2026-03-01",
        completed_before="2026-03-25",
        completed_after="2026-03-02",
        include_notes=True,
        client=client,
    )

    assert payload["ok"] is True
    assert payload["count"] == 1
    assert payload["items"][0]["title"] == "release"
    assert client.search_calls == [
        {
            "query": "release",
            "limit": 5,
            "offset": 2,
            "status": "completed",
            "project_id": "p2",
            "area_id": "a2",
            "deadline_before": "2026-03-20",
            "deadline_after": "2026-03-01",
            "completed_before": "2026-03-25",
            "completed_after": "2026-03-02",
            "include_notes": True,
        }
    ]


def test_read_projects_payload_returns_items() -> None:
    client = StubAppleScriptClient()

    payload = read_projects_payload(
        limit=10,
        offset=1,
        status="open",
        area_id="a1",
        deadline_before="2026-03-01",
        completed_after="2026-02-15",
        include_notes=True,
        client=client,
    )

    assert payload["ok"] is True
    assert payload["count"] == 1
    assert payload["items"][0]["id"] == "p1"
    assert client.project_calls == [
        {
            "limit": 10,
            "offset": 1,
            "status": "open",
            "area_id": "a1",
            "deadline_before": "2026-03-01",
            "deadline_after": None,
            "completed_before": None,
            "completed_after": "2026-02-15",
            "include_notes": True,
        }
    ]


def test_read_areas_payload_returns_items() -> None:
    client = StubAppleScriptClient()

    payload = read_areas_payload(client=client)

    assert payload["ok"] is True
    assert payload["count"] == 1
    assert payload["items"][0]["id"] == "a1"
    assert client.area_calls == 1


def test_read_headings_payload_returns_items() -> None:
    client = StubAppleScriptClient()

    payload = read_headings_payload(
        limit=25,
        offset=2,
        project_id="p1",
        query="shipping",
        client=client,
    )

    assert payload["ok"] is True
    assert payload["count"] == 1
    assert payload["items"][0]["id"] == "h1"
    assert client.heading_calls == [
        {
            "limit": 25,
            "offset": 2,
            "project_id": "p1",
            "query": "shipping",
        }
    ]


def test_auth_set_token_payload_stores_token(monkeypatch: pytest.MonkeyPatch) -> None:
    called: list[str] = []
    monkeypatch.setattr("app.tools._keychain_set_token", lambda token: called.append(token))

    payload = auth_set_token_payload(" token-1 ")

    assert payload["ok"] is True
    assert called == ["token-1"]


def test_auth_clear_token_payload_clears_token(monkeypatch: pytest.MonkeyPatch) -> None:
    called = {"cleared": False}
    monkeypatch.setattr("app.tools._keychain_clear_token", lambda: called.__setitem__("cleared", True))

    payload = auth_clear_token_payload()

    assert payload["ok"] is True
    assert called["cleared"] is True


def test_auth_status_payload_reports_sources(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("THINGS_AUTH_TOKEN", "env-token")
    monkeypatch.setattr("app.tools._keychain_has_token", lambda: True)

    payload = auth_status_payload()

    assert payload["ok"] is True
    assert payload["has_env_token"] is True
    assert payload["has_keychain_token"] is True
    assert payload["active_source"] == "env"
