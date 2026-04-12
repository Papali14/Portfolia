from pathlib import Path

import pytest

from app.ingestion import MockPanPortfolioProvider, load_holdings_from_csv


def test_load_holdings_from_csv_success(tmp_path: Path):
    csv_path = tmp_path / "portfolio.csv"
    csv_path.write_text(
        "symbol,asset_class,market_value\nINFY,equity,1000\nLIQ,debt,2000\n",
        encoding="utf-8",
    )

    holdings = load_holdings_from_csv(csv_path)
    assert len(holdings) == 2
    assert holdings[0].asset_class == "equity"


def test_mock_pan_provider_validates_pan_length():
    with pytest.raises(ValueError):
        MockPanPortfolioProvider().fetch_holdings("ABC")
