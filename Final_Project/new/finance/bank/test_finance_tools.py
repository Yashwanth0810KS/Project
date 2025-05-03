import unittest
from finance_tools import (
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


class TestCalculateEMI(unittest.TestCase):
    def test_input_validation(self):
        """Test that invalid inputs raise appropriate errors."""
        with self.assertRaises(ValueError):
            calculate_emi(-50000, 7.5, 10)
        with self.assertRaises(ValueError):
            calculate_emi(100000, -5.0, 10)

    def test_output_validation(self):
            """Test that output is a float, non-negative, and close to expected value."""
            principal = 200000
            annual_rate = 8.0
            tenure_years = 10
            expected_emi = 2424.79

            emi = calculate_emi(principal, annual_rate, tenure_years)

            self.assertIsInstance(emi, float)
            self.assertGreaterEqual(emi, 0)
            self.assertTrue(emi, expected_emi)

class SIPCalculation(unittest.TestCase):
    def test_invalid_types(self):
        with self.assertRaises(TypeError):
            calculate_sip("5000", 12, 10)  # String instead of float

        with self.assertRaises(TypeError):
            calculate_sip(5000, "12", 10)



    def test_negative_values(self):
        with self.assertRaises(ValueError):
            calculate_sip(-5000, 12, 10)

        with self.assertRaises(ValueError):
            calculate_sip(5000, -5, 10)
        with self.assertRaises(ValueError):
            calculate_sip(5000, 12, -2)



    def test_sip_future_value(self):
        fv = calculate_sip(5000, 12, 10)
        expected_fv = 1166793.0
        self.assertTrue(fv, expected_fv)


class FixedDepositCalculationTests(unittest.TestCase):

    def test_valid_inputs_and_output(self):
        """Test valid inputs and ensure correct output for FD calculation."""
        maturity, interest = calculate_fd(100000, 6, 5, 4)
        self.assertIsInstance(maturity, float)
        self.assertIsInstance(interest, float)

        self.assertGreaterEqual(maturity, 0)
        self.assertGreaterEqual(interest, 0)

        maturity, interest = calculate_fd(100000, 6, 5, 4)
        expected_maturity = 134391.60
        expected_interest = 34391.60
        self.assertTrue(maturity, expected_maturity)
        self.assertTrue(interest, expected_interest)

    def test_invalid_input_types(self):
        """Test invalid input types for FD calculation."""
        with self.assertRaises(TypeError):
            calculate_fd("100000", 6, 5, 4)
        with self.assertRaises(TypeError):
            calculate_fd(100000, "6", 5, 4)


    def test_invalid_values(self):
        """Test invalid values for FD calculation."""
        with self.assertRaises(ValueError):
            calculate_fd(-100000, 6, 5, 4)

        with self.assertRaises(ValueError):
            calculate_fd(100000, -6, 5, 4)

class RecurringDepositCalculationTests(unittest.TestCase):

    def test_valid_inputs_and_output(self):
        """Test valid inputs and ensure correct output for RD calculation."""
        maturity = calculate_rd(5000, 7.0, 5)
        expected_maturity = 346091.56
        self.assertIsInstance(maturity, float)
        self.assertGreaterEqual(maturity, 0)
        self.assertTrue(maturity, expected_maturity)

    def test_invalid_input_types(self):
        """Test invalid input types for RD calculation."""
        with self.assertRaises(TypeError):
            calculate_rd("5000", 7.0, 5)
        with self.assertRaises(TypeError):
            calculate_rd(5000, "7.0", 5)
        with self.assertRaises(TypeError):
            calculate_rd(5000, 7.0, "5")

    def test_invalid_values(self):
        """Test invalid values for RD calculation."""
        with self.assertRaises(ValueError):
            calculate_rd(-5000, 7.0, 5)

class RetirementEstimationTests(unittest.TestCase):

    def test_valid_inputs_and_output(self):
        """Test valid inputs and ensure correct output for retirement estimation."""
        total_corpus, total_invested, total_interest = estimate_retirement(100000, 5000, 8.0, 20)
        self.assertIsInstance(total_corpus, float)
        self.assertIsInstance(total_invested, float)
        self.assertIsInstance(total_interest, float)


        expected_total_corpus = 2901912.0
        expected_total_invested = 1200000.0
        expected_total_interest = 1701912.0

        self.assertTrue(total_corpus, expected_total_corpus)


    def test_invalid_input_types(self):
        """Test invalid input types for retirement estimation."""
        with self.assertRaises(TypeError):
            estimate_retirement("100000", 5000, 8.0, 20)

        with self.assertRaises(TypeError):
            estimate_retirement(100000, "5000", 8.0, 20)


    def test_invalid_value_ranges(self):
        """Test invalid values for retirement estimation."""
        with self.assertRaises(ValueError):
            estimate_retirement(-100000, 5000, 8.0, 20)

        with self.assertRaises(ValueError):
            estimate_retirement(100000, -5000, 8.0, 20)


class HomeLoanEligibilityTests(unittest.TestCase):

    def test_valid_inputs_and_output(self):

        loan_amount = calculate_home_loan_eligibility(50000, 20000, 20, 6.5)
        self.assertIsInstance(loan_amount, float)
        self.assertGreaterEqual(loan_amount, 0)
        expected_loan_amount = 4096612.29
        self.assertTrue(loan_amount, expected_loan_amount)

    def test_invalid_input_types(self):
        """Test invalid input types for home loan eligibility."""
        with self.assertRaises(TypeError):
            calculate_home_loan_eligibility("50000", 20000, 20, 6.5)
        with self.assertRaises(TypeError):
            calculate_home_loan_eligibility(50000, "20000", 20, 6.5)

    def test_invalid_value_ranges(self):
        """Test invalid values for home loan eligibility."""
        with self.assertRaises(ValueError):
            calculate_home_loan_eligibility(-50000, 20000, 20, 6.5)
        with self.assertRaises(ValueError):
            calculate_home_loan_eligibility(50000, -20000, 20, 6.5)

        with self.assertRaises(ValueError):
            calculate_home_loan_eligibility(50000, 20000, -20, 6.5)



    def test_zero_interest_rate(self):
        """Test with zero interest rate."""
        loan_amount = calculate_home_loan_eligibility(50000, 20000, 20, 0)


        expected_loan_amount = 50000 * 0.50 * 12 * 20
        self.assertTrue(loan_amount, expected_loan_amount)

class TestCalculateCreditCardBalance(unittest.TestCase):

    def test_valid_percentage_minimum_payment(self):
        initial_balance = 1000
        interest_rate = 18
        min_payment = 5
        months = 12

        remaining_balance = calculate_credit_card_balance(initial_balance, interest_rate, min_payment, months)
        expected_balance = 479.57

        self.assertTrue(remaining_balance, expected_balance)

    def test_invalid_inputs(self):
        with self.assertRaises(ValueError):
            calculate_credit_card_balance(-1000, 18, 100, 12)
        with self.assertRaises(ValueError):
            calculate_credit_card_balance(1000, -18, 100, 12)
        with self.assertRaises(ValueError):
            calculate_credit_card_balance(1000, 18, -100, 12)



class TestCalculateTaxableIncome(unittest.TestCase):
    def test_basic_case(self):
        self.assertEqual(calculate_taxable_income(700000, 100000), 550000.00)

    def test_exact_deduction(self):
        self.assertEqual(calculate_taxable_income(100000, 50000), 0.00)

    def test_negative_income(self):
        self.assertEqual(calculate_taxable_income(40000, 10000), 0.00)

class TestBudgetPlanner(unittest.TestCase):

    def test_surplus_allocation(self):
        result = budget_planner(100000, 70000)
        self.assertEqual(result['surplus'], 30000.00)
        self.assertEqual(result['savings'], 6000.00)
        self.assertEqual(result['investments'], 9000.00)
        self.assertEqual(result['free_to_use'], 15000.00)
        self.assertIn("Good job", result['message'])

    def test_zero_surplus(self):
        result = budget_planner(50000, 50000)
        self.assertEqual(result['surplus'], 0)
        self.assertEqual(result['savings'], 0)
        self.assertEqual(result['investments'], 0)
        self.assertEqual(result['free_to_use'], 0)
        self.assertIn("overspending", result['message'])



class TestCalculateNetWorth(unittest.TestCase):

    def test_positive_net_worth(self):
        self.assertEqual(calculate_net_worth(1000000, 400000), 600000.00)

    def test_zero_net_worth(self):
        self.assertEqual(calculate_net_worth(500000, 500000), 0.00)

    def test_negative_net_worth(self):
        self.assertEqual(calculate_net_worth(300000, 400000), -100000.00)


if __name__ == '__main__':
    unittest.main()
