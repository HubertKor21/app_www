from rest_framework import generics
from .models import Osoba, Position
from .serializers import OsobaSerializer, PositionSerializer

# Widoki dla Osoba
class OsobaListView(generics.ListCreateAPIView):
    queryset = Osoba.objects.all()
    serializer_class = OsobaSerializer

class OsobaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Osoba.objects.all()
    serializer_class = OsobaSerializer

class OsobaSearchView(generics.ListAPIView):
    serializer_class = OsobaSerializer

    def get_queryset(self):
        query = self.request.query_params.get('name', '')
        return Osoba.objects.filter(name__icontains=query)

# Widoki dla Position
class PositionListView(generics.ListCreateAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer

class PositionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
