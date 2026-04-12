---
name: run
description: "Use to start Portfolia locally for development, including CLI execution and UI static hosting."
---

# Run Agent

This agent helps start the Portfolia application locally for development and testing.

Use it when you need:
- to launch the CLI with sample or real portfolio inputs
- to run the static UI server for browser-based testing
- to validate local changes by running the app end-to-end
- to confirm startup commands and environment expectations

## Typical commands

- `python -m app.main --source-file sample_portfolio.csv --goal "Retirement" --target 2000000 --years 10 --risk moderate --monthly-investment 30000`
- `python -m http.server 8000` and open `http://localhost:8000/ui/`

> Keep local startup workflows simple and aligned with the repo README. Avoid introducing complex dev servers unless required.
