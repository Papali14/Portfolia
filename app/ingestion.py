from __future__ import annotations

import csv
from abc import ABC, abstractmethod
from pathlib import Path

from app.models import Holding

VALID_ASSET_CLASSES = {"equity", "debt", "gold", "cash"}


class PanPortfolioProvider(ABC):
    @abstractmethod
    def fetch_holdings(self, pan: str) -> list[Holding]:
        """Fetch and normalize holdings for the given PAN."""


class MockPanPortfolioProvider(PanPortfolioProvider):
    """Starter mock implementation for PAN-based ingestion."""

    def fetch_holdings(self, pan: str) -> list[Holding]:
        pan = pan.strip().upper()
        if len(pan) != 10:
            raise ValueError("Invalid PAN format.")

        # In production this would call an external aggregation API.
        return [
            Holding(symbol="NIFTYBEES", asset_class="equity", market_value=350000),
            Holding(symbol="GILT-FUND", asset_class="debt", market_value=180000),
            Holding(symbol="GOLDBEES", asset_class="gold", market_value=80000),
            Holding(symbol="SAVINGS", asset_class="cash", market_value=40000),
        ]


def load_holdings_from_csv(file_path: str | Path) -> list[Holding]:
    holdings: list[Holding] = []
    with Path(file_path).open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        required = {"symbol", "asset_class", "market_value"}
        if not reader.fieldnames or not required.issubset(set(reader.fieldnames)):
            raise ValueError(f"CSV must contain headers: {sorted(required)}")

        for row in reader:
            asset_class = row["asset_class"].strip().lower()
            if asset_class not in VALID_ASSET_CLASSES:
                raise ValueError(
                    f"Invalid asset_class '{asset_class}'. Expected one of {sorted(VALID_ASSET_CLASSES)}"
                )
            holdings.append(
                Holding(
                    symbol=row["symbol"].strip(),
                    asset_class=asset_class,
                    market_value=float(row["market_value"]),
                )
            )

    if not holdings:
        raise ValueError("Portfolio is empty.")

    return holdings
