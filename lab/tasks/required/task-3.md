# Pass the Benchmark

Iterate on your agent until it passes the evaluation benchmark.

## [Git workflow](../../../wiki/git-workflow.md)

1. Create an issue titled `[Task] Pass the Benchmark`.
2. Pull latest `main` from `origin` and `upstream`.
3. Create a branch from `main` (e.g., `task/pass-the-benchmark`).
4. Work on the branch. Commit as you go using [conventional commits](https://www.conventionalcommits.org/) (e.g., `feat:`, `docs:`, `test:`).
5. Push, create a PR to `main` in **your fork** (not upstream). Link the issue using a keyword (e.g., `Closes #3`).
6. Get a review from your partner, merge (this closes the issue automatically), delete the branch.

## What you will do

Run the evaluation benchmark, examine failures, fix your agent, and repeat. The benchmark tests your agent with questions about the course material and your deployed system.

You cannot see the questions upfront — you discover them by running the eval. Each failed question shows you what went wrong. Fix it, re-run, and move on to the next one.

```
run eval → see failure → diagnose → fix agent → re-run → next failure → ...
```

## How to run the benchmark

Run `run_eval.py` from the project root:

```bash
python run_eval.py
```

It reads your autochecker credentials from `.env` / `.env.docker.secret` (`AUTOCHECKER_API_URL`, `AUTOCHECKER_EMAIL`, `AUTOCHECKER_PASSWORD`) — same ones you configured during setup.

The script:

1. Fetches one question at a time from the autochecker API.
2. Runs `python agent.py "question"` locally.
3. Checks the answer against the expected result.
4. On pass: prints green, moves to the next question.
5. On fail: prints red with feedback, stops.

```
  + [1/25] A teammate pushes broken code directly to main...
  + [2/25] You see a commit message that just says 'fix'...
  + [3/25] Your teammate and you both edited the same line...

  x [4/25] You change your Python code and run 'docker compose up -d'...
    Your answer: restart the container
    Expected: answer should contain any of: ["--build", "build", ...]

3/25 passed
```

Fix the failing question, then run `python run_eval.py` again.

> **Note:** The autochecker bot tests your agent with additional questions not present in `run_eval.py`. You need a genuinely working agent — not hard-coded answers.

## Debugging workflow

When a question fails, diagnose the root cause:

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| Wrong factual answer | System prompt missing this topic | Add the topic to your system prompt |
| Agent doesn't use a tool when it should | Tool description too vague for the LLM | Improve the tool's description in the schema |
| Tool called but returns an error | Bug in tool implementation | Fix the tool code, test it in isolation |
| Tool called with wrong arguments | LLM misunderstands the schema | Clarify parameter descriptions |
| Agent times out | Too many tool calls or slow LLM | Reduce max iterations, try a faster model |
| Answer is close but doesn't match | Phrasing doesn't contain expected keyword | Adjust system prompt to be more precise |

## Deliverables

### 1. Plan (`plans/task-3.md`)

Before iterating, create `plans/task-3.md`. Run the benchmark once and document:

- Your current score (e.g., "12/25 passed").
- The first few failures and your diagnosis of each.
- Your strategy for improving the agent.

Commit:

```text
docs: add benchmark iteration plan
```

### 2. Agent improvements (update `agent.py`)

Iterate on your agent until `run_eval.py` passes all 25 questions. Common improvements:

- Expand or refine the system prompt.
- Improve tool descriptions so the LLM calls the right tool.
- Fix tool implementations (path handling, error cases, response parsing).
- Handle edge cases (empty responses, timeout, malformed data).

Commit as you go. Example:

```text
fix: improve system prompt for Docker questions
fix: handle empty file in read_file tool
feat: add retry logic for LLM API rate limits
```

### 3. Documentation (update `AGENT.md`)

Update `AGENT.md` with:

- **Final architecture**: any changes made during iteration.
- **Lessons learned**: what failed and why, what you changed.
- **Eval score**: your final `run_eval.py` result.

Commit:

```text
docs: update agent documentation with benchmark results
```

### 4. Tests

Update your regression tests to cover any new edge cases you discovered during iteration.

Commit:

```text
test: update regression tests with benchmark edge cases
```

### 5. Deployment

Deploy the final agent to your VM. The autochecker bot will run the full benchmark (25 shared questions + 9 additional questions = 34 total).

You need at least **75%** (26/34) to pass.

## Acceptance criteria

- [ ] Issue has the correct title.
- [ ] `plans/task-3.md` exists with the initial diagnosis and strategy.
- [ ] `run_eval.py` passes all 25 questions locally.
- [ ] `AGENT.md` documents the final architecture and lessons learned.
- [ ] Regression tests are updated.
- [ ] The agent passes the autochecker bot benchmark (≥75%).
- [ ] PR is approved and merged.
- [ ] Issue is closed by the PR.
