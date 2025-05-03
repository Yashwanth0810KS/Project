from django.shortcuts import render, redirect
from django.http import HttpResponse
import joblib
import os
import numpy as np

# Load model and scaler

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import RegisterForm, DepositForm, WithdrawForm
from django.contrib.auth.forms import AuthenticationForm

from .finance_tools import (
    calculate_emi,
    calculate_sip,
    calculate_fd,
    calculate_rd,
    estimate_retirement,
    calculate_home_loan_eligibility,
    calculate_credit_card_balance,
    calculate_taxable_income,
    budget_planner,
    calculate_net_worth
)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model = joblib.load(os.path.join(BASE_DIR, 'loan_prediction_model.pkl'))
scaler = joblib.load(os.path.join(BASE_DIR, 'loan_scaler.pkl'))

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Account.objects.create(user=user)
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'bank/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'bank/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard_view(request):
    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    return render(request, 'bank/dashboard.html', {'account': account, 'transactions': transactions})

@login_required
def deposit_view(request):
    account = Account.objects.get(user=request.user)
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            account.balance += amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
            return redirect('dashboard')
    else:
        form = DepositForm()
    return render(request, 'bank/deposit.html', {'form': form})

@login_required
def withdraw_view(request):
    account = Account.objects.get(user=request.user)
    if request.method == 'POST':
        form = WithdrawForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            if account.balance >= amount:
                account.balance -= amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='withdraw')
                return redirect('dashboard')
            else:
                form.add_error('amount', 'Insufficient balance')
    else:
        form = WithdrawForm()
    return render(request, 'bank/withdraw.html', {'form': form})

@login_required
def emi(request):
    emi_result = None
    error = None

    if request.method == "POST":
        try:
            principal = float(request.POST['principal'])
            rate = float(request.POST['rate'])
            tenure = int(request.POST['tenure'])

            if principal <= 0 or rate < 0 or tenure <= 0:
                error = "Please enter valid, positive values."
            else:
                emi_result = calculate_emi(principal, rate, tenure)

        except ValueError:
            error = "Invalid input. Please enter numbers only."

    return render(request, 'bank/finance.html', {
        'emi': emi_result,
        'error': error
    })
@login_required
def sip(request):
    future_value = None
    error_message = None

    if request.method == 'POST':
        try:
            sip = float(request.POST.get('sip', 0))
            rate = float(request.POST.get('rate', 0))
            years = int(request.POST.get('years', 0))

            # Validate input
            if sip <= 0:
                error_message = "Monthly SIP amount must be a positive number."
            elif rate <= 0:
                error_message = "Annual return rate must be a positive value."
            elif years <= 0:
                error_message = "Investment duration must be a positive number."
            else:
                future_value = calculate_sip(sip, rate, years)  # external function

        except (ValueError, TypeError):
            error_message = "Please enter valid numeric values."

    return render(request, 'bank/sip.html', {
        'future_value': future_value,
        'error_message': error_message
    })

def fd(request):
    maturity_amount = None
    error_message = None

    if request.method == 'POST':
        try:
            principal = float(request.POST.get('principal', 0))
            rate = float(request.POST.get('rate', 0))
            years = float(request.POST.get('years', 0))
            frequency = int(request.POST.get('frequency', 0))  # Compounding frequency (e.g., 1 for yearly, 4 for quarterly)

            # Input validations
            if principal <= 0:
                error_message = "Principal amount must be a positive number."
            elif rate <= 0:
                error_message = "Interest rate must be a positive value."
            elif years <= 0:
                error_message = "Investment duration must be greater than zero."
            elif frequency <= 0:
                error_message = "Compounding frequency must be a positive integer."
            else:
                maturity_amount = calculate_fd(principal, rate, years, frequency)

        except (ValueError, TypeError):
            error_message = "Please enter valid numeric inputs."

    return render(request, 'bank/FD.html', {
        'maturity_amount': maturity_amount,
        'error_message': error_message
    })



