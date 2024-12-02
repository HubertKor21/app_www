from django.contrib import admin

from .models import Team,Osoba,Person

# Register your models here.
admin.site.register(Team)
admin.site.register(Person)
admin.site.register(Osoba)