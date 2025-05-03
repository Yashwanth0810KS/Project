from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,

    )
    password1 = forms.CharField(
        widget=forms.PasswordInput,

    )

    password2 = forms.CharField(
        widget=forms.PasswordInput,

    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class DepositForm(forms.Form):
    amount = forms.DecimalField(min_value=1)

class WithdrawForm(forms.Form):
    amount = forms.DecimalField(min_value=1)
