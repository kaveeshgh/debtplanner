from helpers import clean_money, get_strategy_orders, build_recommendation



def test_clean_money_strips_dollar_and_comma():
    assert clean_money("$20,000") == 20000.0


def test_clean_money_handles_plain_number_string():
    assert clean_money("20000") == 20000.0


def test_clean_money_handles_decimal():
    assert clean_money("$1,234.56") == 1234.56


def test_avalanche_orders_by_highest_rate_first(three_loans):
    avalanche_order, _ = get_strategy_orders(three_loans)
    # Loan B (22%) first, then A (10%), then C (5%)
    assert avalanche_order == [1, 0, 2]


def test_snowball_orders_by_smallest_balance_first(three_loans):
    _, snowball_order = get_strategy_orders(three_loans)
    # Loan A ($2000) first, then C ($8000), then B ($15000)
    assert snowball_order == [0, 2, 1]


def test_strategy_orders_are_permutations_of_all_loan_indices(three_loans):
    avalanche_order, snowball_order = get_strategy_orders(three_loans)
    assert sorted(avalanche_order) == [0, 1, 2]
    assert sorted(snowball_order) == [0, 1, 2]


def test_recommends_avalanche_when_it_saves_more_interest():
    avalanche = {"months": 24, "total_interest": 500.0}
    snowball = {"months": 24, "total_interest": 800.0}
    result = build_recommendation(avalanche, snowball)
    assert result["strategy"] == "Avalanche"


def test_recommends_snowball_when_it_finishes_faster_and_avalanche_doesnt_save_more():
    avalanche = {"months": 30, "total_interest": 800.0}
    snowball = {"months": 24, "total_interest": 800.0}
    result = build_recommendation(avalanche, snowball)
    assert result["strategy"] == "Snowball"


def test_recommends_tie_when_results_are_identical():
    avalanche = {"months": 24, "total_interest": 800.0}
    snowball = {"months": 24, "total_interest": 800.0}
    result = build_recommendation(avalanche, snowball)
    assert result["strategy"] == "Tie"
