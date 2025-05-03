from django.test import TestCase
from django.contrib.auth.models import User
from .forms import RegisterForm, DepositForm, WithdrawForm
import unittest

from forms import RegisterForm, DepositForm, WithdrawForm  # Replace with your app name


class TestRegisterForm(unittest.TestCase):
    def test_valid_data(self):
        form = RegisterForm(data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'StrongPassword123!',
            'password2': 'StrongPassword123!',
        })
        self.assertTrue(form.is_valid())

    def test_passwords_do_not_match(self):
        form = RegisterForm(data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'pass1',
            'password2': 'pass2',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_missing_username(self):
        form = RegisterForm(data={
            'username': '',
            'email': 'test@example.com',
            'password1': 'pass1234',
            'password2': 'pass1234',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)


class TestDepositForm(unittest.TestCase):
    def test_valid_amount(self):
        form = DepositForm(data={'amount': 100})
        self.assertTrue(form.is_valid())

    def test_zero_amount(self):
        form = DepositForm(data={'amount': 0})
        self.assertFalse(form.is_valid())

    def test_negative_amount(self):
        form = DepositForm(data={'amount': -5})
        self.assertFalse(form.is_valid())


class TestWithdrawForm(unittest.TestCase):
    def test_valid_amount(self):
        form = WithdrawForm(data={'amount': 50})
        self.assertTrue(form.is_valid())

    def test_zero_amount(self):
        form = WithdrawForm(data={'amount': 0})
        self.assertFalse(form.is_valid())

    def test_negative_amount(self):
        form = WithdrawForm(data={'amount': -10})
        self.assertFalse(form.is_valid())


if __name__ == '__main__':
    unittest.main()
