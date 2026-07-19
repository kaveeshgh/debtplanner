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
