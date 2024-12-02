# urls.py
from django.urls import path
from .views import SavingsGoalListCreateView, SavingsGoalDetailView

urlpatterns = [
    path('savings-goals/', SavingsGoalListCreateView.as_view(), name='savings-goal-list-create'),
    path('savings-goals/<int:pk>/', SavingsGoalDetailView.as_view(), name='savings-goal-detail'),
]
