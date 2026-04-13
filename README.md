# Portfolia

Portfolia is a Next.js + React + TypeScript application for portfolio ingestion and analysis. Users upload broker Excel files and receive normalized holdings plus visual insights.

## Current status

- Active stack: Next.js 14, React 18, TypeScript, Tailwind CSS, Recharts, `xlsx`
- API-first ingestion flow using `app/api/process-portfolio/route.ts`
- Browser UI for upload + analysis in `app/` and `components/`
- Legacy Python docs and commands have been removed from this README

## Quick start

1. Use Node.js (recommended: `fnm use default` if your machine uses `fnm`).
2. Install dependencies with `npm install`.
3. Start the app with `npm run dev`.
4. Open `http://localhost:3000`.

## Scripts

- `npm run dev` starts development server
- `npm run build` creates production build
- `npm run start` runs production server
- `npm run lint` runs lint checks

## Product flow

1. User uploads `.xlsx` or `.xls` in the UI.
2. `FileUpload` posts multipart form data to `POST /api/process-portfolio`.
3. API parses workbook, detects relevant columns, infers asset class, and returns normalized holdings.
4. `PortfolioAnalysis` renders totals, charts, and holdings table.

## Key directories

- `app/` Next.js app router pages, layouts, and API routes
- `components/` UI components
- `tests/` sample input files used for manual verification
- `codex/` agent prompts, plans, and process rules

## Documentation governance

Agent and workflow documentation is maintained under `codex/`.

- Shared cross-agent skills and context live in `docs/ai/`.
- Start with [codex/AGENTS.md](codex/AGENTS.md)
- Then load [docs/ai/README.md](docs/ai/README.md)
- Follow [codex/process.md](codex/process.md) for mandatory docs-update rules
- Use the templates in `codex/prompts/` and `codex/plans/`

Rule: if a code change alters behavior, architecture, API, testing approach, or developer workflow, the same change must update affected markdown before task completion.
