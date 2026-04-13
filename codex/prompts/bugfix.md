# Bugfix Prompt Guide

## Purpose

Use this for regression fixes and production bug corrections with minimal blast radius.

## Required response contract

The agent response must include:

- Problem statement and severity
- Root cause
- Minimal safe fix
- Regression coverage
- Documentation impact

## Prompt template

```markdown
I need a bug fix in Portfolia.

Bug details:
- Actual behavior:
- Expected behavior:
- Error/logs:
- Repro steps:
- Suspected files:

Please provide:
1. Root cause analysis
2. Minimal code fix
3. Regression test(s) to prevent recurrence
4. Risk assessment and side effects
5. Documentation impact:
   - Which markdown files must be updated now
   - If none, justify no docs change
```

## Quality bar

- Prioritize correctness and low-risk patching.
- Add or update regression tests whenever feasible.
- Document assumptions when full validation is not possible.
- Follow [process.md](../process.md) docs-sync rules.
