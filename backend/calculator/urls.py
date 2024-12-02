# urls.py
from django.urls import path
from .views import  SavingsCalculatorListCreateView, SavingsCalculatorDetailView

urlpatterns = [
    path('savings-calculators/', SavingsCalculatorListCreateView.as_view(), name='savings-calculator-list-create'),
    path('savings-calculators/<int:pk>/', SavingsCalculatorDetailView.as_view(), name='savings-calculator-detail'),
]
