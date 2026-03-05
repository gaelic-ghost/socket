#!/usr/bin/env python3
"""Build a Things planning digest from exported MCP JSON responses."""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any, Dict

try:
    import yaml
except ImportError:  # pragma: no cover - runtime dependency check
    yaml = None

DEFAULT_SETTINGS: Dict[str, Any] = {
    "dueSoonDays": 3,
    "daysAhead": 4,
    "topProjects": 3,
    "topAreas": 2,
    "maxSuggestions": 5,
    "openCountCap": 10,
    "outputStyle": "operational",
    "scoringWeights": {
        "completed7d": 3.0,
        "dueSoon": 2.0,
        "overdue": 3.0,
        "openCountWeight": 0.5,
        "checklistHints": 1.5,
    },
}


@dataclass
class Activity:
    title: str
    area_title: str = ""
    open_count: int = 0
    due_soon: int = 0
    overdue: int = 0
    completed_7d: int = 0
    checklist_hints: int = 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--areas", required=True, help="Path to areas JSON")
    parser.add_argument("--projects", required=True, help="Path to projects JSON")
    parser.add_argument("--open-todos", required=True, help="Path to open todos JSON")
    parser.add_argument(
        "--recent-done",
        default="",
        help="Path to completed todos JSON (last 7 days preferred)",
    )
    parser.add_argument(
        "--detailed-todos",
        default="",
        help="Path to todo-detail JSON list with notes/checklist-like content",
    )
    parser.add_argument(
        "--days-ahead",
        type=int,
        default=None,
        help="Override planning horizon in days",
    )
    parser.add_argument(
        "--due-soon-days",
        type=int,
        default=None,
        help="Override due-soon horizon in days",
    )
    parser.add_argument(
        "--top-projects",
        type=int,
        default=None,
        help="Override number of top projects in digest",
    )
    parser.add_argument(
        "--top-areas",
        type=int,
        default=None,
        help="Override number of top areas in digest",
    )
    parser.add_argument(
        "--max-suggestions",
        type=int,
        default=None,
        help="Override max number of suggestion bullets",
    )
    parser.add_argument(
        "--open-count-cap",
        type=int,
        default=None,
        help="Override scoring cap applied to open todo counts",
    )
    parser.add_argument(
        "--output-style",
        choices=["operational", "executive"],
        default=None,
        help="Override output style",
    )
    parser.add_argument(
        "--config",
        default="",
        help=(
            "Optional path to customization.yaml. Default resolution uses "
            "config/customization.yaml then config/customization.template.yaml"
        ),
    )
    parser.add_argument(
        "--today",
        default="",
        help="Override date in YYYY-MM-DD (defaults to local today)",
    )
    return parser.parse_args()


def require_yaml() -> None:
    if yaml is None:
        raise RuntimeError(
            "Missing dependency: PyYAML. Run with `uv run --with pyyaml python "
            "scripts/build_digest.py ...`"
        )


def load_yaml_dict(path: Path) -> Dict[str, Any]:
    require_yaml()
    with path.open("r", encoding="utf-8") as handle:
        payload = yaml.safe_load(handle) or {}
    if not isinstance(payload, dict):
        raise ValueError(f"Expected a YAML mapping in {path}")
    return payload


def deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    merged: Dict[str, Any] = deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def resolve_settings(args_config: str) -> tuple[Dict[str, Any], Path, str]:
    script_path = Path(__file__).resolve()
    skill_root = script_path.parent.parent
    template_path = skill_root / "config" / "customization.template.yaml"
    active_path = (
        Path(args_config).expanduser().resolve()
        if args_config
        else (skill_root / "config" / "customization.yaml")
    )

    settings = deepcopy(DEFAULT_SETTINGS)
    source = "hardcoded-defaults"

    if template_path.exists():
        template_payload = load_yaml_dict(template_path)
        template_settings = template_payload.get("settings")
        if isinstance(template_settings, dict):
            settings = deep_merge(settings, template_settings)
        source = str(template_path)

    if active_path.exists():
        active_payload = load_yaml_dict(active_path)
        active_settings = active_payload.get("settings")
        if isinstance(active_settings, dict):
            settings = deep_merge(settings, active_settings)
        source = str(active_path)

    return settings, active_path, source


