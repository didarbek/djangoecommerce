from django.contrib import admin
from .models import Item,Category,Profile,Sex,Order,Address,ItemImage
<<<<<<< HEAD

=======
>>>>>>> 9a2ce80e773389f3c1ce4730100f21ba50285e13

# Register your models here.

@admin.register(Category)
class CategoryProfile(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug':('name',)}

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')

# @admin.register(Image)
# class ImageAdmin(admin.ModelAdmin):
#     list_display = ('id', 'item','image')
admin.site.register(ItemImage)
admin.site.register(Profile)
admin.site.register(Sex)
admin.site.register(Order)
admin.site.register(Address)
