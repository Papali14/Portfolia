# Skill: Developer

Use this skill for feature implementation, bug fixing, and refactoring.

## Mission

Deliver small, reliable changes with clear validation and synced documentation.

## Required process

1. Read shared context: [context.md](../context.md).
2. Confirm scope and non-goals.
3. Implement minimal safe code changes.
4. Validate with lint/tests/manual checks.
5. Run docs delta check and update markdown in the same task.

## Required output

- Files changed and why
- Validation evidence
- Compatibility and edge-case notes
- Documentation impact statement
- Residual risks or follow-up

## Quality guardrails

- Avoid unnecessary abstraction.
- Preserve behavior unless requested otherwise.
- Keep API responses stable and JSON-compatible.
- Include defensive handling for malformed or missing inputs.
