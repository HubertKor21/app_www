# serializers.py
from rest_framework import serializers
from .models import Settlement
from accounts.models import CustomUserModel
from invitations.models import Family

class SettlementSerializer(serializers.ModelSerializer):
    family = serializers.PrimaryKeyRelatedField(queryset=Family.objects.all())
    debtor = serializers.PrimaryKeyRelatedField(queryset=CustomUserModel.objects.all())
    creditor = serializers.PrimaryKeyRelatedField(queryset=CustomUserModel.objects.all())

    class Meta:
        model = Settlement
        fields = ['id', 'family', 'debtor', 'creditor', 'amount', 'created_at', 'is_paid']
