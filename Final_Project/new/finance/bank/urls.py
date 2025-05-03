from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('deposit/', views.deposit_view, name='deposit'),
    path('withdraw/', views.withdraw_view, name='withdraw'),
    path('emi', views.emi, name='emi'),
    path('sip', views.sip, name='sip'),
    path('fd', views.fd, name='fd'),
    path('rd', views.rd, name='rd'),
    path('estimate', views.estimate, name='estimate'),
    path('home_loan_estimator_view', views.home_loan_estimator_view, name='home_loan_estimator_view'),
    path('credit_card_interest_view', views.credit_card_interest_view, name='credit_card_interest_view'),
    path('taxable', views.taxable, name='taxable'),
    path('simple_budget_planner_view', views.simple_budget_planner_view, name='simple_budget_planner_view'),
    path('net_worth_view', views.net_worth_view, name='net_worth_view'),
    path('', views.loan_form_page, name='loan_form_page'),
    path('predict-loan/', views.predict_loan_amount_get, name='predict-loan'),
]
