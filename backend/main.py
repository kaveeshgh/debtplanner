from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pdfplumber
import io

from model import OptimizeRequest
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

from helpers import (
    get_strategy_orders,
    build_recommendation
)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
def read_root():
    return {
        "message": "Debt Planner API is running!"
    }



@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    contents = await file.read()

    with pdfplumber.open(io.BytesIO(contents)) as pdf:

        text = ""

        for page in pdf.pages:
            extracted = page.extract_text()

            if extracted:
                text += extracted

    loan_info = get_loan_info(text)

    return {
        "loan": loan_info,
        "raw_text": text
    }



@app.post("/optimize")
async def optimize(request: OptimizeRequest):
    loans = request.loans
    extra = request.extra_payment

    avalanche_order, snowball_order = get_strategy_orders(loans)

    avalanche = simulate_payoff(
        loans,
        avalanche_order,
        extra
    )

    snowball = simulate_payoff(
        loans,
        snowball_order,
        extra
    )

    return {
        "avalanche": avalanche,
        "snowball": snowball,
        "recommendation": build_recommendation(
            avalanche,
            snowball
        )
    }



@app.post("/timeline")
async def timeline(request: OptimizeRequest):
    loans = request.loans
    extra = request.extra_payment

    avalanche_order, snowball_order = get_strategy_orders(loans)

    return {
        "avalanche":
            simulate_payoff_timeline(
                loans,
                avalanche_order,
                extra
            ),

        "snowball":
            simulate_payoff_timeline(
                loans,
                snowball_order,
                extra
            )
    }



@app.post("/monte-carlo")
async def monte_carlo(request: OptimizeRequest):
    loans = request.loans
    extra = request.extra_payment

    avalanche_order, snowball_order = get_strategy_orders(loans)

    return {
        "avalanche":
            simulate_payoff_monte_carlo(
                loans,
                avalanche_order,
                extra
            ),

        "snowball":
            simulate_payoff_monte_carlo(
                loans,
                snowball_order,
                extra
            )
    }


@app.post("/schedule")
async def schedule(request: OptimizeRequest):
    loans = request.loans
    extra = request.extra_payment

    avalanche_order, _ = get_strategy_orders(loans)

    df = build_amortization_schedule(
        loans,
        avalanche_order,
        extra
    )


    summary = {
        "total_months":
            int(df["month"].max()),

        "total_interest_paid":
            round(
                float(df["total_interest"].sum()),
                2
            ),

        "total_principal_paid":
            round(
                float(df["total_principal"].sum()),
                2
            )
    }

    return {
        "schedule":
            df.to_dict(
                orient="records"
            ),

        "summary":
            summary
    }


@app.post("/analyze/optimize")
async def analyze_optimize(request: OptimizeRequest):
    loans = request.loans
    extra = request.extra_payment

    avalanche_order, snowball_order = get_strategy_orders(loans)

    avalanche = simulate_payoff(
        loans,
        avalanche_order,
        extra
    )

    snowball = simulate_payoff(
        loans,
        snowball_order,
        extra
    )

    avalanche_timeline = simulate_payoff_timeline(
        loans,
        avalanche_order,
        extra
    )

    snowball_timeline = simulate_payoff_timeline(
        loans,
        snowball_order,
        extra
    )

    chart = generate_balance_chart(
        avalanche_timeline,
        snowball_timeline
    )


    return {
        "avalanche":
            avalanche,

        "snowball":
            snowball,

        "recommendation":
            build_recommendation(
                avalanche,
                snowball
            ),

        "chart":
            chart
    }



@app.post("/analyze/monte-carlo")
async def analyze_monte_carlo(request: OptimizeRequest):
    loans = request.loans
    extra = request.extra_payment

    avalanche_order, snowball_order = get_strategy_orders(loans)

    avalanche_mc = simulate_payoff_monte_carlo(
        loans,
        avalanche_order,
        extra
    )

    snowball_mc = simulate_payoff_monte_carlo(
        loans,
        snowball_order,
        extra
    )

    results = {
        "avalanche":
            avalanche_mc,

        "snowball":
            snowball_mc
    }

    chart = generate_monte_carlo_chart(results)

    return {
        **results,

        "chart":
            chart
    }



@app.post("/analyze/schedule")
async def analyze_schedule(request: OptimizeRequest):
    loans = request.loans
    extra = request.extra_payment

    avalanche_order, _ = get_strategy_orders(loans)

    df = build_amortization_schedule(
        loans,
        avalanche_order,
        extra
    )

    summary = {
        "total_months":
            int(df["month"].max()),

        "total_interest_paid":
            round(
                float(df["total_interest"].sum()),
                2
            ),

        "total_principal_paid":
            round(
                float(df["total_principal"].sum()),
                2
            )
    }

    chart = generate_schedule_chart(df)

    return {
        "schedule":
            df.to_dict(
                orient="records"
            ),
        "summary":
            summary,
        "chart":
            chart
    }
