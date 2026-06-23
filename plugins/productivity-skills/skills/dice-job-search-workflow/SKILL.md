---
name: dice-job-search-workflow
description: Search and triage technology jobs through Dice's remote MCP server. Use when the user wants Dice.com job search help, MCP setup guidance, role-fit triage, resume-to-listing comparison, saved search prompt design, salary or skills trend checks, or recurring job-search automation boundaries grounded in Dice's documented search_jobs tool.
---

# Dice Job Search Workflow

Use Dice's remote MCP server as a read-only job-search data source for technology roles.

This skill helps the agent turn a job-search goal into bounded Dice MCP searches,
compare returned jobs against the user's stated preferences, and produce useful
next actions without taking over the application or profile lifecycle.

## Inputs

- Required: the role target, search question, or job-search goal
- Useful: location, remote/hybrid/on-site preference, employment type, recency,
  visa sponsorship needs, salary expectations, dealbreakers, target stack,
  resume or profile excerpt, and maximum number of roles to review
- Optional: existing Dice profile state, saved searches, application tracker,
  preferred resume variant, and whether recurring search automation is desired

## Source

Dice documents a remote MCP endpoint at `https://mcp.dice.com/mcp` with a
read-only `search_jobs` tool. No Dice login is required for basic public job
search. Treat this as an external live data source whose listings, filters, and
client setup details may change.

Official sources:

- Dice MCP technical documentation: https://www.dice.com/about/mcp
- Dice MCP setup guide: https://www.dice.com/career-advice/how-to-connect-the-dice-mcp-server-to-your-ai-assistant
- Dice launch article: https://www.dice.com/career-advice/dice-launches-mcp-server-for-ai-powered-job-search

## Workflow

1. Clarify the search goal in practical terms: target role, geography, work
   mode, seniority, technologies, employment type, recency, and hard filters.
2. Verify whether a Dice MCP tool is available in the active session.
   - If available, use it directly for read-only search.
   - If unavailable, give setup or handoff guidance using the official endpoint
     and do not invent local server code.
3. Prefer broad first searches, then narrow with filters after seeing the
   shape of results. Avoid overfitting the first query to every preference.
4. Use Dice's documented parameters when constructing searches:
   - `keyword`: required job title or search keywords
   - `location`: city, state, region, or remote-oriented search term
   - `radius` and `radius_unit`: location expansion
   - `workplace_types`: `Remote`, `On-Site`, or `Hybrid`
   - `employment_types`: `FULLTIME`, `CONTRACTS`, `PARTTIME`, or `THIRD_PARTY`
   - `employer_types`: `Direct Hire`, `Recruiter`, or `Other`
   - `posted_date`: `ONE`, `THREE`, or `SEVEN`
   - `willing_to_sponsor`: work authorization sponsorship filter
   - `easy_apply`: simplified application filter
   - `jobs_per_page`, `page_number`, and `fields`: pagination and response size
5. Review results for role fit before recommending action. Separate:
   - strong matches worth applying to
   - possible matches worth a resume variant or follow-up search
   - poor matches blocked by hard constraints
   - ambiguous matches needing the full job page, current company info, or user
     decision
6. When comparing against a resume, keep the output evidence-heavy:
   - match required skills to resume proof
   - name missing or weak proof
   - suggest concrete resume edits only when grounded in real experience
   - avoid keyword stuffing, invented experience, and broad ATS filler
7. For recurring searches or digests, design the search prompt and cadence first.
   Require explicit user approval before creating automations, notifications,
   application trackers, or any write surface outside the current answer.
8. If the user wants to apply, keep the boundary clear: prepare materials,
   summarize risks, and ask before submitting, changing profile data, or sending
   messages.

## Search Patterns

Use these as starting shapes, not canned final answers:

- Broad discovery: `keyword`, optional `location`, `jobs_per_page: 25`
- Recent remote search: `keyword`, `workplace_types: ["Remote"]`,
  `posted_date: "THREE"`
- Local hybrid search: `keyword`, `location`, `radius`, `radius_unit: "mi"`,
  `workplace_types: ["Hybrid"]`
- Sponsorship search: `keyword`, `willing_to_sponsor: true`, plus broad
  location or remote filters
- Recruiter-light search: search normally, then classify employer type and
  recruiter involvement from the returned fields when available
- Skills trend check: run a small set of comparable searches, sample results,
  and summarize repeated technologies without claiming full-market statistics

## Output Contract

For job triage, return:

- `Answer`: the direct recommendation or shortlist
- `Meaning`: why the roles or search shape fit the user's goals
- `Risk`: hard blockers, stale/live-data uncertainty, and decisions needed
- `Evidence`: search parameters, result counts, listing names, dates, and links
- `Next Search`: one focused follow-up query when useful

For setup guidance, return:

- `Answer`: whether Dice MCP is currently usable in this environment
- `Meaning`: what the endpoint/tool enables
- `Risk`: authentication, subscription, client, rate-limit, and privacy caveats
- `Details`: client-specific setup steps and verification prompt

## Guardrails

- Do not apply to jobs, send messages, alter a Dice profile, upload resumes, or
  create saved searches unless the user explicitly asks for that exact action.
- Do not claim a role is current, remote, sponsor-friendly, or easy-apply unless
  that field is present in live Dice results or the visible listing evidence.
- Do not infer salary, sponsorship, employer type, or remote status from vague
  wording when the result does not expose it.
- Do not promise that Dice MCP stores no data beyond what the official docs say.
  State only that the documented server exposes public job listings and basic
  search does not require a Dice login.
- Do not scrape Dice web pages when the MCP tool is available and sufficient.
- Do not build a local MCP server, proxy, cache, or automation runner inside this
  skill. This skill is guidance around Dice's external MCP surface.
- Respect rate limits. If HTTP 429 or throttling appears, stop, back off, and
  report the limit instead of retrying aggressively.
- Keep personal job-search preferences, resumes, and application history out of
  logs and durable repo files unless the user explicitly asks to save them.

## References

- `agents/openai.yaml`
- `references/dice-mcp-source-notes.md`
