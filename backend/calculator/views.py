from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import SavingsCalculator
from .serializers import SavingsCalculatorSerializer

class SavingsCalculatorListCreateView(APIView):
    def get(self, request):
        calculators = SavingsCalculator.objects.all()
        serializer = SavingsCalculatorSerializer(calculators, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SavingsCalculatorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SavingsCalculatorDetailView(APIView):
    def get(self, request, pk):
        try:
            calculator = SavingsCalculator.objects.get(pk=pk)
        except SavingsCalculator.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = SavingsCalculatorSerializer(calculator)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            calculator = SavingsCalculator.objects.get(pk=pk)
        except SavingsCalculator.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = SavingsCalculatorSerializer(calculator, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            calculator = SavingsCalculator.objects.get(pk=pk)
        except SavingsCalculator.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        calculator.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)