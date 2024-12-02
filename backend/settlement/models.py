from django.db import models
from accounts.models import CustomUserModel
from invitations.models import Family

class Settlement(models.Model):
    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name="settlements")
    debtor = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE, related_name="debtor_settlements")
    creditor = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE, related_name="creditor_settlements")
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.debtor} -> {self.creditor}: {self.amount} PLN ({'Paid' if self.is_paid else 'Unpaid'})"
