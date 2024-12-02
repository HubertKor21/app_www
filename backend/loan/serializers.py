from rest_framework import serializers
from .models import Loan
from .utils import calculate_decreasing_rates, calculate_fixed_rates

class LoanSerializer(serializers.ModelSerializer):
    # Mark calculated fields as read-only (not saved to DB)
    fixed_rate = serializers.ReadOnlyField()
    decreasing_rate = serializers.ReadOnlyField()

    class Meta:
        model = Loan
        fields = '__all__'

    def validate(self, data):
        # Validate that the loan amount is greater than zero
        if data.get('amount_reaming', 0) <= 0:
            raise serializers.ValidationError("Kwota kredytu musi być większa niż 0.")
        
        # Validate that the interest rate is not negative
        if data.get('interest_rate', 0) < 0:
            raise serializers.ValidationError("Oprocentowanie nie może być ujemne.")
        
        # Validate that installments_remaining is greater than 0
        if data.get('installments_remaining', 0) <= 0:
            raise serializers.ValidationError("Liczba rat musi być większa niż 0 serializer.")

        return data

    def create(self, validated_data):
        # Get the necessary data to calculate the rates
        amount = validated_data.get('amount_reaming')
        interest_rate = validated_data.get('interest_rate')
        installments_remaining = validated_data.get('installments_remaining')

        # Calculate the fixed rate and decreasing rate
        fixed_rate = calculate_fixed_rates(amount, interest_rate, installments_remaining)
        decreasing_rate = calculate_decreasing_rates(amount, interest_rate, installments_remaining)

        # Remove the calculated fields from validated_data since they are not part of the model
        validated_data.pop('fixed_rate', None)
        validated_data.pop('decreasing_rate', None)

        # Call the parent class's create method to create the Loan instance
        loan = super().create(validated_data)

        # After the Loan object is created, we set the calculated values (if needed)
        loan.fixed_rate = fixed_rate
        loan.decreasing_rate = decreasing_rate

        # Save the loan instance with the calculated values
        loan.save()

        return loan