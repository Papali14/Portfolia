# Skill: Architect

Use this skill for architecture/design work and system-level decisions.

## Mission

Design changes that are maintainable, incremental, and explicit about tradeoffs.

## Required process

1. Read shared context: [context.md](../context.md).
2. Assess current boundaries (UI, API, data processing).
3. Propose target architecture with alternatives.
4. Define risks, rollback, and validation.
5. Run docs delta check and update markdown if needed.

## Required output

- Current-state summary
- Proposed design
- Tradeoffs and rejected options
- Risks and mitigation
- Validation strategy
- Documentation impact statement

## Quality guardrails

- Prefer incremental changes over broad rewrites.
- Keep contracts stable unless explicitly approved to break.
- Call out hidden coupling and migration complexity.
