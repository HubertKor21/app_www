# admin.py
from django.contrib import admin
from .models import Settlement

@admin.register(Settlement)
class SettlementAdmin(admin.ModelAdmin):
    list_display = ('family', 'debtor', 'creditor', 'amount', 'is_paid', 'created_at')  # Wyświetlanie pól w tabeli
    list_filter = ('is_paid', 'family')  # Filtry (np. po statusie 'is_paid' i rodzinie)
    search_fields = ('debtor__email', 'creditor__email', 'family__name')  # Wyszukiwanie według e-maili lub nazw rodzin
    ordering = ('-created_at',)  # Sortowanie po dacie utworzenia, najnowsze na górze

