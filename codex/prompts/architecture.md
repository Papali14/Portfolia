# Architecture Prompt Guide

## Purpose

Use this prompt when you want a design review, architecture recommendation, or system-level guidance for Portfolia.

## When to use

- Designing a new feature or extension
- Reviewing the current `app/` structure and separation of concerns
- Validating whether a change fits the existing model and normalization flow
- Suggesting improvements for testability or maintainability

## Prompt template

```markdown
I need an architecture review for Portfolia, a Python starter app for goal-based portfolio strategy.
The repo has `app/` for backend logic, `tests/` for unit coverage, and `ui/` for static browser assets.
Please analyze the current design and suggest:
- whether package boundaries are clear
- whether the CLI model and data normalization flow are appropriate
- any improvements for maintainability or future extension
- any risks or anti-patterns to avoid
```

## Example request

"Review the existing Portfolia architecture and describe how `app.ingestion`, `app.strategy`, and `app.research` should interact. Suggest a clean way to add a new `tax` module without breaking current tests."
