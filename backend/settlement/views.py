from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Settlement
from .serializers import SettlementSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from django.core.mail import send_mail
from invitations.models import Family
from accounts.models import CustomUserModel

class SettlementListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):     
        try:
            # Directly retrieve the family associated with the logged-in user
            family = request.user.family
        except Family.DoesNotExist:
            return Response({"error": "Family not found."}, status=status.HTTP_404_NOT_FOUND)

        # Fetch all settlements associated with the family
        settlements = Settlement.objects.filter(family=family)
        
        # Serialize and return the settlements
        serializer = SettlementSerializer(settlements, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SettlementSerializer(data=request.data)
        if serializer.is_valid():
            # Sprawdzamy, czy dłużnik i wierzyciel są różni
            debtor_id = serializer.validated_data.get('debtor')
            creditor_id = serializer.validated_data.get('creditor')

            if debtor_id == creditor_id:
                return Response({"error": "Dłużnik i wierzyciel nie mogą być tym samym użytkownikiem."},
                                status=status.HTTP_400_BAD_REQUEST)
            
            try:
                # Fetch the logged-in user's family
                family = request.user.family
            except Family.DoesNotExist:
                return Response({"error": "Family not found."}, status=status.HTTP_404_NOT_FOUND)

            # Create the settlement and save it with the family
            settlement = serializer.save(debtor=request.user, family=family)
            
            # Send email to creditor
            send_settlement_email(settlement.creditor, settlement.amount, 'Unpaid')
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SettlementDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk):
        try:
            return Settlement.objects.get(pk=pk)
        except Settlement.DoesNotExist:
            raise NotFound(detail="Settlement not found.")

    def get(self, request, pk):
        settlement = self.get_object(pk)
        serializer = SettlementSerializer(settlement)
        return Response(serializer.data)

    def put(self, request, pk):
        settlement = self.get_object(pk)
        serializer = SettlementSerializer(settlement, data=request.data)
        if serializer.is_valid():
            updated_settlement = serializer.save()
            
            # Wysyłamy e-mail do kredytora
            send_settlement_email(updated_settlement.creditor, updated_settlement.amount, 'Unpaid')
            
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        settlement = self.get_object(pk)
        serializer = SettlementSerializer(settlement, data=request.data, partial=True)
        if serializer.is_valid():
            updated_settlement = serializer.save()
            
            # Wysyłamy e-mail do kredytora, jeśli zmienił się status rozrachunku
            if 'is_paid' in request.data:
                status_message = 'Paid' if updated_settlement.is_paid else 'Unpaid'
                send_settlement_email(updated_settlement.creditor, updated_settlement.amount, status_message)
            
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        settlement = self.get_object(pk)
        settlement.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
def send_settlement_email(creditor, amount, settlement_status):
    print(f"Sending email to {creditor.email} with status {settlement_status} and amount {amount}")

    subject = f"Nowy rozrachunek: {settlement_status}"
    message = f"Masz nowy rozrachunek o wartości {amount} PLN. Status: {settlement_status}."
    from_email = settings.DEFAULT_FROM_EMAIL  # Użyj domyślnego adresu e-mail z ustawień

    try:
        # Wysyłamy e-mail do wierzyciela, czyli do osoby, której należna jest kwota
        send_mail(subject, message, from_email, [creditor.email])
    except Exception as e:
        # Można dodać logowanie błędów
        print(f"Błąd wysyłania e-maila: {e}")
