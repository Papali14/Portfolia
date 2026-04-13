# Architecture Prompt Guide

## Purpose

Use this for architecture reviews, system design decisions, and module boundary discussions in Portfolia.

## Required response contract

The agent response must include:

- Current-state summary
- Proposed architecture
- Tradeoffs and alternatives
- Risks and mitigation
- Validation approach
- Documentation impact

## Prompt template

```markdown
I need an architecture review for Portfolia (Next.js + React + TypeScript).

Context:
- Task goal:
- Current files/modules involved:
- Constraints (performance, timeline, compatibility):

Please provide:
1. Current-state architecture assessment
2. Proposed target design and why
3. Tradeoffs and rejected alternatives
4. Risks, edge cases, and rollback strategy
5. Validation plan (tests/manual checks)
6. Documentation impact:
   - Which markdown files must be updated now
   - If none, explain why
```

## Quality bar

- Prefer incremental evolution over broad rewrites.
- Keep contracts explicit between UI, API, and data processing.
- Call out coupling, hidden state assumptions, and migration risks.
- Follow [process.md](../process.md) docs-sync rules.
