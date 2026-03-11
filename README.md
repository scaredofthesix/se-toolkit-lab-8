# Lab 6 — Build Your Own Agent

The lab gets updated regularly, so do [sync your fork with the upstream](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/syncing-a-fork#syncing-a-fork-branch-from-the-command-line) from time to time.

<h2>Table of contents</h2>

- [Lab story](#lab-story)
- [Learning advice](#learning-advice)
- [Learning outcomes](#learning-outcomes)
- [Tasks](#tasks)
  - [Prerequisites](#prerequisites)
  - [Required](#required)

## Lab story

You have a running Learning Management Service — a backend, a database full of analytics data, and a frontend dashboard. The course is coming to a close and you need to review everything you've learned.

Instead of manually reviewing, you'll build a **CLI agent** that can answer questions about the course and about your own system. The agent uses an LLM with tools to read your codebase and query your API.

An evaluation benchmark tests your agent with ~30 questions. You can't see the questions upfront — you discover them by running the checker. Each failed question tells you what went wrong, and you fix it. By the time your agent passes, you've reviewed the course material and understood how agents work.

## Learning advice

Read the tasks, do the setup properly, work with an agent to help you:

> What do we need to do in Task x? Explain, I want to maximize learning.

> Why is this important? What exactly do we need to do?

You need an agent that has access to the whole repo to work effectively.

## Learning outcomes

By the end of this lab, you should be able to:

- Explain how an agentic loop works: user input → LLM → tool call → execute → feed result → repeat until final answer.
- Integrate with an LLM API using the OpenAI-compatible chat completions format with tool/function calling.
- Implement tools that read files, list directories, and query HTTP APIs, then register them as function-calling schemas.
- Build a CLI that accepts structured input and produces structured output (JSON).
- Debug agent behavior by examining tool call traces, identifying prompt issues, and fixing tool implementations.
- Assess agent quality against a benchmark, iterating on prompts and tools to improve pass rate.

In simple words, you should be able to say:
>
> 1. I built an agent that calls an LLM and answers questions!
> 2. I gave it tools to read files and query my API!
> 3. I iterated until it passed the evaluation benchmark!

## Tasks

### Prerequisites

1. Complete the [lab setup](./lab/tasks/setup-simple.md#lab-setup)

> **Note**: If this is the first lab you are attempting in this course, you need to do the [full version of the setup](./lab/tasks/setup.md#lab-setup)

### Required

1. [Basic agent loop](./lab/tasks/required/task-1.md#basic-agent-loop)
2. [Add tools](./lab/tasks/required/task-2.md#add-tools)
3. [Pass the benchmark](./lab/tasks/required/task-3.md#pass-the-benchmark)
