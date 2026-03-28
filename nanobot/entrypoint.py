"""Resolve Docker env vars into nanobot config, then exec the gateway."""
import json
import os


CONFIG_PATH = "/app/nanobot/config.json"
RESOLVED_PATH = "/app/nanobot/config.resolved.json"
WORKSPACE = "/app/nanobot/workspace"


def main():
    with open(CONFIG_PATH) as f:
        config = json.load(f)

    # --- Provider (LLM) ---
    provider_key = os.environ.get("LLM_API_KEY", "")
    provider_base = os.environ.get("LLM_API_BASE_URL", "")
    provider_model = os.environ.get("LLM_API_MODEL", "")

    if provider_key:
        config.setdefault("providers", {}).setdefault("custom", {})
        config["providers"]["custom"]["apiKey"] = provider_key
    if provider_base:
        config.setdefault("providers", {}).setdefault("custom", {})
        config["providers"]["custom"]["apiBase"] = provider_base
    if provider_model:
        config.setdefault("agents", {}).setdefault("defaults", {})
        config["agents"]["defaults"]["model"] = provider_model
        config["agents"]["defaults"]["provider"] = "custom"

    # --- Gateway ---
    gw_host = os.environ.get("NANOBOT_GATEWAY_CONTAINER_ADDRESS", "0.0.0.0")
    gw_port = os.environ.get("NANOBOT_GATEWAY_CONTAINER_PORT", "18790")
    config.setdefault("gateway", {})
    config["gateway"]["host"] = gw_host
    config["gateway"]["port"] = int(gw_port)

    # --- MCP: LMS ---
    lms_url = os.environ.get("NANOBOT_LMS_BACKEND_URL", "")
    lms_key = os.environ.get("NANOBOT_LMS_API_KEY", "")
    if lms_url:
        config.setdefault("tools", {}).setdefault("mcpServers", {})
        config["tools"]["mcpServers"]["lms"] = {
            "command": "python",
            "args": ["-m", "mcp_lms"],
            "env": {
                "NANOBOT_LMS_BACKEND_URL": lms_url,
                "NANOBOT_LMS_API_KEY": lms_key,
            },
        }

    # --- Webchat channel ---
    wc_host = os.environ.get("NANOBOT_WEBCHAT_CONTAINER_ADDRESS", "")
    wc_port = os.environ.get("NANOBOT_WEBCHAT_CONTAINER_PORT", "8765")
    access_key = os.environ.get("NANOBOT_ACCESS_KEY", "")
    if wc_host:
        config.setdefault("channels", {})
        config["channels"]["webchat"] = {
            "enabled": True,
            "host": wc_host,
            "port": int(wc_port),
            "accessKey": access_key,
            "allowFrom": ["*"],
        }

        # --- MCP: webchat UI ---
        config.setdefault("tools", {}).setdefault("mcpServers", {})
        config["tools"]["mcpServers"]["webchat"] = {
            "command": "python",
            "args": ["-m", "mcp_webchat"],
            "env": {
                "MCP_WEBCHAT_RELAY_URL": f"ws://{wc_host}:{wc_port}",
                "MCP_WEBCHAT_RELAY_TOKEN": access_key,
            },
        }

    # --- Workspace ---
    config.setdefault("agents", {}).setdefault("defaults", {})
    config["agents"]["defaults"]["workspace"] = WORKSPACE

    with open(RESOLVED_PATH, "w") as f:
        json.dump(config, f, indent=2)

    print(f"Using config: {RESOLVED_PATH}", flush=True)
    os.execvp("nanobot", ["nanobot", "gateway", "--config", RESOLVED_PATH, "--workspace", WORKSPACE])


if __name__ == "__main__":
    main()
