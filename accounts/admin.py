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

from django.contrib import admin
from .models import Badge, SellerProfile, BadgeAward

admin.site.register(Badge)
admin.site.register(SellerProfile)
admin.site.register(BadgeAward)
# # admin.py
# from django.contrib import admin
# from .models import Badge, SellerProfile
#
# @admin.register(Badge)
# class BadgeAdmin(admin.ModelAdmin):
#     list_display = ('name', 'description')
#
# @admin.register(SellerProfile)
# class SellerProfileAdmin(admin.ModelAdmin):
#     list_display = ('user', 'total_sales')


# admin.site.register(SellerProfile,SellerProfileAdmin)
# admin.site.register(Badge,BadgeAdmin)