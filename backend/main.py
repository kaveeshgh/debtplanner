# Imports route handling tools
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pdfplumber
import io


# Imports from modules
from model import Loan, OptimizeRequest
from pdf import get_loan_info
from simulate import (
    simulate_payoff,
    simulate_payoff_monte_carlo,
    simulate_payoff_timeline,
    build_amortization_schedule
)
from charts import (
    generate_balance_chart,
    generate_monte_carlo_chart,
    generate_schedule_chart
)

# Creates the application instance
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# A backend health check
@app.get("/")
def read_root():
    return {"message": "Debt Planner API is running!"}



@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    contents = await file.read()

    with pdfplumber.open(io.BytesIO(contents)) as pdf:
        # Loops through every page and concatenates all extracted text into one big string
        text = ""
        for page in pdf.pages:
            text += page.extract_text()

    # Runs regex extraction and returns both the structured data and raw text
    loan_info = get_loan_info(text)
    return {"loan": loan_info, "raw_text": text}



@app.post("/optimize")
async def optimize(request: OptimizeRequest):
    loans = request.loans
    extra = request.extra_payment

    avalanche_order = sorted(range(len(loans)), key=lambda i: float(loans[i].interest_rate), reverse=True)
    snowball_order = sorted(range(len(loans)), key=lambda i: float(loans[i].principal.replace(",", "")))

    # Runs the simulation twice with different orderings and returns both results as a dict
    return {
        "avalanche": simulate_payoff(loans, avalanche_order, extra),
        "snowball": simulate_payoff(loans, snowball_order, extra)
    }



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

    return {
        "avalanche": simulate_payoff_monte_carlo(loans, avalanche_order, extra),
        "snowball": simulate_payoff_monte_carlo(loans, snowball_order, extra)
    }



@app.post("/schedule")
async def schedule(request: OptimizeRequest):
    loans = request.loans
    extra = request.extra_payment

    avalanche_order = sorted(range(len(loans)), key=lambda i: float(loans[i].interest_rate), reverse=True)
    df = build_amortization_schedule(loans, avalanche_order, extra)

    summary = {
        "total_months": int(df["month"].max()),
        "total_interest_paid": round(float(df["total_interest"].sum()), 2),
        "total_principal_paid": round(float(df["total_principal"].sum()), 2),
    }

    return {"schedule": df.to_dict(orient="records"), "summary": summary}



@app.post("/analyze/optimize")
async def analyze_optimize(request: OptimizeRequest):
    loans = request.loans
    extra = request.extra_payment

    avalanche_order = sorted(range(len(loans)), key=lambda i: float(loans[i].interest_rate), reverse=True)
    snowball_order  = sorted(range(len(loans)), key=lambda i: float(loans[i].principal.replace(",", "")))

    # run optimization stats
    avalanche_result = simulate_payoff(loans, avalanche_order, extra)
    snowball_result  = simulate_payoff(loans, snowball_order, extra)

    # run timeline simulations needed for the chart
    avalanche_timeline = simulate_payoff_timeline(loans, avalanche_order, extra)
    snowball_timeline  = simulate_payoff_timeline(loans, snowball_order, extra)

    # generate chart in Python — sends back as base64 image
    chart = generate_balance_chart(avalanche_timeline, snowball_timeline)

    return {
        "avalanche": avalanche_result,
        "snowball":  snowball_result,
        "chart":     chart
    }



@app.post("/analyze/monte-carlo")
async def analyze_monte_carlo(request: OptimizeRequest):
    loans = request.loans
    extra = request.extra_payment

    avalanche_order = sorted(range(len(loans)), key=lambda i: float(loans[i].interest_rate), reverse=True)
    snowball_order  = sorted(range(len(loans)), key=lambda i: float(loans[i].principal.replace(",", "")))

    # run Monte Carlo for both strategies
    avalanche_mc = simulate_payoff_monte_carlo(loans, avalanche_order, extra)
    snowball_mc  = simulate_payoff_monte_carlo(loans, snowball_order,  extra)

    mc_results = {
        "avalanche": avalanche_mc,
        "snowball":  snowball_mc
    }

    # generate chart from mc results
    chart = generate_monte_carlo_chart(mc_results)

    return {
        "avalanche": avalanche_mc,
        "snowball":  snowball_mc,
        "chart":     chart
    }



@app.post("/analyze/schedule")
async def analyze_schedule(request: OptimizeRequest):
    loans = request.loans
    extra = request.extra_payment

    avalanche_order = sorted(range(len(loans)), key=lambda i: float(loans[i].interest_rate), reverse=True)

    # build pandas dataframe
    df = build_amortization_schedule(loans, avalanche_order, extra)

    # pandas summary stats
    summary = {
        "total_months":         int(df["month"].max()),
        "total_interest_paid":  round(float(df["total_interest"].sum()), 2),
        "total_principal_paid": round(float(df["total_principal"].sum()), 2),
    }

    # generate chart from dataframe
    chart = generate_schedule_chart(df)

    return {
        "schedule": df.to_dict(orient="records"),
        "summary":  summary,
        "chart":    chart
    }
