from django.urls import path
from .views import  PositionListView, PositionDetailView,  OsobaAPIView, StanowiskoMembersView, osoba_view

urlpatterns = [
    path('osoby/', OsobaAPIView.as_view(), name='osoba-list'),
    path('osoby/<int:pk>/', OsobaAPIView.as_view(), name='osoba-detail'),
    path('osoby/search/', OsobaAPIView.as_view(), name='osoba-search'),
    path('stanowiska/', PositionListView.as_view(), name='position-list'),
    path('stanowiska/<int:pk>/', PositionDetailView.as_view(), name='position-detail'),
    path('stanowisko/<int:id>/members/', StanowiskoMembersView.as_view(), name='stanowisko-members'),
    path('osoba/<int:pk>/', osoba_view, name='osoba_view'),

]
