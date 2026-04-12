from __future__ import annotations

from app.models import Goal, Holding, RiskProfile, StrategyRecommendation

EXPECTED_RETURNS = {
    "equity": 0.12,
    "debt": 0.07,
    "gold": 0.06,
    "cash": 0.04,
}

BASE_RISK_ALLOCATIONS: dict[RiskProfile, dict[str, float]] = {
    "conservative": {"equity": 0.25, "debt": 0.55, "gold": 0.10, "cash": 0.10},
    "moderate": {"equity": 0.45, "debt": 0.35, "gold": 0.10, "cash": 0.10},
    "growth": {"equity": 0.60, "debt": 0.25, "gold": 0.10, "cash": 0.05},
    "aggressive": {"equity": 0.75, "debt": 0.15, "gold": 0.05, "cash": 0.05},
}


class StrategyEngine:
    def recommend(
        self,
        holdings: list[Holding],
        goal: Goal,
        monthly_investment: float,
    ) -> StrategyRecommendation:
        total_value = sum(h.market_value for h in holdings)
        if total_value <= 0:
            raise ValueError("Portfolio value must be positive.")

        current_alloc = self._current_allocation_pct(holdings, total_value)
        target_alloc = self._target_allocation(goal.risk_profile, goal.years_to_goal)

        rebalance = {
            k: round((target_alloc[k] - current_alloc.get(k, 0.0)) * total_value, 2)
            for k in target_alloc
        }

        positive_gaps = {
            k: max(0.0, target_alloc[k] - current_alloc.get(k, 0.0)) for k in target_alloc
        }
        gap_total = sum(positive_gaps.values())
        if gap_total == 0:
            sip_alloc = target_alloc.copy()
        else:
            sip_alloc = {k: v / gap_total for k, v in positive_gaps.items()}

        expected_return = sum(target_alloc[k] * EXPECTED_RETURNS[k] for k in target_alloc)
        projected_value = self._project_future_value(
            current_value=total_value,
            years=goal.years_to_goal,
            annual_return=expected_return,
            monthly_contribution=monthly_investment,
        )

        return StrategyRecommendation(
            current_value=round(total_value, 2),
            current_allocation_pct={k: round(v * 100, 2) for k, v in current_alloc.items()},
            target_allocation_pct={k: round(v * 100, 2) for k, v in target_alloc.items()},
            rebalance_amount=rebalance,
            monthly_investment_allocation_pct={k: round(v * 100, 2) for k, v in sip_alloc.items()},
            expected_annual_return_pct=round(expected_return * 100, 2),
            projected_value_at_goal=round(projected_value, 2),
            on_track=projected_value >= goal.target_amount,
        )

    def _current_allocation_pct(
        self,
        holdings: list[Holding],
        total_value: float,
    ) -> dict[str, float]:
        alloc = {"equity": 0.0, "debt": 0.0, "gold": 0.0, "cash": 0.0}
        for h in holdings:
            alloc[h.asset_class] += h.market_value

        return {k: v / total_value for k, v in alloc.items()}

    def _target_allocation(self, risk_profile: RiskProfile, years_to_goal: int) -> dict[str, float]:
        target = BASE_RISK_ALLOCATIONS[risk_profile].copy()

        # Glide path: shift equity to debt as the goal gets near.
        if years_to_goal <= 3:
            shift = min(0.15, target["equity"])
            target["equity"] -= shift
            target["debt"] += shift
        elif years_to_goal <= 7:
            shift = min(0.08, target["equity"])
            target["equity"] -= shift
            target["debt"] += shift

        # Normalize in case of future rule changes.
        s = sum(target.values())
        return {k: v / s for k, v in target.items()}

    def _project_future_value(
        self,
        current_value: float,
        years: int,
        annual_return: float,
        monthly_contribution: float,
    ) -> float:
        monthly_rate = annual_return / 12
        months = years * 12

        fv_lumpsum = current_value * (1 + monthly_rate) ** months
        if monthly_rate == 0:
            fv_sip = monthly_contribution * months
        else:
            fv_sip = monthly_contribution * (((1 + monthly_rate) ** months - 1) / monthly_rate)

        return fv_lumpsum + fv_sip
