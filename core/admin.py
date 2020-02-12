from django.contrib import admin
from .models import Item, Category,Profile

# Register your models here.

@admin.register(Category)
class CategoryProfile(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Item)
admin.site.register(Profile)
