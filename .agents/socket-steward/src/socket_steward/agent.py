from __future__ import annotations

from pathlib import Path

from agents import Agent, Runner, function_tool

from socket_steward.audit import run_audit


PROMPT_PATH = Path(__file__).resolve().parents[2] / "docs" / "prompt.md"


@function_tool
def audit_socket_repo(audit_name: str, repo_root: str = ".") -> str:
    """Run a read-only Socket maintainer audit and return the report text."""
    return run_audit(Path(repo_root), audit_name).as_text()


def build_agent() -> Agent[None]:
    return Agent(
        name="Socket Steward",
        instructions=PROMPT_PATH.read_text(encoding="utf-8"),
        tools=[audit_socket_repo],
    )


async def ask_socket_steward(question: str, repo_root: Path) -> str:
    prompt = (
        f"Repository root: {repo_root.resolve()}\n\n"
        f"Question:\n{question}\n\n"
        "Use audit_socket_repo when a deterministic Socket audit would help."
    )
    result = await Runner.run(build_agent(), prompt)
    return str(result.final_output)
