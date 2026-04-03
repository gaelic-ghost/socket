# Diagram Format

Use a simple flat flow that matches execution order.

Example shape:

```text
1. UI handler receives form payload [D1]
2. Action adapter normalizes request body [D2]
3. Service validates command [B1]
4. Repository writes record
5. Presenter returns response DTO [D3]
6. Caller updates UI
```

Marker rules:

- `B#` for branch points
- `D#` for data-shape changes

Keep markers inline and minimal. Explain them in `Notes`.

## Notes style

Example:

```text
B1: If validation fails, the slice exits early with an error response instead of continuing to the repository step.
D2: The raw form payload is converted into the service command shape so validation and domain logic can work with normalized names and types.
```

## Diagram constraints

- Use the same order as the narrative walkthrough.
- Do not turn the diagram into a large graph unless the user explicitly asks for a more complex one.
- If there are multiple branches, keep the mainline readable and push branch detail into notes.
