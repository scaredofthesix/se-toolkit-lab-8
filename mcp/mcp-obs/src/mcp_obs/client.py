"""HTTP client for VictoriaLogs and VictoriaTraces."""
from __future__ import annotations
import httpx
from typing import Any


class ObsClient:
    def __init__(self, victorialogs_url: str, victoriatraces_url: str) -> None:
        self.logs_url = victorialogs_url.rstrip("/")
        self.traces_url = victoriatraces_url.rstrip("/")
        self._http = httpx.AsyncClient(timeout=15.0)

    async def aclose(self) -> None:
        await self._http.aclose()

    async def __aenter__(self) -> "ObsClient":
        return self

    async def __aexit__(self, *_: object) -> None:
        await self.aclose()

    async def logs_search(self, query: str, limit: int = 20) -> list[dict[str, Any]]:
        resp = await self._http.get(
            f"{self.logs_url}/select/logsql/query",
            params={"query": query, "limit": str(limit)},
        )
        resp.raise_for_status()
        lines = resp.text.strip().split("\n")
        import json
        results = []
        for line in lines:
            if line.strip():
                try:
                    results.append(json.loads(line))
                except Exception:
                    results.append({"raw": line})
        return results

    async def logs_error_count(self, query: str) -> int:
        results = await self.logs_search(query, limit=1000)
        return len(results)

    async def traces_list(self, service: str, limit: int = 10) -> dict[str, Any]:
        resp = await self._http.get(
            f"{self.traces_url}/select/jaeger/api/traces",
            params={"service": service, "limit": str(limit)},
        )
        resp.raise_for_status()
        return resp.json()

    async def traces_get(self, trace_id: str) -> dict[str, Any]:
        resp = await self._http.get(
            f"{self.traces_url}/select/jaeger/api/traces/{trace_id}",
        )
        resp.raise_for_status()
        return resp.json()
