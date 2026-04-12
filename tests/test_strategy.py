from app.models import Goal, Holding
from app.strategy import StrategyEngine


def test_recommendation_has_all_allocations_and_projection():
    holdings = [
        Holding("EQ1", "equity", 300000),
        Holding("DB1", "debt", 200000),
        Holding("GD1", "gold", 50000),
        Holding("CS1", "cash", 50000),
    ]
    goal = Goal("Retirement", target_amount=10000000, years_to_goal=15, risk_profile="growth")

    recommendation = StrategyEngine().recommend(holdings, goal, monthly_investment=25000)

    assert recommendation.current_value == 600000
    assert set(recommendation.current_allocation_pct.keys()) == {"equity", "debt", "gold", "cash"}
    assert set(recommendation.target_allocation_pct.keys()) == {"equity", "debt", "gold", "cash"}
    assert recommendation.projected_value_at_goal > recommendation.current_value


def test_glide_path_reduces_equity_for_near_term_goals():
    engine = StrategyEngine()
    long_term = engine._target_allocation("aggressive", years_to_goal=15)
    near_term = engine._target_allocation("aggressive", years_to_goal=2)

    assert near_term["equity"] < long_term["equity"]
    assert near_term["debt"] > long_term["debt"]
