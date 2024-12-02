from django.urls import path
from .views import OsobaListView, OsobaDetailView, OsobaSearchView, PositionListView, PositionDetailView

urlpatterns = [
    path('osoby/', OsobaListView.as_view(), name='osoba-list'),
    path('osoby/<int:pk>/', OsobaDetailView.as_view(), name='osoba-detail'),
    path('osoby/search/', OsobaSearchView.as_view(), name='osoba-search'),
    path('stanowiska/', PositionListView.as_view(), name='position-list'),
    path('stanowiska/<int:pk>/', PositionDetailView.as_view(), name='position-detail'),
]