def read_items(path: str) -> list[dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if isinstance(payload, dict) and isinstance(payload.get("items"), list):
        return [item for item in payload["items"] if isinstance(item, dict)]
    raise ValueError(f"Unsupported JSON shape in {path}")


def parse_date(raw: str) -> date | None:
    if not raw:
        return None
    try:
        return date.fromisoformat(raw[:10])
    except ValueError:
        pass
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(raw, fmt).date()
        except ValueError:
            continue
    return None


def checklist_hint_score(notes: str) -> int:
    if not notes:
        return 0
    markers = ("- [ ]", "- [x]", "[ ]", "[x]", "\n- ", "\n* ", "\n1. ")
    score = sum(1 for marker in markers if marker in notes)
    if notes.count("\n") >= 4:
        score += 1
    return min(score, 3)


def short_task(task: dict[str, Any]) -> str:
    title = str(task.get("title") or "Untitled")
    project = str(task.get("project_title") or "")
    area = str(task.get("area_title") or "")
    if project:
        return f"{title} ({project})"
    if area:
        return f"{title} ({area})"
    return title


def activity_score(activity: Activity, weights: Dict[str, float], open_count_cap: int) -> float:
    return (
        activity.completed_7d * weights["completed7d"]
        + activity.due_soon * weights["dueSoon"]
        + activity.overdue * weights["overdue"]
        + min(activity.open_count, open_count_cap) * weights["openCountWeight"]
        + activity.checklist_hints * weights["checklistHints"]
    )


def inc_activity(
    table: dict[str, Activity], key: str, title: str, area_title: str = ""
) -> Activity:
    entry = table.get(key)
    if entry is None:
        entry = Activity(title=title, area_title=area_title)
        table[key] = entry
    return entry


def normalize_weights(raw: Any) -> Dict[str, float]:
    weights = dict(DEFAULT_SETTINGS["scoringWeights"])
    if not isinstance(raw, dict):
        return weights

    for key in ("completed7d", "dueSoon", "overdue", "openCountWeight", "checklistHints"):
        value = raw.get(key)
        if isinstance(value, (int, float)):
            weights[key] = float(value)

    return weights


def render_digest(
    areas: list[dict[str, Any]],
    projects: list[dict[str, Any]],
    open_todos: list[dict[str, Any]],
    recent_done: list[dict[str, Any]],
    detailed_todos: list[dict[str, Any]],
    today: date,
    days_ahead: int,
    due_soon_days: int,
    top_projects_limit: int,
    top_areas_limit: int,
    max_suggestions: int,
    output_style: str,
    weights: Dict[str, float],
    open_count_cap: int,
) -> str:
    area_names = {str(a.get("id")): str(a.get("title") or "Unknown") for a in areas}
    project_names = {
        str(p.get("id")): str(p.get("title") or "Unknown Project") for p in projects
    }

    proj_activity: dict[str, Activity] = {}
    area_activity: dict[str, Activity] = {}
    open_by_project: dict[str, list[dict[str, Any]]] = defaultdict(list)

    overdue_count = 0
    due_soon_count = 0
    window_tasks: list[tuple[date, dict[str, Any]]] = []
    weekend_tasks = 0

    window_end = today + timedelta(days=days_ahead)

    for todo in open_todos:
        project_id = str(todo.get("project_id") or "")
        area_id = str(todo.get("area_id") or "")
        project_title = str(todo.get("project_title") or project_names.get(project_id) or "Unscoped")
        area_title = str(todo.get("area_title") or area_names.get(area_id) or "Unknown Area")

        due = parse_date(str(todo.get("deadline") or ""))
        if due is not None:
            if due < today:
                overdue_count += 1
            if due <= today + timedelta(days=due_soon_days):
                due_soon_count += 1
            if today <= due <= window_end:
                window_tasks.append((due, todo))
                if due.weekday() >= 5:
                    weekend_tasks += 1

        p_key = project_id or f"project:{project_title}"
        p_entry = inc_activity(proj_activity, p_key, project_title, area_title)
        p_entry.open_count += 1
        if due and due < today:
            p_entry.overdue += 1
        if due and due <= today + timedelta(days=due_soon_days):
            p_entry.due_soon += 1
        p_entry.checklist_hints += checklist_hint_score(str(todo.get("notes") or ""))

        a_key = area_id or f"area:{area_title}"
        a_entry = inc_activity(area_activity, a_key, area_title, area_title)
        a_entry.open_count += 1
        if due and due < today:
            a_entry.overdue += 1
        if due and due <= today + timedelta(days=due_soon_days):
            a_entry.due_soon += 1
        a_entry.checklist_hints += checklist_hint_score(str(todo.get("notes") or ""))

        open_by_project[p_key].append(todo)

    for todo in recent_done:
        project_id = str(todo.get("project_id") or "")
        area_id = str(todo.get("area_id") or "")
        project_title = str(todo.get("project_title") or project_names.get(project_id) or "Unscoped")
        area_title = str(todo.get("area_title") or area_names.get(area_id) or "Unknown Area")

        p_key = project_id or f"project:{project_title}"
        inc_activity(proj_activity, p_key, project_title, area_title).completed_7d += 1
        a_key = area_id or f"area:{area_title}"
        inc_activity(area_activity, a_key, area_title, area_title).completed_7d += 1

    for todo in detailed_todos:
        project_id = str(todo.get("project_id") or "")
        area_id = str(todo.get("area_id") or "")
        project_title = str(todo.get("project_title") or project_names.get(project_id) or "Unscoped")
        area_title = str(todo.get("area_title") or area_names.get(area_id) or "Unknown Area")
        hint = checklist_hint_score(str(todo.get("notes") or ""))
        if hint <= 0:
            continue
        p_key = project_id or f"project:{project_title}"
        inc_activity(proj_activity, p_key, project_title, area_title).checklist_hints += hint
        a_key = area_id or f"area:{area_title}"
        inc_activity(area_activity, a_key, area_title, area_title).checklist_hints += hint

    top_projects = sorted(
        proj_activity.items(),
        key=lambda row: activity_score(row[1], weights, open_count_cap),
        reverse=True,
    )[:top_projects_limit]
    top_areas = sorted(
        area_activity.items(),
        key=lambda row: activity_score(row[1], weights, open_count_cap),
        reverse=True,
    )[:top_areas_limit]
    window_tasks.sort(key=lambda row: row[0])

    lines: list[str] = []
    lines.append(f"# Things Planning Digest - {today.isoformat()}")
    lines.append("")

    if output_style == "executive":
        lines.append("## Executive Summary")
        lines.append(f"- Open todos: {len(open_todos)}")
        lines.append(f"- Immediate risk: {overdue_count} overdue, {due_soon_count} due soon")
        lines.append(
            f"- Top focus: {top_projects[0][1].title if top_projects else 'None currently'}"
        )
        lines.append("")

    lines.append("## Snapshot")
    lines.append(f"- Open todos: {len(open_todos)}")
    lines.append(f"- Overdue: {overdue_count}")
    lines.append(f"- Due in next {due_soon_days}d: {due_soon_count}")
    lines.append(f"- Recently completed (7d): {len(recent_done)}")
    most_active_area = top_areas[0][1].title if top_areas else "None currently"
    lines.append(f"- Most active area: {most_active_area}")
    lines.append("")
    lines.append("## Recently Active")
    lines.append("### Projects")
    if not top_projects:
        lines.append("1. None currently")
    else:
        for idx, (_, item) in enumerate(top_projects, start=1):
            area_suffix = f" ({item.area_title})" if item.area_title else ""
            lines.append(
                f"{idx}. {item.title}{area_suffix} - "
                f"open:{item.open_count}, due soon:{item.due_soon}, "
                f"overdue:{item.overdue}, completed 7d:{item.completed_7d}"
            )
    lines.append("")
    lines.append("### Areas")
    if not top_areas:
        lines.append("1. None currently")
    else:
        for idx, (_, item) in enumerate(top_areas, start=1):
            lines.append(
                f"{idx}. {item.title} - open:{item.open_count}, due soon:{item.due_soon}, "
                f"overdue:{item.overdue}, completed 7d:{item.completed_7d}"
            )
    lines.append("")
    lines.append("## Week/Weekend Ahead")
    if not window_tasks:
        lines.append("- None currently")
    else:
        for due, todo in window_tasks[:8]:
            weekday = due.strftime("%a")
            lines.append(f"- {weekday} {due.isoformat()}: {short_task(todo)}")
    lines.append("")
    lines.append("## Suggestions")

    suggestions: list[str] = []
    if overdue_count > 0:
        suggestions.append(
            f"Triage {overdue_count} overdue todo(s) first and reschedule or complete each one today."
        )

    for key, item in top_projects[:2]:
        candidates = sorted(
            open_by_project.get(key, []),
            key=lambda todo: parse_date(str(todo.get("deadline") or "")) or date.max,
        )
        if not candidates:
            continue
        task = candidates[0]
        task_title = str(task.get("title") or "a top task")
        suggestions.append(f"Start with '{task_title}' to move {item.title} forward today.")

    if weekend_tasks > 0:
        suggestions.append(
            "Block a weekend prep session for deadline-bound tasks due on Saturday or Sunday."
        )
    elif window_tasks:
        suggestions.append(
            f"Reserve a 30-minute planning pass for the next {days_ahead} days of deadlines."
        )

    checklist_total = sum(item.checklist_hints for _, item in top_projects)
    if checklist_total > 0:
        suggestions.append(
            "Split one checklist-heavy todo into smaller next actions to reduce context switching."
        )

    if not suggestions:
        suggestions.append("Pick one high-impact todo and complete it before adding new tasks.")

    for idx, suggestion in enumerate(suggestions[:max_suggestions], start=1):
        lines.append(f"{idx}. {suggestion}")

    return "\n".join(lines)


def main() -> int:
    args = parse_args()

    try:
        settings, active_config_path, config_source = resolve_settings(args.config)
    except Exception as exc:
        print(f"Failed to resolve configuration: {exc}", file=sys.stderr)
        return 2

    weights = normalize_weights(settings.get("scoringWeights"))

    try:
        due_soon_days = int(args.due_soon_days if args.due_soon_days is not None else settings.get("dueSoonDays", 3))
        days_ahead = int(args.days_ahead if args.days_ahead is not None else settings.get("daysAhead", 4))
        top_projects = int(args.top_projects if args.top_projects is not None else settings.get("topProjects", 3))
        top_areas = int(args.top_areas if args.top_areas is not None else settings.get("topAreas", 2))
        max_suggestions = int(
            args.max_suggestions if args.max_suggestions is not None else settings.get("maxSuggestions", 5)
        )
        open_count_cap = int(args.open_count_cap if args.open_count_cap is not None else settings.get("openCountCap", 10))
    except (TypeError, ValueError) as exc:
        print(f"Invalid numeric config value: {exc}", file=sys.stderr)
        return 2

    output_style = args.output_style if args.output_style is not None else str(settings.get("outputStyle", "operational"))
    if output_style not in {"operational", "executive"}:
        output_style = "operational"

    today = (
        date.fromisoformat(args.today)
        if args.today
        else datetime.now().astimezone().date()
    )

    areas = read_items(args.areas)
    projects = read_items(args.projects)
    open_todos = read_items(args.open_todos)
    recent_done = read_items(args.recent_done) if args.recent_done else []
    detailed_todos = read_items(args.detailed_todos) if args.detailed_todos else []

    digest = render_digest(
        areas=areas,
        projects=projects,
        open_todos=open_todos,
        recent_done=recent_done,
        detailed_todos=detailed_todos,
        today=today,
        days_ahead=days_ahead,
        due_soon_days=due_soon_days,
        top_projects_limit=max(1, top_projects),
        top_areas_limit=max(1, top_areas),
        max_suggestions=max(1, max_suggestions),
        output_style=output_style,
        weights=weights,
        open_count_cap=max(1, open_count_cap),
    )

    print(f"<!-- config_source: {config_source}; active_config_path: {active_config_path} -->")
    print(digest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
