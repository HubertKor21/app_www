from decimal import Decimal

def calculate_fixed_rates(amount, interest_rate, installments_remaining):
    """Oblicza ratę stałą."""
    amount = Decimal(amount)
    interest_rate = Decimal(interest_rate)
    installments_remaining = int(installments_remaining)

    # Upewnij się, że liczba rat jest większa niż zero
    if installments_remaining <= 0:
        raise ValueError("Liczba rat musi być większa niż zero.")

    monthly_rate = (interest_rate / 100) / 12
    q = Decimal(1) + monthly_rate
    
    # Avoid division by zero if installments_remaining is 1
    if q**installments_remaining == 1:
        return round(amount * monthly_rate, 2)  # Simple monthly interest for 1 installment

    return round(amount * q**installments_remaining * monthly_rate / (q**installments_remaining - Decimal(1)), 2)

def calculate_decreasing_rates(amount, interest_rate, installment_number):
    """Oblicza raty malejące dla każdej raty (dla danej liczby rat)."""
    amount = Decimal(amount)
    interest_rate = Decimal(interest_rate)
    installment_number = int(installment_number)

    if installment_number <= 0:
        raise ValueError("Liczba rat musi być większa niż zero.")

    # Część kapitałowa, która jest stała dla każdej raty
    capital_part = amount / installment_number

    # Lista rat malejących
    rates = []
    for i in range(1, installment_number + 1):
        # Pozostała kwota do spłaty po poprzednich ratach
        remaining_amount = amount - (capital_part * (i - 1))

        # Obliczanie odsetek dla danej raty
        interest_payment = remaining_amount * (interest_rate / 100) / 12

        # Całkowita rata to część kapitałowa + odsetki
        total_payment = capital_part + interest_payment
        rates.append(round(total_payment, 2))

    return rates