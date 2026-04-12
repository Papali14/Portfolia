---
description: |
  Workspace instructions for Portfolia, a Python starter app for broker-agnostic goal-based portfolio strategy.
  Use these guidelines when editing code, writing tests, improving the CLI, or updating the browser-based UI.
---

# Portfolia Workspace Instructions

- This is a Python project. The primary CLI entrypoint is `python -m app.main`.
- Run tests with `python -m pytest -q`.
- Preserve the existing domain model and normalization flow:
  - `app.ingestion` loads broker CSVs or PAN-based portfolio data.
  - `app.models` defines portfolio holdings and goal objects.
  - `app.strategy` generates goal-based allocation, rebalance, and SIP guidance.
  - `app.research` adds optional market research output.
- CSV input is required to include headers: `symbol`, `asset_class`, `market_value`.
- Valid asset classes are `equity`, `debt`, `gold`, and `cash`.
- Risk profiles are limited to `conservative`, `moderate`, `growth`, and `aggressive`.
- UI assets live under `ui/` and are served statically; do not mix backend logic into the UI folder.
- Keep CLI output JSON-compatible and stable for tests.
- Do not introduce recommendations for options trading or intraday trading; the domain is long-term goal-based guidance.
- Prefer clear error handling for invalid CSVs, invalid PANs, and missing portfolio data.
- When adding features, follow the existing simple, testable architecture rather than creating heavyweight frameworks.
- For additional context, refer to `README.md`.
