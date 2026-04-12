from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

AssetClass = Literal["equity", "debt", "gold", "cash"]
RiskProfile = Literal["conservative", "moderate", "growth", "aggressive"]


@dataclass(frozen=True)
class Holding:
    symbol: str
    asset_class: AssetClass
    market_value: float


@dataclass(frozen=True)
class Goal:
    name: str
    target_amount: float
    years_to_goal: int
    risk_profile: RiskProfile


@dataclass(frozen=True)
class StrategyRecommendation:
    current_value: float
    current_allocation_pct: dict[str, float]
    target_allocation_pct: dict[str, float]
    rebalance_amount: dict[str, float]
    monthly_investment_allocation_pct: dict[str, float]
    expected_annual_return_pct: float
    projected_value_at_goal: float
    on_track: bool
