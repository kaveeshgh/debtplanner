from pydantic import BaseModel, field_validator


class Loan(BaseModel):
    principal: str
    interest_rate: str
    monthly_payment: str
    maturity_date: str = ""

    @field_validator("principal")
    @classmethod
    def validate_principal(cls, value):
        clean = value.replace(",", "").replace("$", "")

        if float(clean) <= 0:
            raise ValueError("Principal must be greater than zero")

        return value


    @field_validator("interest_rate")
    @classmethod
    def validate_interest_rate(cls, value):
        rate = float(value.replace("%", ""))

        if rate < 0:
            raise ValueError("Interest rate cannot be negative")

        return value


    @field_validator("monthly_payment")
    @classmethod
    def validate_payment(cls, value):
        clean = value.replace(",", "").replace("$", "")

        if float(clean) <= 0:
            raise ValueError("Monthly payment must be greater than zero")

        return value



class OptimizeRequest(BaseModel):
    loans: list[Loan]
    extra_payment: float = 100
    