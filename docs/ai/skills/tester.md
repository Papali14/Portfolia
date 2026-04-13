# Skill: Tester

Use this skill for validation planning, regression prevention, and confidence assessment.

## Mission

Ensure changes are reproducible, verified, and safe to ship.

## Required process

1. Read shared context: [context.md](../context.md).
2. Build reproducible scenarios (happy path + edge cases).
3. Define checks (automated or manual).
4. Record results and residual risks.
5. Run docs delta check for test/runbook updates.

## Required output

- Repro steps
- Expected versus actual behavior
- Validation coverage and gaps
- Residual risk assessment
- Documentation impact statement

## Quality guardrails

- Prefer deterministic checks over ad-hoc observation.
- Include negative-path validation for errors and malformed inputs.
- Flag untestable areas and why they remain unverified.
