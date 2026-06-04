# Eval Surface Selection

Use this reference when choosing where agent, skill, prompt, or automation evals
should live.

## Official Sources

- Codex non-interactive mode: <https://developers.openai.com/codex/noninteractive>
- Codex GitHub Action: <https://developers.openai.com/codex/github-action>
- Codex app automations: <https://developers.openai.com/codex/app/automations>
- OpenAI Agents SDK: <https://developers.openai.com/api/docs/guides/agents>
- OpenAI Evals: <https://developers.openai.com/api/docs/guides/evals>
- LangGraph: <https://docs.langchain.com/oss/python/langgraph/overview>
- LangSmith evaluation: <https://docs.smith.langchain.com/evaluation>

## Surface Matrix

| Surface | Use first when | Avoid first when |
| --- | --- | --- |
| Local script or pytest | The eval can assert files, commands, schemas, prompts, or deterministic outputs inside one repo. | The behavior requires live agent traces, hosted tools, or cross-run service state. |
| `codex exec` or Codex GitHub Action | The eval should run a real Codex prompt against a repository with explicit sandbox and output expectations. | The task needs interactive review inside the same run or custom service state. |
| Codex app automation | The eval is a recurring inbox/check-in task where Codex is the user-facing surface. | The eval needs deterministic CI gating or service-owned trace storage. |
| OpenAI Agents SDK eval/tracing | Application code owns tools, handoffs, guardrails, state, or traces. | A local deterministic test can prove the behavior with less moving runtime. |
| LangGraph or LangSmith eval | The workflow is graph-shaped and needs transition, persistence, resume, or graph-run observability. | The workflow is a simple skill, prompt, or one-shot repo task. |
| Stack-owned runner | A narrower plugin already owns the framework, language, simulator, browser, or package test path. | The task is framework-neutral eval planning. |

## Full-Auto Fit Checks

A workflow can be recommended for full automation when all of these are true:

- inputs are bounded or normalized before execution
- write scope is explicit and narrow
- validation is deterministic or reviewable enough to catch material failures
- secrets and private data are excluded or mocked
- failures leave a durable report
- retries are bounded
- rollback, no-op, or draft behavior prevents irreversible damage
- external side effects are absent or explicitly approved in advance

If any check fails, prefer `auto-with-escalation` and name the exact missing
gate instead of falling back to broad human review.
