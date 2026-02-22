from __future__ import annotations

import argparse
import json

from app.ingestion import MockPanPortfolioProvider, load_holdings_from_csv
from app.models import Goal
from app.strategy import StrategyEngine


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Broker-agnostic goal-based portfolio strategy")

    src = parser.add_mutually_exclusive_group(required=True)
    src.add_argument("--source-file", help="Path to broker export CSV")
    src.add_argument("--source-pan", help="PAN for provider-based portfolio fetch")

    parser.add_argument("--goal", required=True, help="Goal name")
    parser.add_argument("--target", type=float, required=True, help="Goal target amount")
    parser.add_argument("--years", type=int, required=True, help="Years to goal")
    parser.add_argument(
        "--risk",
        choices=["conservative", "moderate", "growth", "aggressive"],
        required=True,
        help="Risk profile",
    )
    parser.add_argument(
        "--monthly-investment",
        type=float,
        default=0.0,
        help="Planned monthly contribution",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.source_file:
        holdings = load_holdings_from_csv(args.source_file)
    else:
        holdings = MockPanPortfolioProvider().fetch_holdings(args.source_pan)

    goal = Goal(
        name=args.goal,
        target_amount=args.target,
        years_to_goal=args.years,
        risk_profile=args.risk,
    )

    recommendation = StrategyEngine().recommend(
        holdings=holdings,
        goal=goal,
        monthly_investment=args.monthly_investment,
    )

    print(json.dumps(recommendation.__dict__, indent=2))


if __name__ == "__main__":
    main()
