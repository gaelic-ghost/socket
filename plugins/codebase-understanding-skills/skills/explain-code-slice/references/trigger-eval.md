# Trigger Evaluation Prompts

Use this file to audit whether the frontmatter description is wide enough to catch Gale-style natural phrasing, not just explicit domain labels.

## Should trigger

- `Walk me through this code path from start to finish.`
- `How does this part work?`
- `Follow this value through the system.`
- `Show me the path this request takes.`
- `Where does this data come from?`
- `Where does it go after this?`
- `What calls this?`
- `What does this call next?`
- `Why is this object shaped like that?`
- `Explain the flow end to end.`
- `Trace this from input to output.`
- `Show me the request lifecycle.`
- `I want the pipeline explained step by step.`
- `Cmd-click this with me from start to finish.`
- `Compare the old flow and the new flow.`
- `What changed between these two code paths?`
- `Compare how these two implementations move data through the system.`
- `Walk me through this shit step by step and show me where the data changes shape.`
- `I need to understand who sends this data, why it looks like this, and where it ends up.`
- `Explain what happens after this function gets called and who receives the return value.`

## Should not trigger

- `Refactor this code.`
- `Write a new API endpoint.`
- `Summarize this file at a high level.`
- `Review this PR for bugs.`
- `Find dead code in this module.`
- `Rename these variables for clarity.`
- `Add tests for this service.`
- `Optimize this query.`
- `Fix this type error.`
- `Generate docs for this package.`

## Audit guidance

- Favor should-trigger coverage over narrowness for this skill.
- Include casual, terse, typo-prone, and frustrated phrasings when evaluating trigger breadth.
- Treat comparison prompts as required trigger cases, not optional stretch cases.
- If a natural phrasing feels like Gale would plausibly use it for a slice explanation, it belongs in the should-trigger set.
