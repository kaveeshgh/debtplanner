# Imports regex module
import re

def get_loan_info(text):
    # Default
    loan = {}

    # Scans the entire text string for the first match of the pattern
    principal = re.search(r'principal amount of the Loan is \$([\d,]+\.?\d*)', text)
    # Checks the match object is not None
    if principal:
        loan['principal'] = principal.group(1)
    
    # Same as principal part
    rate = re.search(r'rate of ([\d.]+)%', text)
    if rate:
        loan['interest_rate'] = rate.group(1)

    # Same as principal part
    payment = re.search(r'monthly installments of \$([\d,]+\.?\d*)', text)
    if payment:
        loan['monthly_payment'] = payment.group(1)

    # Same as principal part
    maturity = re.search(r'due and payable on (\w+ \d+, \d+)\s*\(the\s*["\u201c\u201d]Maturity Date["\u201c\u201d]\)', text)
    if maturity:
        loan['maturity_date'] = maturity.group(1)

    return loan
