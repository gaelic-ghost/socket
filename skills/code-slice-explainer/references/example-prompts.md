# Example Prompts

## Single-slice walkthrough

```text
Use $code-slice-explainer to explain the slice for saving a new reminder. Start with the incoming data shape and who creates it, then walk every meaningful step through validation, storage, and final UI update. Use standard detail.
```

## Quick orientation

```text
Explain this slice at quick detail: how does the login request move through this codebase from the initial trigger to the final response?
```

## Natural phrasing

```text
Walk me through this from start to finish.
```

```text
Follow this value through the code and tell me where it comes from, where it changes shape, and where it ends up.
```

```text
What calls this, what does it call next, and why is the data shaped like that?
```

## Thorough walkthrough

```text
Walk me through this slice in thorough detail. I want the data shape first, then the full execution flow with every boundary, branch point, and transformation explained, plus a simple diagram with notes.
```

## Debugging-oriented slice

```text
Use $code-slice-explainer to explain the file-upload slice with a debugging focus. Show the exact path the data takes, where shape changes happen, and where I should inspect if the final URL is wrong.
```

## Compare two slices

```text
Compare these two slices at standard detail: the old checkout flow and the new checkout flow. Explain each path clearly, then compare where their triggers, transformations, boundaries, and outputs differ.
```

```text
Show me what changed between the old flow and the new one, step by step.
```

```text
Compare how these two code paths move data from input to output.
```
