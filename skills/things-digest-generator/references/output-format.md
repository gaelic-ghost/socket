# Digest Output Format

Use this output order.

```markdown
# Things Planning Digest - YYYY-MM-DD

## Executive Summary
- Open todos: <count>
- Immediate risk: <overdue count> overdue, <due-soon count> due soon
- Top focus: <project or None currently>

## Snapshot
- Open todos: <count>
- Overdue: <count>
- Due in next <dueSoonDays>d: <count>
- Recently completed (7d): <count>
- Most active area: <area>

## Recently Active
### Projects
1. <Project> (<Area>) - open:<n>, due soon:<n>, overdue:<n>, completed 7d:<n>
2. <Project> ...
3. <Project> ...

### Areas
1. <Area> - open:<n>, due soon:<n>, overdue:<n>, completed 7d:<n>
2. <Area> ...

## Week/Weekend Ahead
- <Day YYYY-MM-DD>: <task title> (<project/area>)
- <Day YYYY-MM-DD>: ...

## Suggestions
1. <Specific next action with task/project names>
2. <Risk reduction action for overdue or near-due work>
3. <Week/weekend planning action>
```

Formatting rules:
- Include `## Executive Summary` only when `outputStyle=executive`.
- Keep the full digest under ~220 words unless the user asks for detail.
- Use exact task/project names from Things data.
- If a section has no data, write `None currently` instead of omitting the section.
- If there are no open todos and no recent completed todos in scope, output exactly `No findings.`
- Do not prepend an out-of-band metadata comment before the markdown output.

Failure format:
- If required or provided JSON inputs cannot be used, stop with one stderr line that begins `Input error:`.
- Use these exact categories in the error text:
  - `missing required input file`
  - `missing provided input file`
  - `unreadable input path`
  - `invalid JSON`
  - `unsupported JSON shape`
