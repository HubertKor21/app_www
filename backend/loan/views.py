from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Loan
from .serializers import LoanSerializer
from .utils import calculate_fixed_rates, calculate_decreasing_rates
from rest_framework.permissions import IsAuthenticated

class LoanListCreateView(APIView):
    """Widok do pobierania i dodawania kredytów dla zalogowanego użytkownika."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Pobierz listę kredytów dla zalogowanego użytkownika."""
        # Filtrujemy kredyty powiązane z użytkownikiem i jego rodziną
        loans = Loan.objects.filter(family=request.user.family)  # Zmiana: wszyscy członkowie rodziny
        serializer = LoanSerializer(loans, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Dodaj nowy kredyt dla zalogowanego użytkownika i jego rodziny."""
        # Zbieramy dane z requesta
        data = request.data.copy()
        data['user'] = request.user.id  # Automatycznie przypisujemy użytkownika
        data['family'] = request.user.family.id  # Automatycznie przypisujemy rodzinę

        # Tworzymy i walidujemy serializer z nowymi danymi
        serializer = LoanSerializer(data=data)
        if serializer.is_valid():
            # Zapisujemy nowy kredyt z automatycznym przypisaniem użytkownika i rodziny
            loan = serializer.save()

            # Obliczenie rat na podstawie rodzaju
            if loan.loan_type == 'fixed':
                loan.monthly_rate = calculate_fixed_rates(
                    loan.amount_reaming, loan.interest_rate, loan.installments_remaining
                )
            elif loan.loan_type == 'decreasing':
                loan.monthly_rate = calculate_decreasing_rates(
                    loan.amount_reaming, loan.interest_rate, loan.installments_remaining
                )

            loan.save()  # Zapisujemy zmiany
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CalculateRateView(APIView):
    """Oblicza raty dla kredytów powiązanych z rodziną użytkownika."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Oblicz i zwróć raty dla wszystkich kredytów powiązanych z rodziną użytkownika."""
        try:
            family = request.user.family  # Pobierz rodzinę użytkownika
            loans = Loan.objects.filter(family=family)

            response_data = []
            for loan in loans:
                if loan.loan_type == 'fixed':
                    rates = [calculate_fixed_rates(loan.amount_reaming, loan.interest_rate, i) for i in range(1, loan.installments_remaining + 1)]
                elif loan.loan_type == 'decreasing':
                    rates = [calculate_decreasing_rates(loan.amount_reaming, loan.interest_rate, i) for i in range(1, loan.installments_remaining + 1)]
                else:
                    rates = None  # Typ kredytu nieznany

                response_data.append({
                    "loan_id": loan.id,
                    "name": loan.name,
                    "amount_remaining": loan.amount_reaming,
                    "interest_rate": loan.interest_rate,
                    "remaining_installments": loan.installments_remaining,
                    "loan_type": loan.loan_type,
                    "calculated_rates": rates,
                })

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LoanInstallmentsDetailView(APIView):
    """Widok do obliczania rat kredytu stałego lub malejącego."""

    permission_classes = [IsAuthenticated]

    def get(self, request, loan_id):
        """Oblicz i zwróć raty dla kredytu powiązanego z użytkownikiem i jego rodziną."""
        loan_type = request.query_params.get('loan_type')  # Bez domyślnej wartości

        try:
            # Pobierz kredyt powiązany z użytkownikiem i jego rodziną
            loan = Loan.objects.get(id=loan_id, family=request.user.family)  # Zmiana: uwzględniamy całą rodzinę

            # Jeśli loan_type nie zostało podane w zapytaniu, używamy domyślnego typu z bazy danych
            if not loan_type:
                loan_type = loan.loan_type  # Używamy typu kredytu z modelu (np. 'fixed' lub 'decreasing')

            # Obliczamy raty w zależności od typu kredytu
            if loan_type == 'fixed':
                rates = [calculate_fixed_rates(loan.amount_reaming, loan.interest_rate, loan.installments_remaining) for _ in range(loan.installments_remaining)]
            elif loan_type == 'decreasing':
                rates = calculate_decreasing_rates(loan.amount_reaming, loan.interest_rate, loan.installments_remaining)
            else:
                return Response({"error": "Nieprawidłowy typ kredytu."}, status=status.HTTP_400_BAD_REQUEST)

            return Response({
                'loan_name': loan.name,
                'loan_type': loan.loan_type,
                'total_amount_remaining': str(loan.amount_reaming),
                'interest_rate': str(loan.interest_rate),
                'installments_remaining': loan.installments_remaining,
                'installments': rates
            }, status=status.HTTP_200_OK)

        except Loan.DoesNotExist:
            return Response({"error": "Kredyt nie istnieje lub nie należy do tej rodziny."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

