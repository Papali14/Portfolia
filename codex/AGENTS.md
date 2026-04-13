# Portfolia Agent Operating Model

This file defines the operating model and points to shared role skills that are agent-agnostic.

## Core principles

- Keep changes small, verifiable, and production-safe.
- Prefer behavior-preserving refactors unless a behavior change is explicitly requested.
- Provide evidence: list what was changed, how it was verified, and what remains risky.
- Update docs in the same task whenever behavior or workflow changes.

## Shared skills

All agents must load the shared context and the role skill from `docs/ai/`:

- Context: [docs/ai/context.md](../docs/ai/context.md)
- Architect skill: [docs/ai/skills/architect.md](../docs/ai/skills/architect.md)
- Developer skill: [docs/ai/skills/developer.md](../docs/ai/skills/developer.md)
- Tester skill: [docs/ai/skills/tester.md](../docs/ai/skills/tester.md)

These are the canonical role instructions for Codex/Copilot and any future agent runtime.

## Mandatory docs-sync rule

If a task changes any of the following, the same agent must update markdown in the same task:

- Architecture or data flow
- API contract or request/response behavior
- Build/run/test commands
- Error-handling expectations
- Team workflow, coding standards, or Definition of Done

Use [process.md](process.md) as the source of truth for this check.

## Prompt sources

- `codex/prompts/architecture.md`
- `codex/prompts/feature.md`
- `codex/prompts/bugfix.md`
- `codex/prompts/debug.md`
- `codex/prompts/refactor.md`

Prompt guides define task-specific request/response structure. Role behavior comes from `docs/ai/skills/*`.
