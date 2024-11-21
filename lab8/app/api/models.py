from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
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

    def __str__(self):
        return f"{self.name}"


class Person(models.Model):

    name = models.CharField(max_length=60)
    shirt_size = models.CharField(max_length=1, choices=SHIRT_SIZES, default=SHIRT_SIZES[0][0])
    month_added = models.IntegerField(choices=MONTHS.choices, default=MONTHS.choices[0][0])
    team = models.ForeignKey(Team, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name
    
class Position(models.Model):
    position_name = models.CharField(max_length=50)
    discription = models.TextField(blank=True, null=True)

class Osoba(models.Model):
    # GENDER_CHOICE = (
    #     ('K', 'Kobieta'),
    #     ('M', 'Mężczyzna'),
    #     ('I', 'Inne')
    # )
    class Plec(models.IntegerChoices):
        KOBIETA = 1, 'Kobieta'
        MEZCZYZNA = 2, 'Mężczyzna'
        INNE = 3, 'Inne'

    gender = models.IntegerField(choices=Plec.choices, null=True , blank=True)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    # gender = models.CharField(max_length=1, choices=GENDER_CHOICE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    published_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.name} {self.surname}"
    
    def clean(self):
        if not self.name.isalpha():
            raise ValidationError("Nazwa moze zawierac tylko litery")
        if self.published_date > timezone.now().date():
            raise ValidationError("Data dodania nie moze byc z przyszłości")