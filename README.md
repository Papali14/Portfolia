# Portfolia: Broker-Agnostic Goal-Based Portfolio Strategy

This project is a starter app that:

1. Ingests a portfolio from **any broker export file (CSV)**, or
2. Ingests via **PAN lookup** using a pluggable provider,
3. Normalizes holdings into a common model,
4. Generates a goal-based strategy (target allocation + rebalance + SIP guidance).

## Why this design

Broker data formats differ. The app converts all sources into one normalized schema:

- `symbol`
- `asset_class` (`equity`, `debt`, `gold`, `cash`)
- `market_value`

After normalization, strategy logic is source-independent.

## Quick start

```bash
python -m app.main \
  --source-file sample_portfolio.csv \
  --goal "Child Education" \
  --target 5000000 \
  --years 10 \
  --risk moderate \
  --monthly-investment 30000
```

Or via PAN (mock provider in this starter):

```bash
python -m app.main \
  --source-pan ABCDE1234F \
  --goal "Retirement" \
  --target 20000000 \
  --years 18 \
  --risk growth \
  --monthly-investment 50000
```

## CSV format

The CSV must include these headers:

- `symbol`
- `asset_class`
- `market_value`

See `sample_portfolio.csv`.

## Run tests

```bash
python -m pytest -q
```
