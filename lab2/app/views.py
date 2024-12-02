from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Osoba, Position
from .serializers import OsobaSerializer, PositionSerializer

class OsobaAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            osoba = Osoba.objects.get(pk=pk)
            serializer = OsobaSerializer(osoba)
            return Response(serializer.data)
        osoby = Osoba.objects.all()
        serializer = OsobaSerializer(osoby, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OsobaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        osoba = Osoba.objects.get(pk=pk)
        osoba.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Widoki dla Position
class PositionListView(generics.ListCreateAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer

class PositionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
