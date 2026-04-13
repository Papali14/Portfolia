# Refactor Prompt Guide

## Purpose

Use this for behavior-preserving code quality improvements.

## Required response contract

The agent response must include:

- Refactor objective
- Scope and non-goals
- Behavior-preservation checks
- Validation results
- Documentation impact

## Prompt template

```markdown
I want to refactor Portfolia without changing behavior.

Refactor details:
- Target files/modules:
- Current pain points:
- Constraints:

Please provide:
1. Refactor plan with minimal risk
2. Specific code changes and rationale
3. Behavior-preservation verification plan
4. Residual risks
5. Documentation impact:
   - Which markdown files should be updated
   - If none, justify no docs changes
```

## Quality bar

- Do not mix refactor with feature creep.
- Preserve public contracts and user-observable behavior.
- Keep diffs understandable and test-backed.
- Follow [process.md](../process.md) docs-sync rules.
