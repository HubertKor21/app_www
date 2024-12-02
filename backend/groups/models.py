from django.db import models
from django.db.models import Sum
from django.dispatch import receiver
from accounts.models import CustomUserModel
from invitations.models import Family
from transactions.models import Bank
from django.db.models.signals import m2m_changed

# Create your models here.

class Category(models.Model):
    CATEGORY_TYPE_CHOICES = [
        ('expense', 'Wydatki'),
        ('income', 'Przychody'),
    ]

    category_title = models.CharField(max_length=50)
    category_note = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    assigned_amount = models.FloatField(default=0)
    category_type = models.CharField(max_length=7, choices=CATEGORY_TYPE_CHOICES, default='expense')
    category_author = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE, null=True, blank=True)
    bank = models.ForeignKey(Bank, on_delete=models.SET_NULL, null=True, blank=True)  # Zmieniono na przypisanie banku do kategorii


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.category_author and self.category_type == "expense":
            if self.bank:  # Check if the category has a specific bank assigned
                self.bank.balance -= self.assigned_amount
                self.bank.save()

        if self.category_type == "income":
            if self.bank:
                self.bank.balance += self.assigned_amount
                self.bank.save()



class Groups(models.Model):
    groups_title = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    groups_author = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE, related_name='authored_groups')
    categories = models.ManyToManyField(Category, related_name='groups')  # Zmiana z ForeignKey na ManyToManyField
    family = models.ForeignKey(Family, on_delete=models.CASCADE, null=True,blank=True)

    def get_total_expenses(self):
        return self.categories.aggregate(Sum('assigned_amount'))['assigned_amount__sum'] or 0


    def get_total_income(self):
        """Zlicza sumę przychodów (assigned_amount) w grupie"""
        return self.categories.filter(category_type='income').aggregate(total_income=Sum('assigned_amount'))['total_income'] or 0

    def get_balance(self):
        """Zlicza różnicę między przychodami a wydatkami"""
        total_expenses = self.get_total_expenses()
        total_income = self.get_total_income()
        return total_income - total_expenses
    
    def category_count(self):
        return self.categories.count()
    
@receiver(m2m_changed, sender=Groups.categories.through)
def update_balance_on_category_assignment(sender, instance, action, **kwargs):
    if action in ["post_add", "post_remove", "post_clear"]:
        for category in instance.categories.filter(category_type='expense'):
            if category.bank:  # Sprawdzamy, czy kategoria ma przypisany bank
                category.bank.save()