# Imports NumPy and Pandas
import numpy as np
import pandas as pd


def simulate_payoff(loans, order, extra_payment):
    # For every loan, strip commas from the principal string then convert to float
    balances = [float(l.principal.replace(",", "")) for l in loans]
    # Converts annual percentage to monthly decimal rate
    rates = [float(l.interest_rate) / 100 / 12 for l in loans]
    # Same as balances
    min_payments = [float(l.monthly_payment.replace(",", "")) for l in loans]

    # Counters
    months = 0
    total_interest = 0

    # Loops until total debt hits zero or we've hit 50 years
    while sum(balances) > 0 and months < 600:
        # Incerment, reset extra payment pool
        months += 1
        leftover_extra = extra_payment
        
        # Loops through loans and skips already-paid loans
        for i in order:
            if balances[i] <= 0:
                continue

            # Calculates this month's interest, adds it to the running total, and adds it to the balance
            interest = balances[i] * rates[i]
            total_interest += interest
            balances[i] += interest

            payment = min(min_payments[i], balances[i])
            balances[i] -= payment

        # Second loop to dump extra money into loans in priority order
        for i in order:
            if balances[i] <= 0:
                continue
            pay = min(leftover_extra, balances[i])
            balances[i] -= pay
            leftover_extra -= pay

            # Stops once all extra money is spent
            if leftover_extra <= 0:
                break
    
    # Returns final results
    return {"months": months, "total_interest": round(total_interest, 2)}



def simulate_payoff_monte_carlo(loans, order, extra_payment, trials=1000):
    # Same extraction as simulate_payoff but wrapped in np.array()
    # Converts Python lists to NumPy arrays
    balances_init = np.array([float(l.principal.replace(",", "")) for l in loans])
    rates = np.array([float(l.interest_rate) / 100 / 12 for l in loans])
    min_payments = np.array([float(l.monthly_payment.replace(",", "")) for l in loans])

    # Every row is one trial, every column is one loan
    balances = np.tile(balances_init, (trials, 1))
    # Creates an array of 1000 values
    payoff_months = np.full(trials, 600)

    
    for month in range(1, 601):
        # Gives a 1D array of total remaining debt per trial
        active = np.sum(balances, axis=1) > 0
        # If all trials finished, stop the loop
        if not np.any(active):
            break
        
        # Generates 1000 random numbers between 0.85 and 1.15 simultaneously (1 per trial)
        income_factors = np.random.uniform(0.85, 1.15, size=trials)
        # Multiplies the extra payment by each trial's income factor
        this_month_extra = extra_payment * income_factors

        # Gives a boolean array where True(10% of the time) means a shock event happens this month for that trial
        shocks = np.random.random(trials) < 0.10
        shock_amounts = np.random.uniform(100, 800, size=trials)
        this_month_extra = np.maximum(0, this_month_extra - shocks * shock_amounts)
        

        # Every operation applies to all trials simultaneously
        for i in order:
            interest = balances[:, i] * rates[i]
            balances[:, i] += interest
            payment = np.minimum(min_payments[i], balances[:, i])
            balances[:, i] -= payment

        leftover = this_month_extra.copy()
        for i in order:
            pay = np.minimum(leftover, balances[:, i])
            balances[:, i] -= pay
            leftover -= pay
            leftover = np.maximum(leftover, 0)


        # Finds trials that completed exactly this month and records their payoff month
        just_finished = active & (np.sum(balances, axis=1) <= 0)
        payoff_months[just_finished] = month

    # Sorts all 1000 payoff times and converts NumPy integers to Python integers
    payoff_months_sorted = np.sort(payoff_months)
    n = trials

    return {
        "best_case": int(payoff_months_sorted[int(n * 0.10)]),
        "median": int(payoff_months_sorted[int(n * 0.50)]),
        "worst_case": int(payoff_months_sorted[int(n * 0.90)]),
    }



# Basically same as simulate_payoff except instead of just tracking totals, it records a snapshot every month
def simulate_payoff_timeline(loans, order, extra_payment):
    balances = [float(l.principal.replace(",", "")) for l in loans]
    rates = [float(l.interest_rate) / 100 / 12 for l in loans]
    min_payments = [float(l.monthly_payment.replace(",", "")) for l in loans]

    timeline = []
    months = 0

    while sum(balances) > 0 and months < 600:
        months += 1
        leftover_extra = extra_payment

        for i in order:
            if balances[i] <= 0:
                continue
            interest = balances[i] * rates[i]
            balances[i] += interest
            payment = min(min_payments[i], balances[i])
            balances[i] -= payment

        for i in order:
            if balances[i] <= 0:
                continue
            pay = min(leftover_extra, balances[i])
            balances[i] -= pay
            leftover_extra -= pay
            if leftover_extra <= 0:
                break
        
        # After each month's payments, records the total remaining balance across all loans.
        timeline.append({"month": months, "balance": round(sum(balances), 2)})

    return timeline



# Tracks every loan individually each month
def build_amortization_schedule(loans, order, extra_payment):
    balances = [float(l.principal.replace(",", "")) for l in loans]
    rates = [float(l.interest_rate) / 100 / 12 for l in loans]
    min_payments = [float(l.monthly_payment.replace(",", "")) for l in loans]
    names = [f"Loan {i+1}" for i in range(len(loans))]

    # Each element is one month's data
    rows = []
    months = 0


    while sum(balances) > 0 and months < 600:
        months += 1
        leftover_extra = extra_payment

        # Starts a new row dict and running totals for this month
        row = {"month": months}
        total_interest_this_month = 0
        total_principal_this_month = 0

        for i in order:
            if balances[i] <= 0:
                row[f"{names[i]}_balance"] = 0.0
                row[f"{names[i]}_interest"] = 0.0
                row[f"{names[i]}_principal"] = 0.0
                continue

            interest = balances[i] * rates[i]
            balances[i] += interest
            payment = min(min_payments[i], balances[i])
            principal_paid = payment - interest
            balances[i] -= payment

            row[f"{names[i]}_balance"] = round(balances[i], 2)
            row[f"{names[i]}_interest"] = round(interest, 2)
            row[f"{names[i]}_principal"] = round(principal_paid, 2)

            total_interest_this_month += interest
            total_principal_this_month += principal_paid


        for i in order:
            if balances[i] <= 0:
                continue

            pay = min(leftover_extra, balances[i])
            balances[i] -= pay
            leftover_extra -= pay
            total_principal_this_month += pay
            
            row[f"{names[i]}_balance"] = round(balances[i], 2)
            if leftover_extra <= 0:
                break

        row["total_balance"] = round(sum(b for b in balances), 2)
        row["total_interest"] = round(total_interest_this_month, 2)
        row["total_principal"] = round(total_principal_this_month, 2)
        rows.append(row)

    # Converts the list of dicts into a Pandas DataFrame
    df = pd.DataFrame(rows)
    # Computes a running total
    # Each cell contains the sum of all values up to and including that row
    df["cumulative_interest"] = df["total_interest"].cumsum().round(2)

    return df