@login_required
def rd(request):
    maturity_value = None
    error_message = None

    if request.method == 'POST':
        try:
            monthly_deposit = float(request.POST.get('deposit', 0))
            annual_rate = float(request.POST.get('rate', 0))
            years = int(request.POST.get('years', 0))

            # Input validation
            if monthly_deposit <= 0:
                error_message = "Monthly deposit must be a positive amount."
            elif annual_rate <= 0:
                error_message = "Interest rate must be a positive value."
            elif years <= 0:
                error_message = "Number of years must be greater than zero."
            else:
                maturity_value = calculate_rd(monthly_deposit, annual_rate, years)

        except (ValueError, TypeError):
            error_message = "Please enter valid numeric values."

    return render(request, 'bank/RD.html', {
        'maturity_value': maturity_value,
        'error_message': error_message
    })

@login_required
def estimate(request):
    corpus = invested = interest = None
    error_message = None

    if request.method == 'POST':
        try:
            current_savings = float(request.POST.get('current_savings', 0))
            monthly_contribution = float(request.POST.get('monthly_contribution', 0))
            annual_return = float(request.POST.get('annual_return', 0))
            years = int(request.POST.get('years', 0))

            # Validate inputs
            if current_savings < 0:
                error_message = "Current savings must be a non-negative value."
            elif monthly_contribution < 0:
                error_message = "Monthly contribution must be a non-negative value."
            elif annual_return < 0:
                error_message = "Annual return must be a non-negative value."
            elif years <= 0:
                error_message = "Years until retirement must be a positive number."
            else:
                corpus, invested, interest = estimate_retirement(
                    current_savings,
                    monthly_contribution,
                    annual_return,
                    years
                )

        except (ValueError, TypeError):
            error_message = "Please enter valid numeric values."

    return render(request, 'bank/retirement.html', {
        'estimated_corpus': corpus,
        'total_invested': invested,
        'total_interest': interest,
        'error_message': error_message,
    })

@login_required
def home_loan_estimator_view(request):
    loan_amount = None  # Default value
    error_message = None  # Variable to hold any error messages

    if request.method == 'POST':
        try:
            # Retrieve form data from POST request
            monthly_income = float(request.POST.get('monthly_income', 0))
            monthly_expenses = float(request.POST.get('monthly_expenses', 0))
            loan_term_years = int(request.POST.get('loan_term_years', 0))
            interest_rate = float(request.POST.get('interest_rate', 0))

            # Ensure inputs are positive
            if monthly_income <= 0:
                error_message = "Monthly income must be a positive value."
            elif monthly_expenses < 0:
                error_message = "Monthly expenses cannot be negative."
            elif loan_term_years <= 0:
                error_message = "Loan term in years must be a positive value."
            elif interest_rate <= 0:
                error_message = "Interest rate must be a positive value."
            else:
                # Call the function to calculate loan eligibility if inputs are valid
                loan_amount = calculate_home_loan_eligibility(
                    monthly_income,
                    monthly_expenses,
                    loan_term_years,
                    interest_rate
                )

        except (ValueError, TypeError):  # Handle exceptions for invalid input
            error_message = "Please enter valid numeric values for all fields."

    # Return results to template, along with any error messages
    return render(request, 'bank/home_loan.html', {
        'loan_amount': loan_amount,
        'error_message': error_message  # Pass error message to template
    })


@login_required
def credit_card_interest_view(request):
    balance = None  # Default value in case of no result
    error_message = None  # Variable to hold error message in case of invalid input

    if request.method == 'POST':
        try:
            # Retrieve form data
            initial_balance = float(request.POST.get('initial_balance', 0))
            interest_rate = float(request.POST.get('interest_rate', 0))
            min_payment = float(request.POST.get('min_payment', 0))
            months = int(request.POST.get('months', 0))

            # Ensure inputs are valid and positive
            if initial_balance <= 0:
                error_message = "Initial balance must be a positive value."
            elif interest_rate <= 0:
                error_message = "Interest rate must be a positive value."
            elif min_payment <= 0:
                error_message = "Minimum payment must be a positive value."
            elif months <= 0:
                error_message = "Months must be a positive value."
            else:
                # Call the function to calculate the outstanding balance
                balance = calculate_credit_card_balance(
                    initial_balance,
                    interest_rate,
                    min_payment,
                    months
                )
        except (ValueError, TypeError) as e:
            error_message = "Please enter valid numeric values for all fields."

    # Return results to template
    return render(request, 'bank/credit_card.html', {
        'balance': balance,
        'error_message': error_message  # Pass the error message to the template
    })

