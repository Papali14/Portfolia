from __future__ import annotations

import csv
import datetime as dt
import io
import json
import math
import statistics
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass

from app.models import Holding


@dataclass(frozen=True)
class PriceMetrics:
    years_covered: float
    cagr_3y_pct: float | None
    cagr_5y_pct: float | None
    annualized_volatility_pct: float | None
    max_drawdown_pct: float | None


@dataclass(frozen=True)
class FinancialSnapshot:
    revenue_growth_pct: float | None
    gross_margins_pct: float | None
    operating_margins_pct: float | None
    debt_to_equity: float | None
    return_on_equity_pct: float | None


@dataclass(frozen=True)
class SentimentSnapshot:
    articles_considered: int
    sentiment_score: float | None


@dataclass(frozen=True)
class PositionDecision:
    action: str
    rationale: list[str]


@dataclass(frozen=True)
class SecurityResearch:
    symbol: str
    asset_class: str
    price_metrics: PriceMetrics
    financial_snapshot: FinancialSnapshot
    sentiment_snapshot: SentimentSnapshot
    decision: PositionDecision
    source_urls: list[str]
    data_quality_notes: list[str]


class MarketDataClient:
    """Network client for pulling historical prices, financial snapshot, and news headlines."""

    def fetch_daily_prices(self, symbol: str, lookback_years: int = 5) -> tuple[list[tuple[dt.date, float]], list[str]]:
        sources: list[str] = []

        # Primary: Stooq historical CSV.
        stooq_symbol = symbol.lower().replace("-", "")
        stooq_url = f"https://stooq.com/q/d/l/?s={urllib.parse.quote(stooq_symbol)}&i=d"
        try:
            with urllib.request.urlopen(stooq_url, timeout=12) as resp:
                body = resp.read().decode("utf-8", errors="ignore")
            rows = list(csv.DictReader(io.StringIO(body)))
            prices = []
            for row in rows:
                try:
                    day = dt.date.fromisoformat(row["Date"])
                    close = float(row["Close"])
                    if close > 0:
                        prices.append((day, close))
                except Exception:
                    continue
            if prices:
                cutoff = dt.date.today() - dt.timedelta(days=lookback_years * 366)
                filtered = [(d, c) for d, c in prices if d >= cutoff]
                if len(filtered) >= 240:
                    sources.append(stooq_url)
                    return filtered, sources
        except Exception:
            pass

        # Fallback: Yahoo chart API.
        end = int(dt.datetime.now(dt.timezone.utc).timestamp())
        start = int((dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=lookback_years * 366)).timestamp())
        yahoo_url = (
            "https://query1.finance.yahoo.com/v8/finance/chart/"
            f"{urllib.parse.quote(symbol)}?period1={start}&period2={end}&interval=1d"
        )
        try:
            with urllib.request.urlopen(yahoo_url, timeout=12) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
        except Exception:
            return [], sources

        result = payload.get("chart", {}).get("result") or []
        if not result:
            return [], sources

        ts = result[0].get("timestamp") or []
        closes = (((result[0].get("indicators") or {}).get("quote") or [{}])[0]).get("close") or []
        prices = []
        for t, c in zip(ts, closes):
            if c is None:
                continue
            day = dt.datetime.fromtimestamp(t, tz=dt.timezone.utc).date()
            if c > 0:
                prices.append((day, float(c)))

        if prices:
            sources.append(yahoo_url)
        return prices, sources

    def fetch_financial_snapshot(self, symbol: str) -> tuple[FinancialSnapshot, list[str], list[str]]:
        notes: list[str] = []
        sources: list[str] = []
        modules = "financialData,defaultKeyStatistics"
        url = (
            "https://query1.finance.yahoo.com/v10/finance/quoteSummary/"
            f"{urllib.parse.quote(symbol)}?modules={modules}"
        )
        try:
            with urllib.request.urlopen(url, timeout=12) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
            sources.append(url)
            result = ((payload.get("quoteSummary") or {}).get("result") or [{}])[0]
            financial_data = result.get("financialData") or {}
            key_stats = result.get("defaultKeyStatistics") or {}

            def raw(section: dict, key: str) -> float | None:
                val = section.get(key)
                if isinstance(val, dict):
                    val = val.get("raw")
                if isinstance(val, (int, float)):
                    return float(val)
                return None

            revenue_growth = raw(financial_data, "revenueGrowth")
            gross_margins = raw(financial_data, "grossMargins")
            operating_margins = raw(financial_data, "operatingMargins")
            debt_to_equity = raw(financial_data, "debtToEquity")
            roe = raw(financial_data, "returnOnEquity")

            return (
                FinancialSnapshot(
                    revenue_growth_pct=None if revenue_growth is None else revenue_growth * 100,
                    gross_margins_pct=None if gross_margins is None else gross_margins * 100,
                    operating_margins_pct=None if operating_margins is None else operating_margins * 100,
                    debt_to_equity=debt_to_equity,
                    return_on_equity_pct=None if roe is None else roe * 100,
                ),
                sources,
                notes,
            )
        except Exception:
            notes.append("Financial snapshot unavailable from provider.")
            return (
                FinancialSnapshot(None, None, None, None, None),
                sources,
                notes,
            )

    def fetch_sentiment_snapshot(self, symbol: str, max_items: int = 25) -> tuple[SentimentSnapshot, list[str], list[str]]:
        notes: list[str] = []
        sources: list[str] = []
        query = urllib.parse.quote(symbol)
        url = f"https://news.google.com/rss/search?q={query}%20stock%20OR%20mutual%20fund"
        try:
            with urllib.request.urlopen(url, timeout=12) as resp:
                xml_text = resp.read().decode("utf-8", errors="ignore")
            sources.append(url)
            root = ET.fromstring(xml_text)
            titles = []
            for item in root.findall("./channel/item")[:max_items]:
                title = item.findtext("title")
                if title:
                    titles.append(title.lower())

            if not titles:
                notes.append("No recent news headlines available for sentiment.")
                return SentimentSnapshot(0, None), sources, notes

            pos_terms = ["beat", "upgrade", "growth", "profit", "strong", "bullish", "outperform"]
            neg_terms = ["miss", "downgrade", "loss", "weak", "bearish", "fraud", "investigation"]
            total = 0
            for t in titles:
                total += sum(1 for p in pos_terms if p in t)
                total -= sum(1 for n in neg_terms if n in t)
            score = total / max(len(titles), 1)
            return SentimentSnapshot(len(titles), score), sources, notes
        except Exception:
            notes.append("Sentiment data unavailable from news provider.")
            return SentimentSnapshot(0, None), sources, notes


