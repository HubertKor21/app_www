from django.shortcuts import render
from rest_framework import generics
from .models import Team,Person, Osoba, Position
from .serializers import PersonSerializer, OsobaSerializer, PositionSerializer
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response

# Create your views here.
class PersonView(generics.ListCreateAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    permission_classes = [AllowAny]

class OsobaListCreateVies(generics.ListCreateAPIView):
    serializer_class = OsobaSerializer

    def get_queryset(self):
        queryset = Osoba.objects.all()
        # Zawsze filtrujemy obiekty zawierające literę "a" w polu `name`
        queryset = queryset.filter(name__icontains='a')
        return queryset
    
    
class OsobaDeleteView(generics.DestroyAPIView):
    queryset = Osoba.objects.all()
    serializer_class = OsobaSerializer
    lookup_field = 'pk'  

class OsobaUpdateView(generics.UpdateAPIView):
    queryset = Osoba.objects.all()
    serializer_class = OsobaSerializer
    lookup_field = 'pk'  # Aktualizacja na podstawie klucza głównego (id)

    def perform_update(self, serializer):
        instance = serializer.save()
        print(f"Updated Osoba: {instance}")

class PositionListCreateViews(generics.ListCreateAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer


class PositionDeleteView(generics.DestroyAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    lookup_field = 'pk'
