import os
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Settings:
    victorialogs_url: str
    victoriatraces_url: str

def resolve_settings() -> Settings:
    logs_url = os.environ.get("NANOBOT_VICTORIALOGS_URL", "").strip()
    if not logs_url:
        raise RuntimeError("NANOBOT_VICTORIALOGS_URL not set")
    traces_url = os.environ.get("NANOBOT_VICTORIATRACES_URL", "").strip()
    if not traces_url:
        raise RuntimeError("NANOBOT_VICTORIATRACES_URL not set")
    return Settings(victorialogs_url=logs_url, victoriatraces_url=traces_url)
