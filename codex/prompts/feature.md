# Feature Prompt Guide

## Purpose

Use this for new feature development across UI, API, or data-processing layers.

## Required response contract

The agent response must include:

- Feature summary and scope
- Implementation plan
- Files to change
- Validation and tests
- Documentation impact

## Prompt template

```markdown
Help me implement a feature in Portfolia.

Feature:
- Goal:
- User value:
- In scope:
- Out of scope:

Implementation context:
- Related files:
- Data/API impact:
- UI impact:

Please deliver:
1. Minimal implementation approach
2. Exact file-level change plan
3. Test plan (unit/integration/manual as applicable)
4. Risks and fallback behavior
5. Documentation impact:
   - Which markdown files to update in this same task
   - If none, why no update is needed
```

## Quality bar

- Keep implementation incremental and reversible.
- Preserve compatibility unless breaking change is explicitly approved.
- Include edge-case handling and error messaging.
- Follow [process.md](../process.md) docs-sync rules.
