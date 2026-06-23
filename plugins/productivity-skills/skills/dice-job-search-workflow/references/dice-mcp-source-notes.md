# Dice MCP Source Notes

Use this reference when maintaining `dice-job-search-workflow`.

## Official Surfaces

- Technical documentation: https://www.dice.com/about/mcp
- Setup guide: https://www.dice.com/career-advice/how-to-connect-the-dice-mcp-server-to-your-ai-assistant
- Launch article: https://www.dice.com/career-advice/dice-launches-mcp-server-for-ai-powered-job-search

## Endpoint

Dice documents the production endpoint as:

```text
https://mcp.dice.com/mcp
```

The docs say no authentication is required for basic public job-search usage.

## Tool

The documented MCP tool is `search_jobs`.

Required parameter:

- `keyword`: job title or search keywords

Optional parameters documented by Dice:

- `location`
- `radius`
- `radius_unit`
- `jobs_per_page`
- `page_number`
- `posted_date`
- `workplace_types`
- `employment_types`
- `employer_types`
- `willing_to_sponsor`
- `easy_apply`
- `fields`

## Boundaries

The first Socket-owned skill should stay guidance-only around Dice's external
MCP server. It should not bundle a local Dice MCP server, proxy, scraper, cache,
or automation runner.

Treat Dice result data as live and mutable. Search outputs should cite the
search parameters and result evidence that were actually reviewed.
