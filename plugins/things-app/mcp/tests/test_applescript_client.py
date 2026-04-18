from __future__ import annotations

import pytest

from app.applescript_client import (
    AppleScriptThingsClient,
    _classify_applescript_error,
    _normalize_filter_status,
    _normalize_status,
)
from app.things_client import ThingsClientError, ThingsValidationError


class FakeRunner:
    def __init__(self, output: str) -> None:
        self.output = output
        self.scripts: list[str] = []

    def __call__(self, script: str) -> str:
        self.scripts.append(script)
        return self.output


def test_list_todos_parses_rows() -> None:
    runner = FakeRunner(
        "1||Task A||open||2026-03-01|| ||Home, Mac||p1||Project A||a1||Area A||Note A\n"
        "2||Task B||completed||||2026-03-02|| || || || ||"
    )
    client = AppleScriptThingsClient(runner=runner)

    items = client.list_todos(list_id="today", limit=2)

    assert len(items) == 2
    assert items[0]["id"] == "1"
    assert items[1]["title"] == "Task B"
    assert items[0]["project_id"] == "p1"
    assert items[0]["notes"] == "Note A"
    assert items[0]["status_raw"] == "open"
    assert items[0]["status"] == "open"
    assert items[1]["status"] == "completed"
    assert 'to dos of list "Today"' in runner.scripts[0]


def test_parse_rows_normalizes_missing_value() -> None:
    runner = FakeRunner("1||Task A||open||missing value||missing value|||||||")
    client = AppleScriptThingsClient(runner=runner)

    items = client.list_todos(limit=10)

    assert items[0]["deadline"] == ""
    assert items[0]["completion_date"] == ""


def test_normalize_status_values() -> None:
    assert _normalize_status("") == "open"
    assert _normalize_status("Open") == "open"
    assert _normalize_status("completed") == "completed"
    assert _normalize_status("done") == "completed"
    assert _normalize_status("cancelled") == "canceled"
    assert _normalize_status("CANCELED") == "canceled"


def test_normalize_filter_status_values() -> None:
    assert _normalize_filter_status("open") == "open"
    assert _normalize_filter_status("completed") == "completed"
    assert _normalize_filter_status("canceled") == "canceled"


def test_normalize_filter_status_rejects_invalid_value() -> None:
    with pytest.raises(ThingsValidationError, match="THINGS_INVALID_STATUS"):
        _normalize_filter_status("pending")


def test_list_todos_rejects_bad_list() -> None:
    client = AppleScriptThingsClient(runner=FakeRunner(""))

    with pytest.raises(ThingsValidationError, match="Unsupported list_id"):
        client.list_todos(list_id="deadlines")


def test_get_todo_requires_id() -> None:
    client = AppleScriptThingsClient(runner=FakeRunner(""))

    with pytest.raises(ThingsValidationError, match="todo_id"):
        client.get_todo(todo_id=" ")


def test_get_todo_returns_single_item() -> None:
    client = AppleScriptThingsClient(
        runner=FakeRunner("abc||My Task||open|| || ||Home||p1||Proj||a1||Area||Some notes")
    )

    item = client.get_todo(todo_id="abc")

    assert item["id"] == "abc"
    assert item["title"] == "My Task"
    assert item["status"] == "open"
    assert item["notes"] == "Some notes"


def test_get_todo_raises_when_missing() -> None:
    client = AppleScriptThingsClient(runner=FakeRunner(""))

    with pytest.raises(ThingsClientError, match="THINGS_ITEM_NOT_FOUND"):
        client.get_todo(todo_id="abc")


def test_search_todos_requires_query() -> None:
    client = AppleScriptThingsClient(runner=FakeRunner(""))

    with pytest.raises(ThingsValidationError, match="query"):
        client.search_todos(query=" ")


def test_search_todos_parses_results() -> None:
    client = AppleScriptThingsClient(
        runner=FakeRunner("x1||Release prep||open||||||p1||Proj||a1||Area||")
    )

    items = client.search_todos(query="Release", limit=1)

    assert len(items) == 1
    assert items[0]["id"] == "x1"
    assert items[0]["title"] == "Release prep"


