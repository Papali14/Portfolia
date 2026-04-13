# AI Operating Docs (Agent-Agnostic)

This directory is the shared source of truth for all AI agents used in this repository, including Codex and Copilot-style agents.

## Purpose

- Provide one common context model for all agents.
- Provide reusable role skills for architecture, development, and testing.
- Keep outputs consistent regardless of agent implementation.

## Start here

1. Read [context.md](context.md).
2. Pick the role skill for the task:
   - [architect.md](skills/architect.md)
   - [developer.md](skills/developer.md)
   - [tester.md](skills/tester.md)
3. Apply docs-sync rules in [codex/process.md](../../codex/process.md).

## Governance

- If behavior, architecture, API contract, tests, or workflow changes, markdown updates are mandatory in the same task.
- The same agent that changes code owns documentation updates for that change.
