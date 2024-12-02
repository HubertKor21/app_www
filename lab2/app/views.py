from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from .models import Osoba, Position
from .serializers import OsobaSerializer, PositionSerializer
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse

class OsobaAPIView(APIView):
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

    def get(self, request, pk=None):
        if pk:
            osoba = get_object_or_404(Osoba, pk=pk)
            if osoba.wlasciciel != request.user and not request.user.has_perm('app_name.can_view_other_persons'):
                return Response({"error": "Nie masz uprawnień do tego obiektu"}, status=403)
            serializer = OsobaSerializer(osoba)
            return Response(serializer.data)

        queryset = Osoba.objects.filter(wlasciciel=request.user)
        if request.user.has_perm('app_name.can_view_other_persons'):
            queryset = Osoba.objects.all()

        serializer = OsobaSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OsobaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(wlasciciel=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        osoba = get_object_or_404(Osoba, pk=pk, wlasciciel=request.user)
        osoba.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk):
        osoba = self.get_object(pk, request.user)
        if not osoba:
            return Response({"error": "Object not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = OsobaSerializer(osoba, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Widoki dla Position
class PositionListView(generics.ListCreateAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer

class PositionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer

class StanowiskoMembersView(generics.ListAPIView):
    serializer_class = OsobaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        stanowisko_id = self.kwargs['id']
        return Osoba.objects.filter(position_id=stanowisko_id, wlasciciel=self.request.user)




def osoba_view(request, pk):
    if not request.user.has_perm('app.view_osoba'): 
        raise PermissionDenied("Nie masz uprawnień do wyświetlania obiektów Osoba.")
    
    try:
        osoba = Osoba.objects.get(pk=pk)
        return HttpResponse(f"Ten użytkownik nazywa się {osoba.name} {osoba.surname}.")
    except Osoba.DoesNotExist:
        return HttpResponse(f"W bazie nie ma użytkownika o id={pk}.")
