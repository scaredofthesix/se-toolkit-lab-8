# Lab 8 — Task 1 Report

## Task 1A — Bare agent

### Q: "What is the agentic loop?"

The "agentic loop" refers to the iterative process an AI agent uses to achieve a goal. It typically involves these steps:
1. Observation: The agent perceives its environment.
2. Planning: The agent formulates a plan to achieve its goal based on its observations and knowledge.
3. Action: The agent executes a step from its plan by using available tools or skills.
4. Reflection: The agent evaluates the outcome of its action and updates its plan or knowledge accordingly.

This loop repeats until the agent achieves its goal or determines it's unachievable.

### Q: "What labs are available in our LMS?"

I do not have access to your LMS to check which labs are available. I can only access files and tools available to me. Is there a file I can read or a tool I can use to find this information?

## Task 1B — Agent with LMS tools

### Q: "What labs are available?"

Here are the available labs: Lab 01 – Products, Architecture & Roles, Lab 02 — Run, Fix, and Deploy a Backend Service, Lab 03 — Backend API: Explore, Debug, Implement, Deploy, Lab 04 — Testing, Front-end, and AI Agents, Lab 05 — Data Pipeline and Analytics Dashboard, Lab 06 — Build Your Own Agent, Lab 07 — Build a Client with an AI Coding Agent, and lab-08.

### Q: "Is the LMS backend healthy?"

Yes, the LMS backend is healthy! It currently has 56 items in the database.

## Task 1C — Skill prompt

### Q: "Show me the scores"

I found 8 labs available. Which lab's scores would you like to see?
1. Lab 01 – Products, Architecture & Roles
2. Lab 02 — Run, Fix, and Deploy a Backend Service
3. Lab 03 — Backend API: Explore, Debug, Implement, Deploy
4. Lab 04 — Testing, Front-end, and AI Agents
5. Lab 05 — Data Pipeline and Analytics Dashboard
6. Lab 06 — Build Your Own Agent
7. Lab 07 — Build a Client with an AI Coding Agent
8. lab-08

Please let me know which lab you'd like to see the pass rates and scores for, or I can show you all of them if you prefer.

## Task 2A — Deployed agent

Startup log excerpt:
```
Using config: /app/nanobot/config.resolved.json
Starting nanobot gateway version 0.1.4.post5 on port 18790...
WebChat channel enabled
Channels enabled: webchat
Heartbeat: every 1800s
Cron service started with 0 jobs
Heartbeat started (every 1800s)
```

## Task 2B — Web client

WebSocket test response:
```
{"type":"text","content":"I'll check what labs are available in the LMS.","format":"markdown"}
```

Flutter client accessible at http://10.93.24.236:42002/flutter

(Screenshot to be added)

## Task 3A — Structured logging

### Happy-path log excerpt
```
request_started [trace_id=4c89ad1d902b99f4aa13b8b8e2cc362a] 
auth_success [trace_id=4c89ad1d902b99f4aa13b8b8e2cc362a]
db_query [trace_id=4c89ad1d902b99f4aa13b8b8e2cc362a]
request_completed [trace_id=4c89ad1d902b99f4aa13b8b8e2cc362a]
GET /items/ HTTP/1.1 200 OK
```

### Error-path log excerpt
```
request_started [trace_id=a37cd268a82cf65b28dea76bb15831f5]
auth_success [trace_id=a37cd268a82cf65b28dea76bb15831f5]
db_query INFO [trace_id=a37cd268a82cf65b28dea76bb15831f5]
db_query ERROR [trace_id=a37cd268a82cf65b28dea76bb15831f5]
items_list_failed_as_not_found WARNING [trace_id=a37cd268a82cf65b28dea76bb15831f5]
request_completed [trace_id=a37cd268a82cf65b28dea76bb15831f5]
GET /items/ HTTP/1.1 404 Not Found
```

(VictoriaLogs UI screenshot to be added)

## Task 3B — Traces

(Healthy trace screenshot: trace_id=4c89ad1d902b99f4aa13b8b8e2cc362a)
(Error trace screenshot: trace_id=a37cd268a82cf65b28dea76bb15831f5)

## Task 3C — Observability MCP tools

### Normal conditions
Agent response: "No LMS backend errors in the last 10 minutes. The system is healthy with 56 items available."

### After stopping PostgreSQL
Agent response: "There are 6 errors in the Learning Management Service in the last 10 minutes.
Error details:
- Type: Database connection failure
- Error message: [Errno -2] Name or service not known
- Source: lms_backend.db.items (database queries on the item table)
What's likely wrong: The LMS backend cannot resolve the database hostname, indicating either DNS configuration issues, database service is down, or network connectivity problems."

## Task 4A — Multi-step investigation

With PostgreSQL stopped, agent response to "What went wrong?":

8 errors detected in the last 15 minutes affecting the Learning Management Service.

Root Cause: Database Connectivity Problems:
1. Closed database connections (asyncpg InterfaceError: connection is closed)
2. DNS resolution failures ([Errno -2] Name or service not known)

Evidence from Tracing: trace shows GET /items/ → DB query failed → HTTP 404 returned (masking the real DB error).

## Task 4B — Proactive health check

Health Check Summary (11:27 UTC):
- 1 error detected in the last 2 minutes
- Issue: Database connection failure - DNS resolution error when connecting to PostgreSQL
- Trace insight: GET /items/ returned HTTP 404, but the underlying cause was a database connectivity issue. The application may be masking the DB error with a 404 response.

(Screenshot added)

## Task 4C — Bug fix and recovery

### Root cause
The planted bug was in `backend/src/lms_backend/routers/items.py` in the `get_items` endpoint. A broad `except Exception` block caught ALL exceptions (including database connection errors) and returned HTTP 404 "Items not found" instead of propagating the real error. This masked database failures as missing data.

### Fix
Changed the exception handler to:
- Re-raise HTTPException as-is
- Log the real error with `logger.error` instead of `logger.warning`
- Return HTTP 500 with the actual error message instead of 404
```diff
-    except Exception as exc:
-        logger.warning(
-            "items_list_failed_as_not_found",
-            extra={"event": "items_list_failed_as_not_found"},
-        )
-        raise HTTPException(
-            status_code=status.HTTP_404_NOT_FOUND,
-            detail="Items not found",
-        ) from exc
+    except HTTPException:
+        raise
+    except Exception as exc:
+        logger.error(
+            "items_list_failed",
+            extra={"event": "items_list_failed", "error": str(exc)},
+        )
+        raise HTTPException(
+            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
+            detail=f"Internal server error: {exc}",
+        ) from exc
```

### Post-fix failure check
After redeploy with PostgreSQL stopped, curl returns:
HTTP/1.1 500 Internal Server Error
{"detail":"Internal server error: [Errno -2] Name or service not known"}

The real database error is now visible instead of the misleading 404.

### Healthy follow-up
After PostgreSQL restart, health check reports system looks healthy.
