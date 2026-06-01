from __future__ import annotations

from pathlib import Path

from agents import Agent, Runner, function_tool

from socket_steward.audit import run_audit
from socket_steward.plan import plan_docs_sync


PROMPT_PATH = Path(__file__).resolve().parents[2] / "docs" / "prompt.md"


@function_tool
def audit_socket_repo(audit_name: str, repo_root: str = ".") -> str:
    """Run a read-only Socket maintainer audit and return the report text."""
    return run_audit(Path(repo_root), audit_name).as_text()


@function_tool
def plan_socket_docs_sync(repo_root: str = ".") -> str:
    """Plan read-only Socket docs-sync work without applying file edits."""
    return plan_docs_sync(Path(repo_root)).as_text()


def build_agent() -> Agent[None]:
    return Agent(
        name="Socket Steward",
        instructions=PROMPT_PATH.read_text(encoding="utf-8"),
        tools=[audit_socket_repo, plan_socket_docs_sync],
    )


async def ask_socket_steward(question: str, repo_root: Path) -> str:
    prompt = (
        f"Repository root: {repo_root.resolve()}\n\n"
        f"Question:\n{question}\n\n"
        "Use audit_socket_repo or plan_socket_docs_sync when a deterministic Socket "
        "audit or planning pass would help."
    )
    result = await Runner.run(build_agent(), prompt)
    return str(result.final_output)
