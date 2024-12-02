# models.py
from django.db import models
from accounts.models import CustomUserModel

class SavingsCalculator(models.Model):
    user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE, related_name='savings_calculators')
    expense_category = models.CharField(max_length=50)  # Typ wydatku, np. "Jedzenie", "Transport"
    monthly_spending = models.FloatField()  # Miesięczne wydatki w tej kategorii
    suggested_savings = models.FloatField(null=True, blank=True)  # Kwota, którą użytkownik może zaoszczędzić
    potential_savings = models.FloatField(null=True, blank=True)  # Potencjalna kwota oszczędności
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_savings(self):
        """Oblicza, ile można zaoszczędzić na podstawie wydatków"""
        self.suggested_savings = self.monthly_spending * 0.2  # Zaoszczędź 20% wydatków
        self.potential_savings = self.suggested_savings * 12  # Potencjalne oszczędności roczne
        self.save()

    def __str__(self):
        return f'Savings Calculator for {self.user.email}: {self.potential_savings} PLN/year'
