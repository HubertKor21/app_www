from django.urls import path
from .views import PersonView, OsobaListCreateVies, OsobaDeleteView, PositionListCreateViews, PositionDeleteView, OsobaUpdateView# Importing the view directly



urlpatterns = [
    path('person/', PersonView.as_view(), name='PersonView'),
    path('osoba/', OsobaListCreateVies.as_view(), name='osoba'),
    path('osoba/<int:pk>/delete/',OsobaDeleteView.as_view(), name='delete' ),
    path('position/', PositionListCreateViews.as_view(), name='position'),
    path('position/<int:pk>/delete', PositionDeleteView.as_view(), name='delete-position'),
    path('osoba/<int:pk>/update', OsobaUpdateView.as_view(), name="update"),
]