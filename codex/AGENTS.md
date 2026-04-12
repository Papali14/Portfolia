# Portfolia Codex: Agent Reference

This codex describes workspace agents and prompt guides for Portfolia.

## Agents

- `dev-helper` — Developer assistance for features, architecture, refactoring, testing, and documentation.
- `bugfix` — Bug triage and fix workflows, with a test-first mindset and minimal safe changes.
- `run` — Start Portfolia locally for development, including CLI execution and UI static hosting.

## How to use

1. Open a new chat or agent session.
2. Reference the agent by name or ask for the corresponding task:
   - `Use the dev-helper agent to implement a new feature in app/main.py`
   - `Use the bugfix agent to diagnose a failing test and propose a fix`
3. Keep requests focused and include relevant repository context when possible.

## Codex structure

- `codex/prompts/` — prompt templates for architecture, feature planning, debugging, refactoring, and bug fixes.
- `codex/plans/` — planning templates for feature work.

## Notes

These files are designed to make developer workflow more friendly and consistent. Use the agent definitions alongside the prompt guides to get practical, repo-specific recommendations.
