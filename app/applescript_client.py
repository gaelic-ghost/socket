from __future__ import annotations

import subprocess
from datetime import UTC, datetime
from typing import Callable

from app.things_client import ThingsClientError, ThingsValidationError


_FIELD_SEPARATOR = "||"
_LIST_NAME_MAP: dict[str, str] = {
    "inbox": "Inbox",
    "today": "Today",
    "anytime": "Anytime",
    "upcoming": "Upcoming",
    "someday": "Someday",
    "logbook": "Logbook",
}


class AppleScriptThingsClient:
    def __init__(self, runner: Callable[[str], str] | None = None) -> None:
        self._runner = runner or _run_applescript

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
        if limit <= 0:
            raise ThingsValidationError("'limit' must be greater than 0")
        if offset < 0:
            raise ThingsValidationError("'offset' must be greater than or equal to 0")

        list_name = _normalize_list_name(list_id)
        if list_name is None:
            scope_expr = "to dos"
        else:
            scope_expr = f'to dos of list "{_escape_applescript_text(list_name)}"'

        include_notes_literal = "true" if include_notes else "false"
        script = f'''
            on flatten_text(inputText)
                set outputText to inputText as text
                set oldTIDs to AppleScript's text item delimiters
                set AppleScript's text item delimiters to {{return, linefeed, tab}}
                set parts to text items of outputText
                set AppleScript's text item delimiters to " "
                set outputText to parts as text
                set AppleScript's text item delimiters to oldTIDs
                return outputText
            end flatten_text

            on pad2(n)
                if n < 10 then return "0" & n
                return n as text
            end pad2

            on iso_date(d)
                set y to year of d as integer
                set m to month of d as integer
                set dayNumber to day of d as integer
                set h to hours of d as integer
                set minNumber to minutes of d as integer
                set secNumber to seconds of d as integer
                return (y as text) & "-" & my pad2(m) & "-" & my pad2(dayNumber) & "T" & my pad2(h) & ":" & my pad2(minNumber) & ":" & my pad2(secNumber)
            end iso_date

            tell application "Things3"
                set todoItems to {scope_expr}
                set outputText to ""
                repeat with td in todoItems
                    set tdId to (id of td as text)
                    set tdTitle to (name of td as text)
                    set tdStatus to ""
                    set tdDueDate to ""
                    set tdCompletionDate to ""
                    set tdTagNames to ""
                    set tdProjectId to ""
                    set tdProjectTitle to ""
                    set tdAreaId to ""
                    set tdAreaTitle to ""
                    set tdNotes to ""

                    try
                        set tdStatus to (status of td as text)
                    end try
                    try
                        set tdDueDate to my iso_date(due date of td)
                    end try
                    try
                        set tdCompletionDate to my iso_date(completion date of td)
                    end try
                    try
                        set tdTagNames to (tag names of td as text)
                    end try
                    try
                        set tdProjectRef to project of td
                        set tdProjectId to (id of tdProjectRef as text)
                        set tdProjectTitle to (name of tdProjectRef as text)
                    end try
                    try
                        set tdAreaRef to area of td
                        set tdAreaId to (id of tdAreaRef as text)
                        set tdAreaTitle to (name of tdAreaRef as text)
                    on error
                        try
                            if tdProjectId is not "" then
                                set tdAreaRef to area of tdProjectRef
                                set tdAreaId to (id of tdAreaRef as text)
                                set tdAreaTitle to (name of tdAreaRef as text)
                            end if
                        end try
                    end try
                    if {include_notes_literal} then
                        try
                            set tdNotes to my flatten_text(notes of td as text)
                        end try
                    end if

                    set rowText to tdId & "{_FIELD_SEPARATOR}" & tdTitle & "{_FIELD_SEPARATOR}" & tdStatus & "{_FIELD_SEPARATOR}" & tdDueDate & "{_FIELD_SEPARATOR}" & tdCompletionDate & "{_FIELD_SEPARATOR}" & tdTagNames & "{_FIELD_SEPARATOR}" & tdProjectId & "{_FIELD_SEPARATOR}" & tdProjectTitle & "{_FIELD_SEPARATOR}" & tdAreaId & "{_FIELD_SEPARATOR}" & tdAreaTitle & "{_FIELD_SEPARATOR}" & tdNotes
                    if outputText is "" then
                        set outputText to rowText
                    else
                        set outputText to outputText & linefeed & rowText
                    end if
                end repeat
                return outputText
            end tell
        '''

        raw = self._runner(script)
        rows = _parse_rows(raw)
        return _filter_todos(
            rows,
            limit=limit,
            offset=offset,
            status=status,
            project_id=project_id,
            area_id=area_id,
            deadline_before=deadline_before,
            deadline_after=deadline_after,
            completed_before=completed_before,
            completed_after=completed_after,
        )

    def get_todo(self, *, todo_id: str, include_notes: bool = True) -> dict[str, str]:
        normalized_id = todo_id.strip()
        if not normalized_id:
            raise ThingsValidationError("'todo_id' is required")

        include_notes_literal = "true" if include_notes else "false"
        script = f'''
            on flatten_text(inputText)
                set outputText to inputText as text
                set oldTIDs to AppleScript's text item delimiters
                set AppleScript's text item delimiters to {{return, linefeed, tab}}
                set parts to text items of outputText
                set AppleScript's text item delimiters to " "
                set outputText to parts as text
                set AppleScript's text item delimiters to oldTIDs
                return outputText
            end flatten_text

            on pad2(n)
                if n < 10 then return "0" & n
                return n as text
            end pad2

            on iso_date(d)
                set y to year of d as integer
                set m to month of d as integer
                set dayNumber to day of d as integer
                set h to hours of d as integer
                set minNumber to minutes of d as integer
                set secNumber to seconds of d as integer
                return (y as text) & "-" & my pad2(m) & "-" & my pad2(dayNumber) & "T" & my pad2(h) & ":" & my pad2(minNumber) & ":" & my pad2(secNumber)
            end iso_date

            tell application "Things3"
                set td to to do id "{_escape_applescript_text(normalized_id)}"
                set tdId to (id of td as text)
                set tdTitle to (name of td as text)
                set tdStatus to ""
                set tdDueDate to ""
                set tdCompletionDate to ""
                set tdTagNames to ""
                set tdProjectId to ""
                set tdProjectTitle to ""
                set tdAreaId to ""
                set tdAreaTitle to ""
                set tdNotes to ""

                try
                    set tdStatus to (status of td as text)
                end try
                try
                    set tdDueDate to my iso_date(due date of td)
                end try
                try
                    set tdCompletionDate to my iso_date(completion date of td)
                end try
                try
                    set tdTagNames to (tag names of td as text)
                end try
                try
                    set tdProjectRef to project of td
                    set tdProjectId to (id of tdProjectRef as text)
                    set tdProjectTitle to (name of tdProjectRef as text)
                end try
                try
                    set tdAreaRef to area of td
                    set tdAreaId to (id of tdAreaRef as text)
                    set tdAreaTitle to (name of tdAreaRef as text)
                on error
                    try
                        if tdProjectId is not "" then
                            set tdAreaRef to area of tdProjectRef
                            set tdAreaId to (id of tdAreaRef as text)
                            set tdAreaTitle to (name of tdAreaRef as text)
                        end if
                    end try
                end try
                if {include_notes_literal} then
                    try
                        set tdNotes to my flatten_text(notes of td as text)
                    end try
                end if

                return tdId & "{_FIELD_SEPARATOR}" & tdTitle & "{_FIELD_SEPARATOR}" & tdStatus & "{_FIELD_SEPARATOR}" & tdDueDate & "{_FIELD_SEPARATOR}" & tdCompletionDate & "{_FIELD_SEPARATOR}" & tdTagNames & "{_FIELD_SEPARATOR}" & tdProjectId & "{_FIELD_SEPARATOR}" & tdProjectTitle & "{_FIELD_SEPARATOR}" & tdAreaId & "{_FIELD_SEPARATOR}" & tdAreaTitle & "{_FIELD_SEPARATOR}" & tdNotes
            end tell
        '''

        raw = self._runner(script)
        rows = _parse_rows(raw)
        if not rows:
            raise ThingsClientError(f"THINGS_ITEM_NOT_FOUND: No to-do found for id '{normalized_id}'")
        return rows[0]

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
        normalized_query = query.strip()
        if not normalized_query:
            raise ThingsValidationError("'query' is required")
        if limit <= 0:
            raise ThingsValidationError("'limit' must be greater than 0")
        if offset < 0:
            raise ThingsValidationError("'offset' must be greater than or equal to 0")

        include_notes_literal = "true" if include_notes else "false"
        script = f'''
            on flatten_text(inputText)
                set outputText to inputText as text
                set oldTIDs to AppleScript's text item delimiters
                set AppleScript's text item delimiters to {{return, linefeed, tab}}
                set parts to text items of outputText
                set AppleScript's text item delimiters to " "
                set outputText to parts as text
                set AppleScript's text item delimiters to oldTIDs
                return outputText
            end flatten_text

            on pad2(n)
                if n < 10 then return "0" & n
                return n as text
            end pad2

            on iso_date(d)
                set y to year of d as integer
                set m to month of d as integer
                set dayNumber to day of d as integer
                set h to hours of d as integer
                set minNumber to minutes of d as integer
                set secNumber to seconds of d as integer
                return (y as text) & "-" & my pad2(m) & "-" & my pad2(dayNumber) & "T" & my pad2(h) & ":" & my pad2(minNumber) & ":" & my pad2(secNumber)
            end iso_date

            tell application "Things3"
                set outputText to ""
                repeat with td in to dos
                    set tdName to (name of td as text)
                    considering case
                        set isMatch to (tdName contains "{_escape_applescript_text(normalized_query)}")
                    end considering
                    if isMatch then
                        set tdId to (id of td as text)
                        set tdStatus to ""
                        set tdDueDate to ""
                        set tdCompletionDate to ""
                        set tdTagNames to ""
                        set tdProjectId to ""
                        set tdProjectTitle to ""
                        set tdAreaId to ""
                        set tdAreaTitle to ""
                        set tdNotes to ""

                        try
                            set tdStatus to (status of td as text)
                        end try
                        try
                            set tdDueDate to my iso_date(due date of td)
                        end try
                        try
                            set tdCompletionDate to my iso_date(completion date of td)
                        end try
                        try
                            set tdTagNames to (tag names of td as text)
                        end try
                        try
                            set tdProjectRef to project of td
                            set tdProjectId to (id of tdProjectRef as text)
                            set tdProjectTitle to (name of tdProjectRef as text)
                        end try
                        try
                            set tdAreaRef to area of td
                            set tdAreaId to (id of tdAreaRef as text)
                            set tdAreaTitle to (name of tdAreaRef as text)
                        on error
                            try
                                if tdProjectId is not "" then
                                    set tdAreaRef to area of tdProjectRef
                                    set tdAreaId to (id of tdAreaRef as text)
                                    set tdAreaTitle to (name of tdAreaRef as text)
                                end if
                            end try
                        end try
                        if {include_notes_literal} then
                            try
                                set tdNotes to my flatten_text(notes of td as text)
                            end try
                        end if

                        set rowText to tdId & "{_FIELD_SEPARATOR}" & tdName & "{_FIELD_SEPARATOR}" & tdStatus & "{_FIELD_SEPARATOR}" & tdDueDate & "{_FIELD_SEPARATOR}" & tdCompletionDate & "{_FIELD_SEPARATOR}" & tdTagNames & "{_FIELD_SEPARATOR}" & tdProjectId & "{_FIELD_SEPARATOR}" & tdProjectTitle & "{_FIELD_SEPARATOR}" & tdAreaId & "{_FIELD_SEPARATOR}" & tdAreaTitle & "{_FIELD_SEPARATOR}" & tdNotes
                        if outputText is "" then
                            set outputText to rowText
                        else
                            set outputText to outputText & linefeed & rowText
                        end if
                    end if
                end repeat
                return outputText
            end tell
        '''

        raw = self._runner(script)
        rows = _parse_rows(raw)
        return _filter_todos(
            rows,
            limit=limit,
            offset=offset,
            status=status,
            project_id=project_id,
            area_id=area_id,
            deadline_before=deadline_before,
            deadline_after=deadline_after,
            completed_before=completed_before,
            completed_after=completed_after,
        )

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
        if limit <= 0:
            raise ThingsValidationError("'limit' must be greater than 0")
        if offset < 0:
            raise ThingsValidationError("'offset' must be greater than or equal to 0")

        include_notes_literal = "true" if include_notes else "false"
        script = f'''
            on flatten_text(inputText)
                set outputText to inputText as text
                set oldTIDs to AppleScript's text item delimiters
                set AppleScript's text item delimiters to {{return, linefeed, tab}}
                set parts to text items of outputText
                set AppleScript's text item delimiters to " "
                set outputText to parts as text
                set AppleScript's text item delimiters to oldTIDs
                return outputText
            end flatten_text

            on pad2(n)
                if n < 10 then return "0" & n
                return n as text
            end pad2

            on iso_date(d)
                set y to year of d as integer
                set m to month of d as integer
                set dayNumber to day of d as integer
                set h to hours of d as integer
                set minNumber to minutes of d as integer
                set secNumber to seconds of d as integer
                return (y as text) & "-" & my pad2(m) & "-" & my pad2(dayNumber) & "T" & my pad2(h) & ":" & my pad2(minNumber) & ":" & my pad2(secNumber)
            end iso_date

            tell application "Things3"
                set outputText to ""
                repeat with pr in projects
                    set prId to (id of pr as text)
                    set prTitle to (name of pr as text)
                    set prStatus to ""
                    set prDueDate to ""
                    set prCompletionDate to ""
                    set prTagNames to ""
                    set prAreaId to ""
                    set prAreaTitle to ""
                    set prNotes to ""

                    try
                        set prStatus to (status of pr as text)
                    end try
                    try
                        set prDueDate to my iso_date(due date of pr)
                    end try
                    try
                        set prCompletionDate to my iso_date(completion date of pr)
                    end try
                    try
                        set prTagNames to (tag names of pr as text)
                    end try
                    try
                        set prAreaRef to area of pr
                        set prAreaId to (id of prAreaRef as text)
                        set prAreaTitle to (name of prAreaRef as text)
                    end try
                    if {include_notes_literal} then
                        try
                            set prNotes to my flatten_text(notes of pr as text)
                        end try
                    end if

                    set rowText to prId & "{_FIELD_SEPARATOR}" & prTitle & "{_FIELD_SEPARATOR}" & prStatus & "{_FIELD_SEPARATOR}" & prDueDate & "{_FIELD_SEPARATOR}" & prCompletionDate & "{_FIELD_SEPARATOR}" & prTagNames & "{_FIELD_SEPARATOR}" & prAreaId & "{_FIELD_SEPARATOR}" & prAreaTitle & "{_FIELD_SEPARATOR}" & prNotes
                    if outputText is "" then
                        set outputText to rowText
                    else
                        set outputText to outputText & linefeed & rowText
                    end if
                end repeat
                return outputText
            end tell
        '''

        raw = self._runner(script)
        rows = _parse_project_rows(raw)
        return _filter_projects(
            rows,
            limit=limit,
            offset=offset,
            status=status,
            area_id=area_id,
            deadline_before=deadline_before,
            deadline_after=deadline_after,
            completed_before=completed_before,
            completed_after=completed_after,
        )

    def list_areas(self) -> list[dict[str, str]]:
        script = f'''
            tell application "Things3"
                set outputText to ""
                repeat with ar in areas
                    set arId to (id of ar as text)
                    set arTitle to (name of ar as text)
                    set rowText to arId & "{_FIELD_SEPARATOR}" & arTitle
                    if outputText is "" then
                        set outputText to rowText
                    else
                        set outputText to outputText & linefeed & rowText
                    end if
                end repeat
                return outputText
            end tell
        '''
        raw = self._runner(script)
        return _parse_area_rows(raw)

    def list_headings(
        self,
        *,
        limit: int = 200,
        offset: int = 0,
        project_id: str | None = None,
        query: str | None = None,
    ) -> list[dict[str, str]]:
        if limit <= 0:
            raise ThingsValidationError("'limit' must be greater than 0")
        if offset < 0:
            raise ThingsValidationError("'offset' must be greater than or equal to 0")

        script = f'''
            tell application "Things3"
                set outputText to ""
                repeat with pr in projects
                    set prRef to contents of pr
                    set prId to (id of prRef as text)
                    set prTitle to (name of prRef as text)
                    repeat with td in to dos of prRef
                        try
                            set tdType to ""
                            set tdType to (type of td as text)
                            if tdType contains "heading" then
                                set hdId to (id of td as text)
                                set hdTitle to (name of td as text)
                                set rowText to hdId & "{_FIELD_SEPARATOR}" & hdTitle & "{_FIELD_SEPARATOR}" & prId & "{_FIELD_SEPARATOR}" & prTitle
                                if outputText is "" then
                                    set outputText to rowText
                                else
                                    set outputText to outputText & linefeed & rowText
                                end if
                            end if
                        end try
                    end repeat
                end repeat
                return outputText
            end tell
        '''
        raw = self._runner(script)
        rows = _parse_heading_rows(raw)
        return _filter_headings(
            rows,
            limit=limit,
            offset=offset,
            project_id=project_id,
            query=query,
        )


