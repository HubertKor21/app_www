from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from invitations.models import Family
from .managers import CustomUserManager


# Create your models here.
class CustomUserModel(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(unique=True,max_length=255)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100,null=True,blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateField(auto_now=True)
    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name="members_of_family", null=True, blank=True)
    budget = models.FloatField(default=0)  # Miesięczny budżet użytkownika

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    