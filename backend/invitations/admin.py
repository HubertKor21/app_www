from django.contrib import admin
from .models import Family, Invite

class FamilyAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'created_by','member_count')  # Display fields
    search_fields = ('name',)
class InviteAdmin(admin.ModelAdmin):
    list_display = ('email', 'family', 'is_accepted', 'created_at')  # Display fields
    search_fields = ('email', 'family__name')  # Searching by email and family name
    list_filter = ('is_accepted', 'created_at')  # Filtering by acceptance status and created_at

# Register models with admin
admin.site.register(Family, FamilyAdmin)
admin.site.register(Invite, InviteAdmin)
