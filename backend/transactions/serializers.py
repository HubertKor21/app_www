from rest_framework import serializers
from .models import Bank, Budget

class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = ['id', 'user', 'bank_name', 'balance']
        read_only_fields = ['user']  # user is set automatically


class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ['id', 'family_id', 'amount', 'created_at']
        read_only_fields = ['created_at']  # Assuming created_at should be read-only

class BankNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = ['id', 'bank_name']