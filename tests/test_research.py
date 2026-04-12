import datetime as dt

from app.models import Holding
from app.research import (
    FinancialSnapshot,
    MarketResearchService,
    SentimentSnapshot,
)


class StubClient:
    def fetch_daily_prices(self, symbol: str, lookback_years: int = 5):
        start = dt.date(2021, 1, 1)
        prices = []
        px = 100.0
        for i in range(252 * 5):
            day = start + dt.timedelta(days=i)
            if day.weekday() >= 5:
                continue
            px *= 1.0004
            prices.append((day, px))
        return prices, ["https://stub/prices"]

    def fetch_financial_snapshot(self, symbol: str):
        return (
            FinancialSnapshot(
                revenue_growth_pct=12.0,
                gross_margins_pct=45.0,
                operating_margins_pct=18.0,
                debt_to_equity=0.4,
                return_on_equity_pct=19.0,
            ),
            ["https://stub/financials"],
            [],
        )

    def fetch_sentiment_snapshot(self, symbol: str, max_items: int = 25):
        return SentimentSnapshot(10, 0.5), ["https://stub/news"], []


def test_research_service_produces_accumulate_for_strong_equity():
    svc = MarketResearchService(client=StubClient())
    out = svc.analyze_holding(Holding("INFY", "equity", 100000))

    assert out.decision.action == "ACCUMULATE"
    assert out.price_metrics.cagr_5y_pct is not None
    assert len(out.source_urls) == 3


def test_research_service_non_equity_is_hold():
    svc = MarketResearchService(client=StubClient())
    out = svc.analyze_holding(Holding("DEBTFUND", "debt", 50000))

    assert out.decision.action == "HOLD"
