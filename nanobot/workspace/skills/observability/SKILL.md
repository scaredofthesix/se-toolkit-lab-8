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

## Strategy

- When the user asks about errors, first use `logs_error_count` with a query like `_time:10m service.name:"Learning Management Service" severity:ERROR` to check if there are any.
- If errors exist, use `logs_search` to get the details.
- If you find a `trace_id` in the log entries, use `traces_get` to fetch the full trace for deeper analysis.
- Summarize findings concisely — don't dump raw JSON to the user.
- Report: how many errors, what type, which service, and suggest what might be wrong.
- The main backend service is called "Learning Management Service".
- Use narrow time windows (e.g. `_time:10m`) unless the user specifies otherwise.
