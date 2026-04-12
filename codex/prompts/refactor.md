# Refactor Prompt Guide

## Purpose

Use this prompt when you want to improve Portfolia code quality without changing behavior.

## When to use

- cleaning up duplicated logic
- simplifying testable functions
- reorganizing module responsibilities
- making `app/`, `tests/`, or `ui/` easier to understand

## Prompt template

```markdown
I want to refactor Portfolia with a behavior-preserving change.
Focus on readability, small scope, and existing tests.
Include:
- the target files or functions
- the reason for the refactor
- verification steps or tests
```

## Example request

"Refactor `app.ingestion.load_holdings_from_csv` to improve validation and reduce nested logic, while keeping the current behavior and tests intact."
