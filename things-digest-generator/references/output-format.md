# Digest Output Format

Use this exact section order.

```markdown
# Things Planning Digest - YYYY-MM-DD

## Snapshot
- Open todos: <count>
- Overdue: <count>
- Due in next 72h: <count>
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
- Keep the full digest under ~220 words unless the user asks for detail.
- Use exact task/project names from Things data.
- If a section has no data, write `None currently` instead of omitting the section.
