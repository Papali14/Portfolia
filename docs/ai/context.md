# Shared Agent Context

Use this file to build task context before implementation. It is designed for any agent runtime.

## Product snapshot

- Product: Portfolia
- Stack: Next.js 14, React 18, TypeScript, Tailwind, Recharts, `xlsx`
- Main workflow:
  1. Upload Excel file in UI
  2. POST to `app/api/process-portfolio/route.ts`
  3. Normalize holdings (`symbol`, `asset_class`, `market_value`)
  4. Render analysis in charts and table

## Key paths

- `app/` pages, layout, API routes
- `components/` UI components
- `tests/` sample files for manual verification
- `codex/prompts/` task prompt guides
- `codex/process.md` docs-sync and Definition of Done

## Task intake checklist

Before coding:

1. Confirm task type: architecture, feature, bugfix, debug, refactor.
2. Identify impacted files and contracts.
3. Identify validation strategy (lint, tests, or manual checks).
4. Identify likely docs impact.

## Output contract

For substantial tasks, include:

- What changed
- Why it changed
- How it was validated
- Docs impact (updated files or explicit no-change reason)
- Residual risks or follow-up

## Documentation Delta Check

Answer before closing task:

- Did user-facing or developer-facing behavior change?
- Did API/data contract change?
- Did architecture responsibility change?
- Did run/build/test workflow change?
- Did error-handling/debugging guidance change?

If any answer is yes, update markdown in the same task.
