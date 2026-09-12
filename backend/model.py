from pydantic import BaseModel, field_validator
from helpers import clean_money

class Debt(BaseModel):
    name: str = ""
    type: str = ""
    principal: str
    interest_rate: str
    minimum_payment: str

    @field_validator("principal")
    @classmethod
    def validate_principal(cls, value):
        clean = clean_money(value)

        if float(clean) <= 0:
            raise ValueError("Principal must be greater than zero")

        return value


    @field_validator("interest_rate")
    @classmethod
    def validate_interest_rate(cls, value):
        rate = clean_money(value)

        if rate < 0:
            raise ValueError("Interest rate cannot be negative")

        return value


    @field_validator("minimum_payment")
    @classmethod
    def validate_payment(cls, value):
        clean = clean_money(value)

        if float(clean) <= 0:
            raise ValueError("Minimum payment must be greater than zero")

        return value



class OptimizeRequest(BaseModel):
    loans: list[Debt]
    extra_payment: float = 100
    