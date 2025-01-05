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


# admin.py
from django.contrib import admin
from .models import Badge, SellerProfile

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'criteria')

@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_sales')
