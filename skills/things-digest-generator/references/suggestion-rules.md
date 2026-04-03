# Scoring And Suggestions

Use these rules unless the user asks for a different weighting model.

## Activity scoring

Compute per project and per area:
- `open_count`
- `due_soon_count` (`deadline <= today + 3d`)
- `overdue_count`
- `completed_7d_count`
- `checklist_hint_count` (notes contain markdown checkbox patterns or long bullet lists)

Default score:

`score = completed_7d_count*3 + due_soon_count*2 + overdue_count*3 + min(open_count, 10)*0.5 + checklist_hint_count*1.5`

Sort descending by score. Use top 3 projects and top 2 areas in the digest.

## Suggestion rules

Generate 3-5 suggestions in this order:
1. Overdue triage: if overdue items exist, recommend a same-day triage action.
2. Top project next action: pick one concrete todo title from the highest-scoring project.
3. Second top project next action: include if available.
4. Weekend/Monday prep: if Saturday/Sunday/Monday deadlines exist in the window, recommend prep.
5. Checklist-heavy simplification: if checklist hints are common, suggest splitting one large task.

Style constraints:
- Make each suggestion one sentence.
- Start with an imperative verb.
- Include a concrete task or project name.
