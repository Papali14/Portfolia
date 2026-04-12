# Bugfix Prompt Guide

## Purpose

Use this prompt for future bug fixes and regression work in Portfolia.

## When to use

- a test fails unexpectedly
- CLI behavior no longer matches the README
- data validation or edge-case handling breaks
- you want to add a regression test for a bug

## Prompt template

```markdown
I need a bug fix for Portfolia.
Provide:
- the failing behavior or test
- the expected behavior
- the minimal code change
- the regression test to add or update
```

## Example request

"Fix the bug where `MockPanPortfolioProvider.fetch_holdings` accepts a PAN shorter than 10 characters. Include a regression test and a short explanation."
