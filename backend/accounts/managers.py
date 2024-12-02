from django.contrib.auth.models import BaseUserManager
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class CustomUserManager(BaseUserManager):
    
    def email_validation(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError("You must provide a valid email")

    def create_user(self, email, first_name, last_name=None, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is a required field")
        else:
            self.email_validation(email)
            clean_email = self.normalize_email(email)

        if not first_name:
            raise ValueError("First name is a required field")
        
        user = self.model(
            email=clean_email,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        user.set_password(password)
        user.is_active = extra_fields.get("is_active", True)
        user.is_staff = extra_fields.get("is_staff", False)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name=None, password=None, **extra_fields):
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)

        if not email:
            raise ValueError("Email is a required field")
        else:
            self.email_validation(email)
            clean_email = self.normalize_email(email)

        if not first_name:
            raise ValueError("First name is a required field")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")

        return self.create_user(clean_email, first_name, last_name, password, **extra_fields)
