from django.contrib import admin

from transactions.models import Bank
from .models import Groups, Category
from django import forms


# Define a custom form for the intermediary model
class GroupsCategoriesForm(forms.ModelForm):
    category_title = forms.CharField(max_length=50, required=False, disabled=True)
    category_note = forms.CharField(max_length=200, required=False, disabled=True)
    assigned_amount = forms.FloatField(required=False, disabled=True)
    category_type = forms.ChoiceField(choices=Category.CATEGORY_TYPE_CHOICES, required=False, disabled=True)
    bank = forms.ModelChoiceField(queryset=Bank.objects.all(), required=False, disabled=True)

    class Meta:
        model = Groups.categories.through
        fields = ['category', 'category_title', 'category_note', 'assigned_amount', 'category_type', 'bank']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate fields based on the related Category instance
        if self.instance.pk:
            category = self.instance.category  # Access the related Category
            self.fields['category_title'].initial = category.category_title
            self.fields['category_note'].initial = category.category_note
            self.fields['assigned_amount'].initial = category.assigned_amount
            self.fields['category_type'].initial = category.category_type
            self.fields['bank'].initial = category.bank

# Inline for Category model in the Groups admin
class CategoryInline(admin.TabularInline):
    model = Groups.categories.through  # This is the intermediary model
    extra = 1
    form = GroupsCategoriesForm  # Use the custom form to display Category fields

# Admin for Groups
class GroupsAdmin(admin.ModelAdmin):
    inlines = [CategoryInline]  # Add CategoryInline to the Groups admin
    list_display = ['groups_title', 'groups_author', 'created_at', 'family']
    search_fields = ['groups_title', 'groups_author__email']

# Admin for Category
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','category_title', 'category_note', 'assigned_amount', 'category_type', 'category_author', 'bank', 'created_at']
    search_fields = ['category_title', 'category_author__email']

# Register models with Django admin
admin.site.register(Groups, GroupsAdmin)
admin.site.register(Category, CategoryAdmin)
