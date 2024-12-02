from django.db import models
from accounts.models import CustomUserModel
from django.db.models.signals import post_save
from django.dispatch import receiver

class SavingsGoal(models.Model):
    GOAL_CHOICES = [
        ('vacation', 'Wakacje'),
        ('home_renovation', 'Remont'),
        ('emergency_fund', 'Fundusz awaryjny'),
        ('education', 'Edukacja'),
        ('other', 'Inne'),
    ]

    title = models.CharField(max_length=100)
    goal_type = models.CharField(max_length=50, choices=GOAL_CHOICES)
    target_amount = models.FloatField()  # Kwota do osiągnięcia
    current_amount = models.FloatField(default=0)  # Kwota zgromadzona do tej pory
    due_date = models.DateField()  # Termin realizacji celu
    user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE, related_name='savings_goals')
    created_at = models.DateTimeField(auto_now_add=True)

    # Kwota dodana przez użytkownika
    added_amount = models.FloatField(default=0)

    def progress(self):
        """Oblicza postęp w realizacji celu"""
        if self.target_amount is None or self.target_amount == 0:
            return 0  # Jeśli target_amount jest None lub 0, zwróć 0%
        return (self.current_amount / self.target_amount) * 100

    def __str__(self):
        return f'{self.title} - {self.progress()}%'

