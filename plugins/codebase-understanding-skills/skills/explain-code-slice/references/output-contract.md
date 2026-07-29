# Output Contract

Use this response structure in order.

## 1. Slice summary

State:

- what this slice is
- what triggers it
- who sends or constructs the initial input
- what the incoming data shape represents
- why that data enters the slice

Keep this short but concrete.

## 2. Walkthrough

Write a conversational step-by-step walkthrough in execution order.

For each meaningful step, cover:

- the file, function, or subsystem when known
- what the step is doing
- whether it is shared or specialized
- whether it crosses a boundary
- whether it is a branch point
- whether the data shape changes there
- why that step exists

If the same function is revisited through a branch, describe that explicitly rather than flattening it away.

## 3. Diagram

Include a compact execution-flow diagram with numbered steps. Use inline markers to flag:

- branch points
- data-shape changes

Keep the diagram simple enough to skim quickly.

## 4. Notes

Add short footnotes keyed to the markers from the diagram.

Use notes for:

- branch explanations
- data-shape change explanations
- boundary meaning
- alternate path clarification

Do not move the main story into the notes. The notes are for uncluttering, not for hiding core behavior.
