===============================================================
                ONLINE BANKING SYSTEM - USER MANUAL
===============================================================

A complete platform for secure banking transactions and personal financial tools.

---------------------------------------------------------------
TABLE OF CONTENTS
---------------------------------------------------------------
1. Overview
2. System Requirements
3. Setup Instructions
4. User Registration & Authentication
5. Banking Features
6. Personal Finance Tools
7. Loan Estimator (ML Powered)
8. Security Measures
9. Troubleshooting Guide
10. Contact & Support

---------------------------------------------------------------
1. OVERVIEW
---------------------------------------------------------------
This Online Banking System enables users to:
- Register and securely log in
- Perform deposits, withdrawals, and view balance
- Use tools like EMI, SIP, FD, tax, and budget calculators
- Predict loan eligibility via machine learning

Built using:
- Python
- Django
- Pandas
- SQLite/PostgreSQL
- HTML

---------------------------------------------------------------
2. SYSTEM REQUIREMENTS
---------------------------------------------------------------
For Users:
- Browser: Chrome, Firefox, Edge, Safari
- Internet Connection

For Developers:
- Python 3.x
- Django 5.x
- SQLite or PostgreSQL
- Git (Version Control)
- JIRA (Task Tracking)

---------------------------------------------------------------
3. SETUP INSTRUCTIONS
---------------------------------------------------------------
Step 1: Clone the Repository
> git clone https://github.com/your-repo/bank.git
> cd banking-system

Step 2: Install Dependencies
> pip install -r requirements.txt

Step 3: Apply Migrations
> python manage.py makemigrations
> python manage.py migrate

Step 4: Start the Server
> python manage.py runserver

Access the app at: http://127.0.0.1:8000/

---------------------------------------------------------------
4. USER REGISTRATION & AUTHENTICATION
---------------------------------------------------------------
Register:
- Visit: /register/
- Provide name, email, and password
- Click "Sign Up"

Login:
- Visit: /login/
- Enter credentials
- Access dashboard

Logout:
- Click "Logout" on dashboard to end session

---------------------------------------------------------------
5. BANKING FEATURES
---------------------------------------------------------------
View Balance:
- Login to dashboard, balance is shown

Deposit Money:
- Click "Deposit Money"
- Enter amount and submit

Withdraw Money:
- Click "Withdraw Money"
- Enter amount ≤ balance
- Submit to process withdrawal

Transaction History:
- All transactions are logged and viewable

---------------------------------------------------------------
6. PERSONAL FINANCE TOOLS
---------------------------------------------------------------
Available Tools:
- EMI Calculator
- SIP Calculator
- FD & RD Calculators
- Retirement Savings Estimator
- Home Loan Estimator
- Credit Card Interest Calculator
- Taxable Income Calculator
- Budget Planner
- Net Worth Calculator

How to Use:
- Login
- Go to "Financial Tools"
- Choose tool, enter details, click "Calculate"

---------------------------------------------------------------
7. LOAN ESTIMATOR (ML POWERED)
---------------------------------------------------------------
Predicts max loan amount based on:
- Age
- Monthly Income
- Credit Score
- Loan Tenure
- Existing Loans
- Dependents

Usage:
- Login
- Go to "Loan Estimator"
- Enter details
- Click "Predict Loan Amount"

---------------------------------------------------------------
8. SECURITY MEASURES
---------------------------------------------------------------
- Password Encryption (Django auth system)
- Authentication Required for all banking features
- Transaction Validations (e.g., balance checks)
- Secure Database Access (PostgreSQL/SQLite)

---------------------------------------------------------------
9. TROUBLESHOOTING GUIDE
---------------------------------------------------------------
| Issue                          | Solution                            |
|-------------------------------|-------------------------------------|
| Cannot log in                 | Check credentials or reset password |
| Deposit not reflected         | Refresh or check transaction history|
| Withdrawal error              | Ensure sufficient balance           |
| Financial tool not loading    | Clear browser cache and refresh     |
| Loan prediction error         | Verify input values                 |

---------------------------------------------------------------
10. CONTACT & SUPPORT
---------------------------------------------------------------
- Email: support@bankingapp.com
- Phone: +91-8431578288
- GitHub: (https://github.com/Yashwanth0810KS)

---------------------------------------------------------------
FINAL NOTES
---------------------------------------------------------------
This system integrates secure online banking with helpful financial tools. It provides a smooth, modern experience for everyday money management.

===============================================================
