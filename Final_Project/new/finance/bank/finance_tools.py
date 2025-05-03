
#  --------------------------------------------------1 --------------------------------
def calculate_emi(principal, annual_rate, tenure_years):

    if principal <= 0 or annual_rate < 0 or tenure_years <= 0:
        raise ValueError("Principal, annual rate, and tenure must be positive and greater than zero.")
    monthly_rate = annual_rate / (12 * 100)
    tenure_months = tenure_years * 12

    if monthly_rate == 0:
        emi = principal / tenure_months
    else:
        emi = (principal * monthly_rate * (1 + monthly_rate) ** tenure_months) / \
              ((1 + monthly_rate) ** tenure_months - 1)

    return max(emi, 0)

#  --------------------------------------------------2 --------------------------------
def calculate_sip(monthly_investment, annual_rate, years):

    if monthly_investment <= 0 or annual_rate < 0 or years <= 0:
        raise ValueError("Inputs must be positive and annual rate non-negative.")
    r = annual_rate / (12 * 100)
    n = years * 12
    fv = monthly_investment * (((1 + r) ** n - 1) / r) * (1 + r)
    return round(fv, 2)

# --------------------------------------------------3 --------------------------------
def calculate_fd(principal, annual_rate, years, compounding_frequency=4):

    if principal <= 0 or annual_rate < 0 or years <= 0 or compounding_frequency <= 0:
        raise ValueError("Inputs must be positive, and interest rate must be non-negative.")
    r = annual_rate / 100
    n = compounding_frequency
    t = years
    maturity_amount = principal * (1 + r / n) ** (n * t)
    interest_earned = maturity_amount - principal
    return round(maturity_amount, 2), round(interest_earned, 2)

# --------------------------------------------------4 --------------------------------
def calculate_rd(monthly_deposit, annual_rate, years):

    if monthly_deposit <= 0 or annual_rate < 0 or years <= 0:
        raise ValueError("All inputs must be positive, and interest rate must be non-negative.")

    n = years * 12
    r = annual_rate / 400
    maturity_value = monthly_deposit * (((1 + r) ** n - 1) / (1 - (1 + r) ** -1))
    return round(maturity_value, 2)

#--------------------------------------------------5--------------------------------

def estimate_retirement(current_savings, monthly_contribution, annual_return, years):

    if current_savings < 0 or monthly_contribution < 0 or annual_return < 0 or years <= 0:
        raise ValueError("All inputs must be non-negative, and years must be positive.")
    r = annual_return / 12 / 100
    n = years * 12
    fv_sip = monthly_contribution * (((1 + r) ** n - 1) / r) * (1 + r)
    fv_lump = current_savings * ((1 + r) ** n)
    total_corpus = round(fv_sip + fv_lump, 2)
    total_invested = current_savings + (monthly_contribution * n)
    total_interest = round(total_corpus - total_invested, 2)

    return float(total_corpus), float(total_invested), float(total_interest)

# #  --------------------------------------------------6--------------------------------
def calculate_home_loan_eligibility(monthly_income, monthly_expenses, loan_term_years, interest_rate):

    if monthly_income < 0 or monthly_expenses < 0 or loan_term_years <= 0 or interest_rate < 0:
        raise ValueError("Inputs must be non-negative, and loan term must be greater than zero.")

    disposable_income = monthly_income - monthly_expenses
    if disposable_income <= 0:
        return 0.0  # No eligibility
    eligible_emi = monthly_income * 0.50 - monthly_expenses
    loan_term_months = loan_term_years * 12
    r = interest_rate / 12 / 100
    emi = eligible_emi
    if r == 0:
        loan_amount = emi * loan_term_months
    else:
        loan_amount = emi * ((1 + r) ** loan_term_months - 1) / (r * (1 + r) ** loan_term_months)

    loan_amount = round(loan_amount, 2)  # Round to 2 decimal places
    return loan_amount# #  --------------------------------------------------7 --------------------------------

def calculate_credit_card_balance(initial_balance, interest_rate, min_payment, months):

    if not all(isinstance(val, (int, float)) for val in [initial_balance, interest_rate, min_payment, months]):
        raise TypeError("All inputs must be numbers (int or float).")
    if initial_balance <= 0 or interest_rate <= 0 or min_payment <= 0 or months <= 0:
        raise ValueError("All inputs must be positive numbers.")

    balance = initial_balance
    monthly_interest_rate = interest_rate / 12 / 100  # Convert annual rate to monthly

    for month in range(months):

        balance += balance * monthly_interest_rate
        balance -= min_payment
        if balance < 0:
            balance = 0
            break
    
    return round(balance, 2)

# #  --------------------------------------------------8 --------------------------------
def calculate_taxable_income(gross_income, deductions):


    STANDARD_DEDUCTION = 50000
    taxable_income = gross_income - deductions - STANDARD_DEDUCTION
    return max(0, round(taxable_income, 2))
#
# #  --------------------------------------------------9 --------------------------------


def budget_planner(monthly_income, monthly_expenses):

    surplus = monthly_income - monthly_expenses

    if surplus <= 0:
        return {
            'surplus': surplus,
            'message': "You are overspending! Consider reducing expenses.",
            'savings': 0,
            'investments': 0,
            'free_to_use': 0
        }

    savings = round(surplus * 0.2, 2)
    investments = round(surplus * 0.3, 2)
    free_to_use = round(surplus * 0.5, 2)

    return {
        'surplus': round(surplus, 2),
        'message': "Good job! Here's how you can allocate your surplus.",
        'savings': savings,
        'investments': investments,
        'free_to_use': free_to_use
    }

# #  --------------------------------------------------10 --------------------------------


def calculate_net_worth(total_assets, total_liabilities):

    net_worth = total_assets - total_liabilities
    return round(net_worth, 2)
