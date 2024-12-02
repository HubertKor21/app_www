from rest_framework import serializers
from .models import SavingsGoal

class SavingsGoalSerializer(serializers.ModelSerializer):
    progress = serializers.SerializerMethodField()

    class Meta:
        model = SavingsGoal
        fields = ['id', 'title', 'goal_type', 'target_amount', 'current_amount', 'due_date', 'user', 'created_at', 'progress']
        read_only_fields = ['id', 'created_at', 'progress',]


    def validate_due_date(self, value):
        if value is None or value == '':
            raise serializers.ValidationError("Due date is required.")
        return value

    def get_progress(self, obj):
        return obj.progress()
