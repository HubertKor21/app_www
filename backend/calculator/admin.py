# admin.py
from django.contrib import admin
from .models import SavingsCalculator

class SavingsGoalAdmin(admin.ModelAdmin):
    list_display = ('title', 'goal_type', 'target_amount', 'current_amount', 'due_date', 'user', 'created_at', 'progress')
    search_fields = ('title', 'user__email', 'goal_type')
    list_filter = ('goal_type', 'user', 'created_at')
    readonly_fields = ('progress', 'created_at')  # Pole progress i created_at są tylko do odczytu


admin.site.register(SavingsCalculator)
