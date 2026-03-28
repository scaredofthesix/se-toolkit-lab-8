"""MCP server exposing observability tools."""
from __future__ import annotations
import asyncio
import json
from typing import Any
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool
from pydantic import BaseModel, Field
from mcp_obs.client import ObsClient
from mcp_obs.settings import resolve_settings


class LogsSearchArgs(BaseModel):
    query: str = Field(description="LogsQL query, e.g. '_time:10m service.name:\"Learning Management Service\" severity:ERROR'")
    limit: int = Field(default=20, ge=1, description="Max log entries to return")

class LogsErrorCountArgs(BaseModel):
    query: str = Field(description="LogsQL query to count matching error entries")

class TracesListArgs(BaseModel):
    service: str = Field(description="Service name, e.g. 'Learning Management Service'")
    limit: int = Field(default=10, ge=1, description="Max traces to return")

class TracesGetArgs(BaseModel):
    trace_id: str = Field(description="Trace ID to fetch")


def create_server(client: ObsClient) -> Server:
    server = Server("obs")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            Tool(
                name="logs_search",
                description="Search structured logs using LogsQL. Use fields like _time, service.name, severity, event, trace_id. Example: '_time:10m service.name:\"Learning Management Service\" severity:ERROR'",
                inputSchema=LogsSearchArgs.model_json_schema(),
            ),
            Tool(
                name="logs_error_count",
                description="Count log entries matching a LogsQL query. Useful to quickly check how many errors occurred.",
                inputSchema=LogsErrorCountArgs.model_json_schema(),
            ),
            Tool(
                name="traces_list",
                description="List recent traces for a service from VictoriaTraces.",
                inputSchema=TracesListArgs.model_json_schema(),
            ),
            Tool(
                name="traces_get",
                description="Fetch a specific trace by its trace ID from VictoriaTraces.",
                inputSchema=TracesGetArgs.model_json_schema(),
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict[str, Any] | None) -> list[TextContent]:
        args = arguments or {}
        try:
            if name == "logs_search":
                parsed = LogsSearchArgs.model_validate(args)
                results = await client.logs_search(parsed.query, parsed.limit)
                return [TextContent(type="text", text=json.dumps(results[:parsed.limit], ensure_ascii=False, default=str))]
            elif name == "logs_error_count":
                parsed = LogsErrorCountArgs.model_validate(args)
                count = await client.logs_error_count(parsed.query)
                return [TextContent(type="text", text=json.dumps({"count": count}))]
            elif name == "traces_list":
                parsed = TracesListArgs.model_validate(args)
                data = await client.traces_list(parsed.service, parsed.limit)
                return [TextContent(type="text", text=json.dumps(data, ensure_ascii=False, default=str))]
            elif name == "traces_get":
                parsed = TracesGetArgs.model_validate(args)
                data = await client.traces_get(parsed.trace_id)
                return [TextContent(type="text", text=json.dumps(data, ensure_ascii=False, default=str))]
            else:
                return [TextContent(type="text", text=f"Unknown tool: {name}")]
        except Exception as exc:
            return [TextContent(type="text", text=f"Error: {type(exc).__name__}: {exc}")]

    _ = list_tools, call_tool
    return server


async def main() -> None:
    settings = resolve_settings()
    async with ObsClient(settings.victorialogs_url, settings.victoriatraces_url) as client:
        server = create_server(client)
        async with stdio_server() as (read_stream, write_stream):
            await server.run(read_stream, write_stream, server.create_initialization_options())
