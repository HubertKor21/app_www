from django.contrib import admin
from .models import Bank, Budget, Transaction

class BankAdmin(admin.ModelAdmin):
    list_display = ('user', 'bank_name', 'balance')
    list_filter = ('user', 'bank_name')
    search_fields = ('user__email', 'bank_name')
    readonly_fields = ('balance',)  # `balance` jako tylko do odczytu, jeśli potrzebne
    ordering = ('user',)

    def get_family(self, obj):
        # Wyświetla rodzinę powiązaną z użytkownikiem
        return obj.user.family if obj.user.family else "Brak rodziny"
    get_family.short_description = "Rodzina"  # Ustawia tytuł kolumny

class BudgetAdmin(admin.ModelAdmin):
    list_display = ('family_id', 'amount', 'created_at')
    list_filter = ('family_id', 'created_at')
    search_fields = ('family_id__name',)  # Upewnij się, że istnieje pole `name` w modelu `Family`
    ordering = ('family_id',)

    def get_total_balance(self, obj):
        # Funkcja obliczająca całkowity balance dla rodziny
        total_balance = sum(bank.balance for bank in Bank.objects.filter(user__family=obj.family_id))
        return total_balance
    get_total_balance.short_description = "Całkowity balans rodziny"  # Nazwa kolumny

    readonly_fields = ('amount',)

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('bank', 'amount', 'date')
    list_filter = ('bank', 'date')
    search_fields = ('bank__bank_name', 'bank__user__email')
    ordering = ('-date',)  # Sortowanie po dacie w kolejności malejącej
    date_hierarchy = 'date'  # Dodanie możliwości filtrowania po dacie

# Rejestracja modeli w panelu administracyjnym
admin.site.register(Bank, BankAdmin)
admin.site.register(Budget, BudgetAdmin)
admin.site.register(Transaction, TransactionAdmin)
