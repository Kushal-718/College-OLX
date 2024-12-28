from django.contrib import admin
from .models import CustomUser,Product



class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('college_email','username')

class ProductAdmin(admin.ModelAdmin):
        # overridding
     list_display = ('name', 'price', 'stock')


# Register your models here.
admin.site.register(CustomUser,CustomUserAdmin)
admin.site.register(Product,ProductAdmin)
