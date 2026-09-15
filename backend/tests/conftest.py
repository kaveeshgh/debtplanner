import pytest
from model import Debt


@pytest.fixture
def three_loans():
    """
    Three loans with distinct balance/rate combinations s

    Expected avalanche order (highest rate first): B (22%), A (10%), C (5%)
    Expected snowball order (smallest balance first): A (2000), C (8000), B (15000)
    """
    return [
        Debt(principal="2000", interest_rate="10", minimum_payment="100"),   # A
        Debt(principal="15000", interest_rate="22", minimum_payment="300"), # B
        Debt(principal="8000", interest_rate="5", minimum_payment="150"),   # C
    ]


@pytest.fixture
def zero_interest_loan():
    return Debt(principal="1200", interest_rate="0", minimum_payment="100")


@pytest.fixture
def negative_amortization_loan():
    #A loan whose minimum payment cannot cover its own monthly interest.
    return Debt(principal="10000", interest_rate="60", minimum_payment="50")
