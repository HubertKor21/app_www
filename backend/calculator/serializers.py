# serializers.py
from rest_framework import serializers
from .models import SavingsCalculator

class SavingsCalculatorSerializer(serializers.ModelSerializer):
    # Ustawiamy sugerowane i potencjalne oszczędności jako read_only
    suggested_savings = serializers.FloatField(read_only=True)
    potential_savings = serializers.FloatField(read_only=True)

    class Meta:
        model = SavingsCalculator
        fields = ['id', 'user', 'expense_category', 'monthly_spending', 'suggested_savings', 'potential_savings', 'created_at']

    def validate_user(self, value):
        if value is None:
            raise serializers.ValidationError("User is required.")
        return value

    def validate_expense_category(self, value):
        if not value:
            raise serializers.ValidationError("Expense category is required.")
        return value

    def validate_monthly_spending(self, value):
        if value is None or value <= 0:
            raise serializers.ValidationError("Monthly spending must be greater than 0.")
        return value

    def create(self, validated_data):
        # Tworzymy obiekt SavingsCalculator
        instance = super().create(validated_data)
        # Obliczamy sugerowane oszczędności i potencjalne oszczędności
        instance.calculate_savings()  # Wywołujemy metodę calculate_savings, aby obliczyć wartości
        return instance