def _run_applescript(script: str) -> str:
    try:
        result = subprocess.run(
            ["osascript", "-e", script],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as exc:
        raw_message = (exc.stderr or exc.stdout or str(exc)).strip()
        code, message = _classify_applescript_error(raw_message)
        raise ThingsClientError(f"{code}: {message}. Raw error: {raw_message}") from exc
    return result.stdout.strip()


def _parse_rows(raw: str) -> list[dict[str, str]]:
    if not raw:
        return []
    rows: list[dict[str, str]] = []
    for line in raw.splitlines():
        if not line.strip():
            continue
        parts = line.split(_FIELD_SEPARATOR)
        if len(parts) < 2:
            continue
        while len(parts) < 11:
            parts.append("")
        normalized_parts = [_normalize_applescript_value(part) for part in parts]
        rows.append(
            {
                "id": normalized_parts[0],
                "title": normalized_parts[1],
                "status_raw": normalized_parts[2],
                "status": _normalize_status(normalized_parts[2]),
                "deadline": normalized_parts[3],
                "completion_date": normalized_parts[4],
                "tags": normalized_parts[5],
                "project_id": normalized_parts[6],
                "project_title": normalized_parts[7],
                "area_id": normalized_parts[8],
                "area_title": normalized_parts[9],
                "notes": normalized_parts[10],
            }
        )
    return rows


def _filter_todos(
    rows: list[dict[str, str]],
    *,
    limit: int,
    offset: int,
    status: str | None,
    project_id: str | None,
    area_id: str | None,
    deadline_before: str | None,
    deadline_after: str | None,
    completed_before: str | None,
    completed_after: str | None,
) -> list[dict[str, str]]:
    filtered = rows

    if status and status.strip():
        normalized_status = _normalize_filter_status(status)
        filtered = [item for item in filtered if item.get("status", "").strip().lower() == normalized_status]

    if project_id and project_id.strip():
        normalized_project_id = project_id.strip()
        filtered = [item for item in filtered if item.get("project_id", "") == normalized_project_id]

    if area_id and area_id.strip():
        normalized_area_id = area_id.strip()
        filtered = [item for item in filtered if item.get("area_id", "") == normalized_area_id]

    deadline_before_dt = _parse_filter_datetime(deadline_before, field_name="deadline_before")
    deadline_after_dt = _parse_filter_datetime(deadline_after, field_name="deadline_after")
    completed_before_dt = _parse_filter_datetime(completed_before, field_name="completed_before")
    completed_after_dt = _parse_filter_datetime(completed_after, field_name="completed_after")

    if deadline_before_dt is not None:
        filtered = [
            item for item in filtered if (item_dt := _parse_item_datetime(item.get("deadline", ""))) is not None and item_dt < deadline_before_dt
        ]
    if deadline_after_dt is not None:
        filtered = [
            item for item in filtered if (item_dt := _parse_item_datetime(item.get("deadline", ""))) is not None and item_dt > deadline_after_dt
        ]
    if completed_before_dt is not None:
        filtered = [
            item
            for item in filtered
            if (item_dt := _parse_item_datetime(item.get("completion_date", ""))) is not None and item_dt < completed_before_dt
        ]
    if completed_after_dt is not None:
        filtered = [
            item
            for item in filtered
            if (item_dt := _parse_item_datetime(item.get("completion_date", ""))) is not None and item_dt > completed_after_dt
        ]

    return filtered[offset : offset + limit]


def _parse_project_rows(raw: str) -> list[dict[str, str]]:
    if not raw:
        return []
    rows: list[dict[str, str]] = []
    for line in raw.splitlines():
        if not line.strip():
            continue
        parts = line.split(_FIELD_SEPARATOR)
        if len(parts) < 2:
            continue
        while len(parts) < 9:
            parts.append("")
        normalized_parts = [_normalize_applescript_value(part) for part in parts]
        rows.append(
            {
                "id": normalized_parts[0],
                "title": normalized_parts[1],
                "status_raw": normalized_parts[2],
                "status": _normalize_status(normalized_parts[2]),
                "deadline": normalized_parts[3],
                "completion_date": normalized_parts[4],
                "tags": normalized_parts[5],
                "area_id": normalized_parts[6],
                "area_title": normalized_parts[7],
                "notes": normalized_parts[8],
            }
        )
    return rows


def _parse_area_rows(raw: str) -> list[dict[str, str]]:
    if not raw:
        return []
    rows: list[dict[str, str]] = []
    for line in raw.splitlines():
        if not line.strip():
            continue
        parts = line.split(_FIELD_SEPARATOR)
        if len(parts) < 2:
            continue
        rows.append({"id": _normalize_applescript_value(parts[0]), "title": _normalize_applescript_value(parts[1])})
    return rows


def _parse_heading_rows(raw: str) -> list[dict[str, str]]:
    if not raw:
        return []
    rows: list[dict[str, str]] = []
    for line in raw.splitlines():
        if not line.strip():
            continue
        parts = line.split(_FIELD_SEPARATOR)
        if len(parts) < 2:
            continue
        while len(parts) < 4:
            parts.append("")
        normalized_parts = [_normalize_applescript_value(part) for part in parts]
        rows.append(
            {
                "id": normalized_parts[0],
                "title": normalized_parts[1],
                "project_id": normalized_parts[2],
                "project_title": normalized_parts[3],
            }
        )
    return rows


def _filter_projects(
    rows: list[dict[str, str]],
    *,
    limit: int,
    offset: int,
    status: str | None,
    area_id: str | None,
    deadline_before: str | None,
    deadline_after: str | None,
    completed_before: str | None,
    completed_after: str | None,
) -> list[dict[str, str]]:
    filtered = rows
    if status and status.strip():
        normalized_status = _normalize_filter_status(status)
        filtered = [item for item in filtered if item.get("status", "").strip().lower() == normalized_status]
    if area_id and area_id.strip():
        normalized_area_id = area_id.strip()
        filtered = [item for item in filtered if item.get("area_id", "") == normalized_area_id]

    deadline_before_dt = _parse_filter_datetime(deadline_before, field_name="deadline_before")
    deadline_after_dt = _parse_filter_datetime(deadline_after, field_name="deadline_after")
    completed_before_dt = _parse_filter_datetime(completed_before, field_name="completed_before")
    completed_after_dt = _parse_filter_datetime(completed_after, field_name="completed_after")

    if deadline_before_dt is not None:
        filtered = [
            item for item in filtered if (item_dt := _parse_item_datetime(item.get("deadline", ""))) is not None and item_dt < deadline_before_dt
        ]
    if deadline_after_dt is not None:
        filtered = [
            item for item in filtered if (item_dt := _parse_item_datetime(item.get("deadline", ""))) is not None and item_dt > deadline_after_dt
        ]
    if completed_before_dt is not None:
        filtered = [
            item
            for item in filtered
            if (item_dt := _parse_item_datetime(item.get("completion_date", ""))) is not None and item_dt < completed_before_dt
        ]
    if completed_after_dt is not None:
        filtered = [
            item
            for item in filtered
            if (item_dt := _parse_item_datetime(item.get("completion_date", ""))) is not None and item_dt > completed_after_dt
        ]

    return filtered[offset : offset + limit]


def _filter_headings(
    rows: list[dict[str, str]],
    *,
    limit: int,
    offset: int,
    project_id: str | None,
    query: str | None,
) -> list[dict[str, str]]:
    filtered = rows
    if project_id and project_id.strip():
        normalized_project_id = project_id.strip()
        filtered = [item for item in filtered if item.get("project_id", "") == normalized_project_id]

    if query and query.strip():
        normalized_query = query.strip().lower()
        filtered = [item for item in filtered if normalized_query in item.get("title", "").lower()]

    return filtered[offset : offset + limit]


def _parse_filter_datetime(value: str | None, *, field_name: str) -> datetime | None:
    if value is None or not value.strip():
        return None
    parsed = _parse_datetime(value.strip())
    if parsed is None:
        raise ThingsValidationError(
            f"THINGS_INVALID_DATE_FILTER: '{field_name}' must be an ISO-8601 date or datetime"
        )
    return parsed


def _parse_item_datetime(value: str) -> datetime | None:
    if not value:
        return None
    return _parse_datetime(value)


def _parse_datetime(value: str) -> datetime | None:
    normalized = value.strip().replace("Z", "+00:00")
    if not normalized:
        return None
    try:
        dt = datetime.fromisoformat(normalized)
    except ValueError:
        return None
    if dt.tzinfo is None:
        return dt
    return dt.astimezone(UTC).replace(tzinfo=None)


def _normalize_list_name(list_id: str | None) -> str | None:
    if list_id is None:
        return None
    key = list_id.strip().lower()
    if not key or key == "all":
        return None
    if key not in _LIST_NAME_MAP:
        supported = ", ".join(sorted([*list(_LIST_NAME_MAP.keys()), "all"]))
        raise ThingsValidationError(
            f"THINGS_INVALID_LIST: Unsupported list_id '{list_id}'. Supported values: {supported}"
        )
    return _LIST_NAME_MAP[key]


def _escape_applescript_text(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def _normalize_applescript_value(value: str) -> str:
    normalized = value.strip()
    if normalized.lower() == "missing value":
        return ""
    return normalized


def _normalize_status(raw_status: str) -> str:
    normalized = raw_status.strip().lower()
    if not normalized:
        return "open"
    if "cancel" in normalized:
        return "canceled"
    if "complete" in normalized or "done" in normalized:
        return "completed"
    if "open" in normalized or "incomplete" in normalized:
        return "open"
    return normalized


def _normalize_filter_status(status: str) -> str:
    normalized = status.strip().lower()
    allowed = {"open", "completed", "canceled"}
    if normalized not in allowed:
        allowed_values = ", ".join(sorted(allowed))
        raise ThingsValidationError(
            f"THINGS_INVALID_STATUS: Unsupported status '{status}'. Supported values: {allowed_values}"
        )
    return normalized


def _classify_applescript_error(raw_message: str) -> tuple[str, str]:
    message = raw_message.lower()

    if (
        "-1743" in message
        or "not authorized to send apple events" in message
        or "not permitted to send apple events" in message
    ):
        return (
            "THINGS_AUTOMATION_DENIED",
            "Automation permission denied. Allow Terminal/Codex to control Things3 in System Settings > Privacy & Security > Automation",
        )

    if (
        "application isn't running" in message
        or "application isn’t running" in message
        or "can't get application \"things3\"" in message
        or "can’t get application \"things3\"" in message
        or "-600" in message
    ):
        return ("THINGS_APP_UNAVAILABLE", "Things3 is not running or unavailable")

    return ("THINGS_SCRIPT_FAILED", "AppleScript execution failed")
