def clean_money(value):
    """
    Converts strings like:
    "$20,000"
    "20,000"

    into:
    20000.0
    """
    return float(
        value
        .replace("$", "")
        .replace(",", "")
    )



def get_strategy_orders(loans):
    avalanche_order = sorted(
        range(len(loans)),
        key=lambda i: float(loans[i].interest_rate),
        reverse=True
    )

    snowball_order = sorted(
        range(len(loans)),
        key=lambda i: clean_money(loans[i].principal)
    )

    return avalanche_order, snowball_order



def build_recommendation(avalanche, snowball):

    if avalanche["total_interest"] < snowball["total_interest"]:

        return {
            "strategy": "Avalanche",
            "reason": "Saves more money by reducing interest"
        }

    elif snowball["months"] < avalanche["months"]:

        return {
            "strategy": "Snowball",
            "reason": "Pays debt off faster"
        }

    return {
        "strategy": "Tie",
        "reason": "Both strategies perform similarly"
    }

def format_currency(value):

    return f"${value:,.2f}"
