from rest_framework import serializers
from accounts.models import CustomUserModel
from .models import Family

class InviteUserSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    family_name = serializers.CharField(required=True)

    # def validate_email(self, value):
    #     if CustomUserModel.objects.filter(email=value).exists():
    #         raise serializers.ValidationError("This email is already in use")
    #     return value
    
class ConfirmInvitationSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUserModel
        fields = ['id','email', 'first_name', 'last_name']  

class FamilySerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Family
        fields = ['name', 'members']