class MarketResearchService:
    """Runs data-backed 3Y/5Y research and position suggestions for holdings."""

    def __init__(self, client: MarketDataClient | None = None):
        self.client = client or MarketDataClient()

    def analyze_portfolio(self, holdings: list[Holding]) -> list[SecurityResearch]:
        return [self.analyze_holding(h) for h in holdings]

    def analyze_holding(self, holding: Holding) -> SecurityResearch:
        prices, price_sources = self.client.fetch_daily_prices(holding.symbol, lookback_years=5)
        price_metrics, price_notes = self._compute_price_metrics(prices)

        financial, fin_sources, fin_notes = self.client.fetch_financial_snapshot(holding.symbol)
        sentiment, sent_sources, sent_notes = self.client.fetch_sentiment_snapshot(holding.symbol)

        decision = self._decide(holding.asset_class, price_metrics, financial, sentiment)

        return SecurityResearch(
            symbol=holding.symbol,
            asset_class=holding.asset_class,
            price_metrics=price_metrics,
            financial_snapshot=financial,
            sentiment_snapshot=sentiment,
            decision=decision,
            source_urls=price_sources + fin_sources + sent_sources,
            data_quality_notes=price_notes + fin_notes + sent_notes,
        )

    def _compute_price_metrics(self, prices: list[tuple[dt.date, float]]) -> tuple[PriceMetrics, list[str]]:
        notes: list[str] = []
        if len(prices) < 240:
            notes.append("Insufficient historical price data for robust 1Y+ analysis.")
            return PriceMetrics(0.0, None, None, None, None), notes

        prices = sorted(prices, key=lambda x: x[0])
        start_day, start_price = prices[0]
        end_day, end_price = prices[-1]
        years_covered = max((end_day - start_day).days / 365.25, 0.0)

        def cagr(years: int) -> float | None:
            cutoff = end_day - dt.timedelta(days=years * 365)
            window = [p for p in prices if p[0] >= cutoff]
            if len(window) < 200:
                return None
            p0 = window[0][1]
            p1 = window[-1][1]
            elapsed = max((window[-1][0] - window[0][0]).days / 365.25, 0.001)
            return (p1 / p0) ** (1 / elapsed) - 1

        daily_returns = []
        for i in range(1, len(prices)):
            prev = prices[i - 1][1]
            curr = prices[i][1]
            if prev > 0:
                daily_returns.append((curr / prev) - 1)

        vol = None
        if len(daily_returns) > 5:
            vol = statistics.pstdev(daily_returns) * math.sqrt(252)

        peak = prices[0][1]
        max_dd = 0.0
        for _, px in prices:
            peak = max(peak, px)
            dd = (px - peak) / peak
            max_dd = min(max_dd, dd)

        return (
            PriceMetrics(
                years_covered=round(years_covered, 2),
                cagr_3y_pct=None if cagr(3) is None else round(cagr(3) * 100, 2),
                cagr_5y_pct=None if cagr(5) is None else round(cagr(5) * 100, 2),
                annualized_volatility_pct=None if vol is None else round(vol * 100, 2),
                max_drawdown_pct=round(max_dd * 100, 2),
            ),
            notes,
        )

    def _decide(
        self,
        asset_class: str,
        metrics: PriceMetrics,
        fin: FinancialSnapshot,
        sent: SentimentSnapshot,
    ) -> PositionDecision:
        rationale: list[str] = []
        if asset_class != "equity":
            rationale.append("Non-equity position: maintain strategic allocation unless goal glide path requires rebalance.")
            return PositionDecision("HOLD", rationale)

        score = 0

        if metrics.cagr_5y_pct is not None:
            rationale.append(f"5Y CAGR: {metrics.cagr_5y_pct}%")
            if metrics.cagr_5y_pct >= 12:
                score += 2
            elif metrics.cagr_5y_pct >= 8:
                score += 1
            else:
                score -= 2
        elif metrics.cagr_3y_pct is not None:
            rationale.append(f"3Y CAGR: {metrics.cagr_3y_pct}% (5Y unavailable)")
            if metrics.cagr_3y_pct >= 10:
                score += 1
            else:
                score -= 1
        else:
            rationale.append("Insufficient 3Y/5Y return history.")

        if metrics.max_drawdown_pct is not None:
            rationale.append(f"Max drawdown: {metrics.max_drawdown_pct}%")
            if metrics.max_drawdown_pct < -55:
                score -= 2
            elif metrics.max_drawdown_pct < -40:
                score -= 1

        if fin.return_on_equity_pct is not None:
            rationale.append(f"ROE: {round(fin.return_on_equity_pct, 2)}%")
            if fin.return_on_equity_pct >= 15:
                score += 1
            elif fin.return_on_equity_pct < 8:
                score -= 1

        if fin.debt_to_equity is not None:
            rationale.append(f"Debt/Equity: {round(fin.debt_to_equity, 2)}")
            if fin.debt_to_equity > 2.0:
                score -= 1

        if sent.sentiment_score is not None:
            rationale.append(f"News sentiment score: {round(sent.sentiment_score, 2)} from {sent.articles_considered} headlines")
            if sent.sentiment_score > 0.2:
                score += 1
            elif sent.sentiment_score < -0.2:
                score -= 1
        else:
            rationale.append("News sentiment unavailable.")

        if score >= 3:
            action = "ACCUMULATE"
        elif score >= 1:
            action = "HOLD"
        elif score <= -2:
            action = "REDUCE"
        else:
            action = "HOLD"

        rationale.append("No derivatives/options/trading actions are generated; this is long-term position guidance.")
        return PositionDecision(action, rationale)


def to_dict(research: SecurityResearch) -> dict:
    return asdict(research)
