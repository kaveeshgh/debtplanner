from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pdfplumber
import io
import re
import random
from pydantic import BaseModel


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite's default port
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Debt Planner API is running!"}




def get_loan_info(text):
    loan = {}


    # principal amount
    principal = re.search(r'principal amount of the Loan is \$([\d,]+\.?\d*)', text)
    if principal:
        loan['principal'] = principal.group(1)


    # interest rate
    rate = re.search(r'rate of ([\d.]+)%', text)
    if rate:
        loan['interest_rate'] = rate.group(1)


    # monthly payment
    payment = re.search(r'monthly installments of \$([\d,]+\.?\d*)', text)
    if payment:
        loan['monthly_payment'] = payment.group(1)


    # maturity date
    maturity = re.search(r'due and payable on (\w+ \d+, \d+)\s*\(the\s*["\u201c\u201d]Maturity Date["\u201c\u201d]\)', text)
    if maturity:
        loan['maturity_date'] = maturity.group(1)


    return loan


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    contents = await file.read()


    with pdfplumber.open(io.BytesIO(contents)) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()


    loan_info = get_loan_info(text);
    return {"loan": loan_info , "raw_text": text}




class Loan(BaseModel):
    principal: str
    interest_rate: str
    monthly_payment: str
    maturity_date: str


class OptimizeRequest(BaseModel):
    loans: list[Loan]
    extra_payment: float = 0  # incase extra money can be added


def simulate_payoff(loans, order, extra_payment):
    balances = [float(l.principal.replace(",", "")) for l in loans]
    rates = [float(l.interest_rate) / 100 / 12 for l in loans]  
    min_payments = [float(l.monthly_payment.replace(",", "")) for l in loans]

    months = 0
    total_interest = 0

    while sum(balances) > 0 and months < 600:  # 600 month safety cap
        months += 1
        leftover_extra = extra_payment

        # pay minimums + accrue interest on every loan
        for i in order:
            if balances[i] <= 0:
                continue
            interest = balances[i] * rates[i]
            total_interest += interest
            balances[i] += interest
            payment = min(min_payments[i], balances[i])
            balances[i] -= payment

        # dump all extra money into the priority loan (avalanche or snowball order)
        for i in order:
            if balances[i] <= 0:
                continue
            pay = min(leftover_extra, balances[i])
            balances[i] -= pay
            leftover_extra -= pay
            if leftover_extra <= 0:
                break

    return {"months": months, "total_interest": round(total_interest, 2)}

def simulate_payoff_monte_carlo(loans, order, extra_payment, trials=1000):
    payoff_months = []

    for _ in range(trials):
        balances = [float(l.principal.replace(",", "")) for l in loans]
        rates = [float(l.interest_rate) / 100 / 12 for l in loans]
        min_payments = [float(l.monthly_payment.replace(",", "")) for l in loans]

        months = 0

        while sum(balances) > 0 and months < 600:
            months += 1

            # randomize the extra payment each month to simulate real life
            income_factor = random.uniform(0.85, 1.15)  # income can swing +-15%
            this_month_extra = extra_payment * income_factor

            # occasionally a surprise expense eats into the extra payment
            if random.random() < 0.1:  # 10% chance each month
                shock = random.uniform(100, 800)
                this_month_extra = max(0, this_month_extra - shock)

            leftover_extra = this_month_extra

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

        payoff_months.append(months)

    payoff_months.sort()
    n = len(payoff_months)

    return {
        "best_case": payoff_months[int(n * 0.10)],   # 10th percentile
        "median": payoff_months[int(n * 0.50)],
        "worst_case": payoff_months[int(n * 0.90)],  # 90th percentile
    }

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

        timeline.append({"month": months, "balance": round(sum(balances), 2)})

    return timeline


@app.post("/timeline")
async def timeline(request: OptimizeRequest):
    loans = request.loans
    extra = request.extra_payment

    avalanche_order = sorted(range(len(loans)), key=lambda i: float(loans[i].interest_rate), reverse=True)
    snowball_order = sorted(range(len(loans)), key=lambda i: float(loans[i].principal.replace(",", "")))

    return {
        "avalanche": simulate_payoff_timeline(loans, avalanche_order, extra),
        "snowball": simulate_payoff_timeline(loans, snowball_order, extra)
}

@app.post("/monte-carlo")
async def monte_carlo(request: OptimizeRequest):
    loans = request.loans
    extra = request.extra_payment

    avalanche_order = sorted(range(len(loans)), key=lambda i: float(loans[i].interest_rate), reverse=True)
    snowball_order = sorted(range(len(loans)), key=lambda i: float(loans[i].principal.replace(",", "")))

    results = {
        "avalanche": simulate_payoff_monte_carlo(loans, avalanche_order, extra),
        "snowball": simulate_payoff_monte_carlo(loans, snowball_order, extra)
    }

    return results


@app.post("/optimize")
async def optimize(request: OptimizeRequest):
    loans = request.loans
    extra = request.extra_payment

    # avalanche = highest interest rate first
    avalanche_order = sorted(range(len(loans)), key=lambda i: float(loans[i].interest_rate), reverse=True)

    # snowball = smallest balance first
    snowball_order = sorted(range(len(loans)), key=lambda i: float(loans[i].principal.replace(",", "")))

    results = {
        "avalanche": simulate_payoff(loans, avalanche_order, extra),
        "snowball": simulate_payoff(loans, snowball_order, extra)
    }

    return results
