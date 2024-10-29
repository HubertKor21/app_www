from django.contrib import admin
from .models import Person,Coach,Team,Osoba,Position

# Register your models here.
admin.site.register(Person)
admin.site.register(Coach)
admin.site.register(Team)
admin.site.register(Position)

# @admin.register(Osoba)
# class OsobaAdmin(admin.ModelAdmin):
#     readonly_fields = ('data_dodania',)

# class OsobaAdmin(admin.ModelAdmin):
#     list_display = ('imie', 'nazwisko', 'plec', 'stanowisko')

@admin.register(Osoba)
class OsobaAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'gender', 'position_id_display')

    @admin.display(ordering='position__id', description='Stanowisko (id)')
    def position_id_display(self, obj):
        return f"{obj.position} ({obj.position.id})"

class OsobaAdmin(admin.ModelAdmin):
    list_filter = ('stanowisko', 'data_dodania')

class StanowiskoAdmin(admin.ModelAdmin):
    list_filter = ('nazwa',)