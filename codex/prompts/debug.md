# Debug Prompt Guide

## Purpose

Use this for root-cause diagnosis before or during a fix.

## Required response contract

The agent response must include:

- Reproduction strategy
- Root-cause hypothesis (with evidence)
- Confirmed cause
- Safe fix recommendation
- Documentation impact

## Prompt template

```markdown
Help me debug a Portfolia issue.

Context:
- Symptom/error:
- Expected behavior:
- Observed behavior:
- Affected files/modules:
- Recent related changes:

Please provide:
1. Minimal repro steps
2. Root-cause analysis path (what to inspect and why)
3. Confirmed or most likely root cause
4. Safe fix strategy and validation checks
5. Documentation impact:
   - Which markdown should be updated if fix changes behavior/workflow
   - If none, explain why
```

## Quality bar

- Separate hypothesis from confirmed facts.
- Prefer deterministic repro over guess-based debugging.
- Include what to monitor after deploying a fix.
- Follow [process.md](../process.md) docs-sync rules.
