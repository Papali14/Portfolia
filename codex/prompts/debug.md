# Debug Prompt Guide

## Purpose

Use this prompt when you need help diagnosing a bug or fixing a failing test in Portfolia.

## When to use

- A unit test is failing in `tests/`
- CLI output is incorrect or unstable
- A function produces an unexpected error or exception
- You need to isolate the root cause from repository context

## Prompt template

```markdown
I have a bug in Portfolia. Here are the details:
- failing test or error message
- relevant file paths and function names
- expected behavior
- actual behavior
Please describe the root cause, minimal repro steps, and a safe code fix.
```

## Example request

"Help me debug why `load_holdings_from_csv` raises `ValueError: Portfolio is empty.` for a CSV with valid headers. Show the root cause and test changes needed."
