# urls.py
from django.urls import path
from .views import SettlementListCreateAPIView, SettlementDetailAPIView

urlpatterns = [
    path('settlements/', SettlementListCreateAPIView.as_view(), name='settlement-list-create'),
    path('settlements/<int:pk>/', SettlementDetailAPIView.as_view(), name='settlement-detail'),
]
