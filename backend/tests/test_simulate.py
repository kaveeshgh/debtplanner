from simulate import simulate_payoff, simulate_payoff_monte_carlo, build_amortization_schedule


def test_zero_interest_loan_payoff_matches_hand_calculation(zero_interest_loan):
    """
    $1200 principal, 0% interest, $100/month minimum, no extra payment.
    With zero interest, this is pure division: 1200 / 100 = exactly 12 months,
    and total interest must be exactly 0.
    """
    result = simulate_payoff([zero_interest_loan], order=[0], extra_payment=0)
    assert result["months"] == 12
    assert result["total_interest"] == 0.0


def test_extra_payment_shortens_payoff(zero_interest_loan):
    baseline = simulate_payoff([zero_interest_loan], order=[0], extra_payment=0)
    with_extra = simulate_payoff([zero_interest_loan], order=[0], extra_payment=100)
    assert with_extra["months"] < baseline["months"]
    assert with_extra["months"] == 6


def test_negative_amortization_hits_600_month_cap(negative_amortization_loan):
    result = simulate_payoff([negative_amortization_loan], order=[0], extra_payment=0)
    assert result["months"] == 600


def test_monte_carlo_percentiles_are_ordered(zero_interest_loan):
    """
    Regardless of randomness, best_case(10th percentile) should never be
    slower than median(50th), and median should never be slower than
    worst_case(90th)
    """
    result = simulate_payoff_monte_carlo(
        [zero_interest_loan], order=[0], extra_payment=50, trials=200
    )
    assert result["best_case"] <= result["median"] <= result["worst_case"]


def test_monte_carlo_returns_expected_keys(zero_interest_loan):
    result = simulate_payoff_monte_carlo(
        [zero_interest_loan], order=[0], extra_payment=50, trials=50
    )
    assert set(result.keys()) == {"best_case", "median", "worst_case"}


def test_schedule_cumulative_interest_is_non_decreasing(three_loans):
    from helpers import get_strategy_orders
    avalanche_order, _ = get_strategy_orders(three_loans)
    df = build_amortization_schedule(three_loans, avalanche_order, extra_payment=100)

    cumulative = df["cumulative_interest"].tolist()
    assert all(b >= a for a, b in zip(cumulative, cumulative[1:]))


def test_schedule_ends_with_zero_total_balance_or_hits_cap(three_loans):
    from helpers import get_strategy_orders
    avalanche_order, _ = get_strategy_orders(three_loans)
    df = build_amortization_schedule(three_loans, avalanche_order, extra_payment=100)

    final_balance = df["total_balance"].iloc[-1]
    final_month = df["month"].iloc[-1]
    assert final_balance == 0.0 or final_month == 600
