from django.urls import path
from .views import BankListCreateView, BudgetDetailView, CurrentMonthBalanceView, BankNameListView, IncomeByDateView

urlpatterns = [
    path('banks/', BankListCreateView.as_view(), name='bank-list-create'),
    path('budget/', BudgetDetailView.as_view(), name='budget-detail'),
    path('balance/monthly/', CurrentMonthBalanceView.as_view(), name='monthly-balance'),
    path('banks/name/', BankNameListView.as_view(), name='bank-list'),
    path('income-by-date/', IncomeByDateView.as_view(), name='income-by-date'),
    path('banks/<int:pk>/', BankListCreateView.as_view(), name='bank-update'),

]