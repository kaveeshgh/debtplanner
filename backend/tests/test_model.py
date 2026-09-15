import pytest
from pydantic import ValidationError

from model import Debt, OptimizeRequest


def test_valid_debt_constructs():
    debt = Debt(principal="20000", interest_rate="5.5", minimum_payment="400")
    assert debt.principal == "20000"
    assert debt.interest_rate == "5.5"
    assert debt.minimum_payment == "400"

@pytest.mark.parametrize("bad_principal", ["0", "-500", "-0.01"])
def test_zero_or_negative_principal_rejected(bad_principal):
    with pytest.raises(ValidationError):
        Debt(principal=bad_principal, interest_rate="5", minimum_payment="100")


def test_negative_interest_rate_rejected():
    with pytest.raises(ValidationError):
        Debt(principal="1000", interest_rate="-1", minimum_payment="100")


def test_zero_interest_rate_is_allowed():
    """0% is a legitimate rate (e.g. promotional periods) -- must not be rejected."""
    debt = Debt(principal="1000", interest_rate="0", minimum_payment="100")
    assert debt.interest_rate == "0"


@pytest.mark.parametrize("bad_payment", ["0", "-100"])
def test_zero_or_negative_minimum_payment_rejected(bad_payment):
    with pytest.raises(ValidationError):
        Debt(principal="1000", interest_rate="5", minimum_payment=bad_payment)


def test_optimize_request_extra_payment_defaults_to_100():
    req = OptimizeRequest(loans=[
        Debt(principal="1000", interest_rate="5", minimum_payment="100")
    ])
    assert req.extra_payment == 100


def test_optimize_request_honors_explicit_extra_payment():
    req = OptimizeRequest(
        loans=[Debt(principal="1000", interest_rate="5", minimum_payment="100")],
        extra_payment=250,
    )
    assert req.extra_payment == 250
