from django.contrib import admin
from .models import Item,Category,Profile,Sex,Order,Address

# Register your models here.

@admin.register(Category)
class CategoryProfile(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Item)
admin.site.register(Profile)
admin.site.register(Sex)
admin.site.register(Order)
admin.site.register(Address)
