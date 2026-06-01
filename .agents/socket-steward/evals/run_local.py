from __future__ import annotations

import asyncio
import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from socket_steward.agent import ask_socket_steward


EVAL_ROOT = Path(__file__).resolve().parent
APP_ROOT = EVAL_ROOT.parent
REPO_ROOT = APP_ROOT.parents[1]
CASES_PATH = EVAL_ROOT / "cases.jsonl"
RESULTS_PATH = EVAL_ROOT / "results" / "latest.json"


@dataclass(frozen=True)
class EvalCase:
    case_id: str
    prompt: str
    required: tuple[str, ...]
    required_any: tuple[tuple[str, ...], ...]
    forbidden: tuple[str, ...]


@dataclass(frozen=True)
class EvalResult:
    case_id: str
    passed: bool
    missing_required: tuple[str, ...]
    missing_required_any: tuple[tuple[str, ...], ...]
    present_forbidden: tuple[str, ...]
    output: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "case_id": self.case_id,
            "passed": self.passed,
            "missing_required": list(self.missing_required),
            "missing_required_any": [list(group) for group in self.missing_required_any],
            "present_forbidden": list(self.present_forbidden),
            "output": self.output,
        }


def load_cases(path: Path) -> tuple[EvalCase, ...]:
    cases: list[EvalCase] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        raw = json.loads(line)
        cases.append(
            EvalCase(
                case_id=str(raw["id"]),
                prompt=str(raw["prompt"]),
                required=tuple(str(item) for item in raw.get("required", [])),
                required_any=tuple(
                    tuple(str(item) for item in group) for group in raw.get("required_any", [])
                ),
                forbidden=tuple(str(item) for item in raw.get("forbidden", [])),
            )
        )
        if not cases[-1].prompt:
            raise ValueError(f"Eval case on line {line_number} is missing a prompt.")
    return tuple(cases)


def grade(case: EvalCase, output: str) -> EvalResult:
    haystack = output.lower()
    missing_required = tuple(item for item in case.required if item.lower() not in haystack)
    missing_required_any = tuple(
        group for group in case.required_any if not any(item.lower() in haystack for item in group)
    )
    present_forbidden = tuple(item for item in case.forbidden if item.lower() in haystack)
    return EvalResult(
        case_id=case.case_id,
        passed=not missing_required and not missing_required_any and not present_forbidden,
        missing_required=missing_required,
        missing_required_any=missing_required_any,
        present_forbidden=present_forbidden,
        output=output,
    )


async def run_case(case: EvalCase) -> EvalResult:
    output = await ask_socket_steward(case.prompt, REPO_ROOT)
    return grade(case, output)


async def run_all() -> tuple[EvalResult, ...]:
    return tuple([await run_case(case) for case in load_cases(CASES_PATH)])


def main() -> int:
    if not os.environ.get("OPENAI_API_KEY"):
        print("OPENAI_API_KEY is required for Socket Steward local evals.", file=sys.stderr)
        return 2

    results = asyncio.run(run_all())
    payload = {
        "passed": all(result.passed for result in results),
        "results": [result.to_dict() for result in results],
    }
    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULTS_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    for result in results:
        status = "PASS" if result.passed else "FAIL"
        print(f"{status} {result.case_id}")
        if result.missing_required:
            print(f"  missing required: {', '.join(result.missing_required)}")
        for group in result.missing_required_any:
            print(f"  missing required-any: one of {', '.join(group)}")
        if result.present_forbidden:
            print(f"  present forbidden: {', '.join(result.present_forbidden)}")

    return 0 if payload["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
