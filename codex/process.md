# Portfolia Change And Documentation Process

This process is agent-agnostic and applies to all task types: architecture, feature, bugfix, debug, and refactor.

## Objective

Keep code and documentation synchronized so future agents can act with high confidence and produce consistent outputs.

## Required lifecycle for every task

1. Understand the request and map impacted modules.
2. Implement the change safely.
3. Validate behavior (tests, lint, or manual verification).
4. Run Documentation Delta Check.
5. Close task only after code + docs are aligned.

## Documentation Delta Check (mandatory)

Before task completion, answer these questions:

- Did behavior change for users or developers?
- Did any API contract or data shape change?
- Did architecture boundaries or responsibilities change?
- Did setup/run/test workflow change?
- Did failure modes, edge cases, or debugging guidance change?

If any answer is "yes", update affected markdown in the same task.

## Docs ownership rule

The same agent that implements the code change must update related documentation before closing the task. Do not defer docs updates to a future task unless explicitly requested by the user.

## Definition of Done

A task is done only when all are true:

- Code changes are complete.
- Validation evidence is provided.
- Docs delta check is explicitly reported.
- Required markdown updates are committed in the same change.
- Remaining risks or follow-ups are clearly listed.

## Suggested markdown mapping

- Product usage, setup, scripts: `README.md`
- Shared agent context and skills: `docs/ai/context.md`, `docs/ai/skills/*.md`
- Agent operating model and policy links: `codex/AGENTS.md`
- Prompt contracts and output format: `codex/prompts/*.md`
- Feature planning: `codex/plans/*.md`

## Output contract for agents

For consistency across agent implementations, every substantial task response should include:

- What changed
- Why it changed
- How it was validated
- Docs impact (updated files or explicit no-change reason)
- Residual risks or next steps