# views.py

@login_required
def taxable(request):
    taxable_income = None
    error_message = None  # Add an error message variable to show validation errors

    if request.method == 'POST':
        try:
            # Get values from the POST request
            gross_income = float(request.POST.get('gross_income', 0))
            deductions = float(request.POST.get('deductions', 0))

            # Ensure the income and deductions are positive values
            if gross_income <= 0:
                error_message = "Gross income must be a positive value."
            elif deductions < 0:
                error_message = "Deductions cannot be negative."
            else:
                # Calculate taxable income if inputs are valid
                taxable_income = calculate_taxable_income(gross_income, deductions)

        except (ValueError, TypeError):
            error_message = "Please enter valid numeric values."

    return render(request, 'bank/taxable.html', {
        'taxable_income': taxable_income,
        'error_message': error_message  # Pass error message to the template if any
    })
@login_required
def simple_budget_planner_view(request):
    result = None
    error_message = None

    if request.method == 'POST':
        try:
            # Get the input values from the form
            monthly_income = float(request.POST.get('monthly_income', 0))
            monthly_expenses = float(request.POST.get('monthly_expenses', 0))

            # Check if both values are positive
            if monthly_income <= 0:
                error_message = "Monthly income must be a positive value."
            elif monthly_expenses < 0:
                error_message = "Monthly expenses cannot be negative."
            else:
                # If inputs are valid, call the budget_planner function
                result = budget_planner(monthly_income, monthly_expenses)

        except (ValueError, TypeError):
            error_message = "Please enter valid numeric values for income and expenses."

    return render(request, 'bank/simple_budget.html', {'result': result, 'error_message': error_message})



@login_required
def net_worth_view(request):
    result = None
    error_message = None

    if request.method == 'POST':
        try:
            assets = float(request.POST.get('assets', 0))
            liabilities = float(request.POST.get('liabilities', 0))

            if assets < 0:
                error_message = "Assets must be non-negative values."
            elif liabilities < 0:
                error_message = "Liabilities must be non-negative values."
            else:
                result = calculate_net_worth(assets, liabilities)

        except (ValueError, TypeError):
            error_message = "Please enter valid numeric values."

    return render(request, 'bank/net_worth.html', {
        'net_worth': result,
        'error_message': error_message  # Ensure this is passed to template
    })
@login_required
def loan_form_page(request):
    return render(request, 'bank/predictor_form.html')


@login_required
def predict_loan_amount_get(request):
    try:

        age = float(request.GET['Age'])
        income = float(request.GET['Monthly_Income'])  # Monthly income in INR
        score = float(request.GET['Credit_Score'])
        tenure_years = float(request.GET['Loan_Tenure_Years'])
        existing_loan = float(request.GET['Existing_Loan_Amount'])
        dependents = float(request.GET['Num_of_Dependents'])


        features = [[age, income, score, tenure_years, existing_loan, dependents]]
        scaled = scaler.transform(features)
        predicted_amount = model.predict(scaled)[0]


        foir = 0.5
        tenure_months = tenure_years * 12
        max_eligible_emi = income * foir
        max_possible_loan = max_eligible_emi * tenure_months


        max_possible_loan = max_possible_loan - existing_loan
        max_possible_loan = max(max_possible_loan, 0)
        final_prediction = min(predicted_amount, max_possible_loan)

        return render(request, 'bank/prediction_result.html', {
            'prediction': round(final_prediction, 2)
        })

    except Exception as e:
        return HttpResponse(f"<h3>Error: {str(e)}</h3>", status=400)