def test_list_todos_filters_and_offset() -> None:
    row1 = "||".join(["1", "Task A", "open", "2026-03-01T12:00:00", "", "", "p1", "Proj", "a1", "Area", ""])
    row2 = "||".join(
        ["2", "Task B", "completed", "", "2026-03-02T12:00:00", "", "p1", "Proj", "a1", "Area", ""]
    )
    row3 = "||".join(["3", "Task C", "open", "2026-03-03T12:00:00", "", "", "p2", "Proj2", "a2", "Area2", ""])
    rows = "\n".join([row1, row2, row3])
    client = AppleScriptThingsClient(runner=FakeRunner(rows))

    items = client.list_todos(status="open", project_id="p1", limit=1, offset=0)
    assert [item["id"] for item in items] == ["1"]

    items_with_offset = client.list_todos(status="open", limit=1, offset=1)
    assert [item["id"] for item in items_with_offset] == ["3"]


def test_list_todos_filters_by_deadline_and_completion() -> None:
    row1 = "||".join(["1", "Task A", "open", "2026-03-01T12:00:00", "", "", "p1", "Proj", "a1", "Area", ""])
    row2 = "||".join(
        ["2", "Task B", "completed", "2026-03-04T12:00:00", "2026-03-05T12:00:00", "", "p1", "Proj", "a1", "Area", ""]
    )
    row3 = "||".join(
        ["3", "Task C", "completed", "2026-03-10T12:00:00", "2026-03-12T12:00:00", "", "p2", "Proj2", "a2", "Area2", ""]
    )
    client = AppleScriptThingsClient(runner=FakeRunner("\n".join([row1, row2, row3])))

    items = client.list_todos(deadline_before="2026-03-06", completed_after="2026-03-01")

    assert [item["id"] for item in items] == ["2"]


def test_list_projects_parses_rows_and_filters() -> None:
    row1 = "||".join(["p1", "Project A", "open", "2026-03-01T12:00:00", "", "work", "a1", "Area A", "Note A"])
    row2 = "||".join(
        ["p2", "Project B", "completed", "2026-03-04T12:00:00", "2026-03-05T12:00:00", "", "a1", "Area A", ""]
    )
    row3 = "||".join(
        ["p3", "Project C", "completed", "2026-03-10T12:00:00", "2026-03-12T12:00:00", "", "a2", "Area B", ""]
    )
    client = AppleScriptThingsClient(runner=FakeRunner("\n".join([row1, row2, row3])))

    items = client.list_projects(status="completed", area_id="a1", completed_after="2026-03-01")

    assert [item["id"] for item in items] == ["p2"]
    assert items[0]["title"] == "Project B"
    assert items[0]["area_title"] == "Area A"
    assert items[0]["status"] == "completed"


def test_list_areas_parses_rows() -> None:
    client = AppleScriptThingsClient(runner=FakeRunner("a1||Area A\na2||Area B"))

    items = client.list_areas()

    assert items == [{"id": "a1", "title": "Area A"}, {"id": "a2", "title": "Area B"}]


def test_list_headings_parses_rows_and_filters() -> None:
    rows = "\n".join(
        [
            "h1||Planning||p1||Project A",
            "h2||Shipping||p1||Project A",
            "h3||Inbox||p2||Project B",
        ]
    )
    client = AppleScriptThingsClient(runner=FakeRunner(rows))

    items = client.list_headings(project_id="p1", query="ship", limit=10, offset=0)

    assert items == [
        {
            "id": "h2",
            "title": "Shipping",
            "project_id": "p1",
            "project_title": "Project A",
        }
    ]


def test_date_filter_rejects_invalid_value() -> None:
    row = "||".join(["1", "Task A", "open", "2026-03-01T12:00:00", "", "", "p1", "Proj", "a1", "Area", ""])
    client = AppleScriptThingsClient(runner=FakeRunner(row))

    with pytest.raises(ThingsValidationError, match="THINGS_INVALID_DATE_FILTER"):
        client.list_todos(deadline_before="next week")


def test_classify_applescript_error_permission_denied() -> None:
    code, message = _classify_applescript_error(
        "Not authorized to send Apple events to Things3. (-1743)"
    )
    assert code == "THINGS_AUTOMATION_DENIED"
    assert "Automation permission denied" in message


def test_classify_applescript_error_app_unavailable() -> None:
    code, message = _classify_applescript_error("Application isn't running. (-600)")
    assert code == "THINGS_APP_UNAVAILABLE"
    assert "not running" in message


def test_classify_applescript_error_fallback() -> None:
    code, message = _classify_applescript_error("some random script failure")
    assert code == "THINGS_SCRIPT_FAILED"
    assert "execution failed" in message
