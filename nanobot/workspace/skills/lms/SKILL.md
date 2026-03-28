---
name: lms
description: Use LMS MCP tools for live course data
always: true
---

# LMS Skill

You have access to the following LMS tools:

- **lms_health** — Check if the LMS backend is healthy and report the item count. No parameters needed.
- **lms_labs** — List all labs available in the LMS. No parameters needed.
- **lms_learners** — List all learners registered in the LMS. No parameters needed.
- **lms_pass_rates** — Get pass rates for a lab. Requires `lab` parameter (e.g. "lab-04").
- **lms_timeline** — Get submission timeline for a lab. Requires `lab` parameter.
- **lms_groups** — Get group performance for a lab. Requires `lab` parameter.
- **lms_top_learners** — Get top learners by average score for a lab. Requires `lab` and optional `limit` parameter.
- **lms_completion_rate** — Get completion rate for a lab. Requires `lab` parameter.
- **lms_sync_pipeline** — Trigger the LMS sync pipeline. No parameters needed.

## Strategy

- If the user asks for scores, pass rates, completion, groups, timeline, or top learners **without naming a lab**, call `lms_labs` first to get available labs, then ask the user which lab they want.
- If multiple labs are available, present the lab titles and ask the user to choose one before proceeding.
- When lab choice is needed, use each lab title as the user-facing label.
- Format numeric results nicely: use percentages for rates, round to one decimal place.
- Keep responses concise and direct.
- When the user asks "what can you do?", explain that you can check LMS health, list labs and learners, show pass rates, timelines, group performance, top learners, completion rates, and trigger sync.
- Never guess or fabricate LMS data. Always use the tools to get real data.
