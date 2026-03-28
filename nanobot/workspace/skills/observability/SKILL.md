---
name: observability
description: Use observability MCP tools for logs and traces
always: true
---

# Observability Skill

You have access to observability tools for querying structured logs and distributed traces.

## Available Tools

- **logs_search** — Search structured logs using LogsQL. Key fields: `_time`, `service.name`, `severity`, `event`, `trace_id`.
- **logs_error_count** — Count log entries matching a LogsQL query.
- **traces_list** — List recent traces for a service.
- **traces_get** — Fetch a specific trace by trace ID.

## Investigation Strategy

When the user asks "What went wrong?", "Check system health", or about errors:

1. First use `logs_error_count` with query `_time:5m service.name:"Learning Management Service" severity:ERROR` to check if there are recent errors.
2. If errors exist, use `logs_search` with the same query to get error details and extract `trace_id` values.
3. If you find a `trace_id` in the log entries, use `traces_get` to fetch the full trace for deeper analysis.
4. Summarize findings concisely:
   - How many errors occurred
   - What type of error (DB connection, timeout, etc.)
   - Which service and operation failed
   - What the trace reveals about the request flow
   - Note any discrepancies (e.g., if logs show a DB error but the HTTP response was 404 instead of 500)
   - Suggest what might be wrong

## Important Notes

- The main backend service is called "Learning Management Service".
- Use narrow time windows (e.g. `_time:5m` or `_time:2m`) unless the user specifies otherwise.
- Never dump raw JSON to the user — always summarize.
- Pay attention to mismatches between the real error cause and the HTTP status code returned.
