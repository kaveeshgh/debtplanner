# Debt Planner
Debt Planner is a full-stack application designed to help people better understand and manage their debt. It allows users to upload or enter their loans, compare different repayment strategies, see how long it will take to become debt-free, and understand how unexpected financial changes could affect their plan.

The project uses a **React frontend** and a **Python FastAPI backend**. Python handles the financial logic, loan calculations, simulations, PDF extraction, and chart generation, while React provides the interactive interface where users can view and explore their results.

---
# Features
## Add and Analyze Loans
Users can add their loans in two different ways:
- Enter loan details manually
- Upload loan documents and automatically extract important information

The application can work with:
- Loan balance
- Interest rate
- Monthly payment
- Maturity date

---
# Debt Repayment Strategies
Debt Planner compares two of the most common repayment approaches:

## Avalanche Method
The Avalanche method focuses on paying off the highest-interest debt first.

This approach is designed to:
- Reduce the amount of interest paid over time
- Create the most cost-efficient repayment plan


## Snowball Method
The Snowball method focuses on paying off the smallest balances first.

This approach can help users:
- Eliminate smaller debts faster
- Build momentum through quick wins


The application compares both strategies and shows:
- How many months until the debt is paid off
- Total interest paid
- Which strategy is more beneficial based on the results

---
# Monte Carlo Simulation
Paying off debt is not always predictable. Unexpected expenses, income changes, and other life events can affect a repayment plan.
To account for this, Debt Planner runs **1,000 simulated repayment scenarios**.

Each simulation introduces different financial conditions, such as:
- Changes in available extra payments
- Unexpected expenses
- Income fluctuations

The results show a realistic range of outcomes:
- Best-case scenario
- Most likely scenario
- Worst-case scenario

This helps users understand how resilient their repayment plan is.

---
# Amortization Schedule
The application generates a detailed month-by-month repayment schedule.

Users can see:

- How much money goes toward interest each month
- How much reduces the loan balance
- Remaining debt over time
- Total interest accumulated

The schedule is generated with Pandas and displayed directly in the application.

---
# Data Visualization

Debt Planner creates visual reports using Python and Matplotlib.

The application generates charts showing:
- Debt balance changes over time
- Avalanche vs Snowball comparisons
- Monte Carlo payoff ranges
- Monthly interest vs principal breakdown

Charts are generated on the backend and displayed in the React interface.
