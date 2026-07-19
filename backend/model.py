# Imports BaseModel from Pydantic
from pydantic import BaseModel

# Defines the shape of a Loan object
class Loan(BaseModel):
    principal: str
    interest_rate: str
    monthly_payment: str
    maturity_date: str

# The shape of the request body for optimize/monte-carlo/timeline/schedule endpoints
class OptimizeRequest(BaseModel):
    loans: list[Loan]
    extra_payment: float = 0
    