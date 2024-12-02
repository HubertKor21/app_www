from django.db import models
from accounts.models import CustomUserModel
from invitations.models import Family
# Create your models here.

class Loan(models.Model):
    LOAN_TYPE_CHOICES = [
        ('fixed', 'Stałe'),
        ('decreasing', 'Malejące')
    ]

    user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE,related_name="loans")
    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name='loans')
    name = models.CharField(max_length=255)
    amount_reaming = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, verbose_name="Kwota pozostała do spłaty")
    loan_type = models.CharField(max_length=10, choices=LOAN_TYPE_CHOICES, default='fixed', verbose_name="Rodzaj rat")
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, verbose_name="Oprocentowanie")
    payment_day = models.PositiveSmallIntegerField(verbose_name="Dzień płatności raty")  # Zakładając, że wartości będą od 1 do 31
    last_payment_date = models.DateField(verbose_name="Data spłaty ostatniej raty")
    installments_remaining = models.PositiveIntegerField(verbose_name="Pozostało rat")

    def __str__(self):
        return f"{self.name} - {self.amount_reaming} zł"
    
    class Meta:
        verbose_name = "Kredyt"
        verbose_name_plural = "Kredyty"
