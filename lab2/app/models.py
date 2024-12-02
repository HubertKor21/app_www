from django.db import models
from django.core.exceptions import ValidationError
from datetime import date

# Create your models here.
MONTHS = models.IntegerChoices('Miesiace', 'Styczeń Luty Marzec Kwiecień Maj Czerwiec Lipiec Sierpień Wrzesień Październik Listopad Grudzień')

SHIRT_SIZES = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
    )


class Team(models.Model):
    name = models.CharField(max_length=60)
    country = models.CharField(max_length=2)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True) # Dodane pole 

    def __str__(self):
        return f"{self.name}"


class Person(models.Model):

    name = models.CharField(max_length=60)
    shirt_size = models.CharField(max_length=1, choices=SHIRT_SIZES, default=SHIRT_SIZES[0][0])
    month_added = models.IntegerField(choices=MONTHS.choices, default=MONTHS.choices[0][0])
    team = models.ForeignKey(Team, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name
    
class Coach(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField(null=True, blank=True)
    team = models.ForeignKey(Team,on_delete=models.CASCADE, null=True, blank=True)

class Position(models.Model):
    position_name = models.CharField(max_length=50)
    discription = models.TextField(blank=True, null=True)


class Osoba(models.Model):
    class Plec(models.IntegerChoices):
        KOBIETA = 1, 'Kobieta'
        MEZCZYZNA = 2, 'Mężczyzna'
        INNE = 3, 'Inne'

    gender = models.IntegerField(choices=Plec.choices, null=True, blank=True)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    published_date = models.DateField(default=date.today)

    def clean(self):
        # Walidacja pola name - tylko litery
        if not self.name.isalpha():
            raise ValidationError({'name': 'Nazwa może zawierać tylko litery.'})
        # Walidacja published_date - nie z przyszłości
        if self.published_date > date.today():
            raise ValidationError({'published_date': 'Data dodania nie może być z przyszłości.'})

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} {self.surname}"
