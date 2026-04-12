# Feature Prompt Guide

## Purpose

Use this prompt to define, implement, and test new features in Portfolia.

## When to use

- Adding a new CLI option or goal type
- Extending the portfolio ingestion flow
- Improving output formatting or report generation
- Building new UI support under `ui/`

## Prompt template

```markdown
Help me add a new feature to Portfolia.
Describe the change, the modifiers, and the tests required.
Include:
- a short summary of the feature
- the files or modules to change
- a minimal set of tests to validate behavior
- any CLI or user-facing output considerations
```

## Example request

"Add support for a `--currency` option to the CLI that formats the goal target and strategy output in the selected currency. Show the code changes and the new test cases."
