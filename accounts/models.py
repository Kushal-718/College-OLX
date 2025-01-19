from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models_base import SellerProfile, Badge, BadgeAward

# Re-export the models
__all__ = ['SellerProfile', 'Badge', 'BadgeAward']

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_seller_profile(sender, instance, created, **kwargs):
    if created:
        SellerProfile.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_seller_profile(sender, instance, **kwargs):
    instance.seller_profile.save()

class CustomUser(AbstractUser):
    college_email = models.EmailField(unique=True)
    #username and password are present by default



class Product(models.Model):#inheritance
    # CATEGORY_CHOICES = [
    #     ('book', 'Book'),
    #     ('electronics', 'Electronics'),
    #     ('clothing', 'Clothing'),
    #     # Add more categories as needed
    # ]
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='product_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    is_sold = models.BooleanField(default=False)  # Add this field
    sold_date = models.DateTimeField(null=True, blank=True)  # Add this field too
    # category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)


    def __str__(self):
        return self.name

#
# from django.db import models
# from django.conf import settings  # Import settings instead of User directly
#
#
# class Badge(models.Model):
#     BADGE_CATEGORIES = [
#         ('SALES', 'Sales Milestone'),
#         ('RATING', 'Rating Achievement'),
#         ('CATEGORY', 'Category Specialist'),
#         ('PERFORMANCE', 'Performance'),
#         ('SPECIAL', 'Special Achievement')
#     ]
#
#     name = models.CharField(max_length=100)
#     description = models.TextField()
#     image = models.ImageField(upload_to='badges/')
#     requirement = models.IntegerField()
#     # Add default value here
#     category = models.CharField(
#         max_length=50,
#         choices=BADGE_CATEGORIES,
#         default='SALES'  # Adding default value
#     )
#     created_at = models.DateTimeField(
#         auto_now_add=True,
#         default = timezone.now  # Add this default
#     )
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         ordering = ['requirement']
# from django.db import models
# from django.conf import settings
# from django.utils import timezone
#
# class Badge(models.Model):
#     BADGE_CATEGORIES = [
#         ('SALES', 'Sales Milestone'),
#         ('RATING', 'Rating Achievement'),
#         ('CATEGORY', 'Category Specialist'),
#         ('PERFORMANCE', 'Performance'),
#         ('SPECIAL', 'Special Achievement')
#     ]
#
#     name = models.CharField(max_length=100)
#     description = models.TextField()
#     image = models.ImageField(upload_to='badges/')
#     requirement = models.IntegerField()
#     category = models.CharField(
#         max_width=50,
#         choices=BADGE_CATEGORIES,
#         default='SALES'
#     )
#     # Fixed: Use only default, not auto_now_add
#     created_at = models.DateTimeField(default=timezone.now)
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
# #         ordering = ['requirement']
from django.db import models
from django.conf import settings
from django.utils import timezone


# class Badge(models.Model):
#     BADGE_CATEGORIES = [
#         ('SALES', 'Sales Milestone'),
#         ('RATING', 'Rating Achievement'),
#         ('CATEGORY', 'Category Specialist'),
#         ('PERFORMANCE', 'Performance'),
#         ('SPECIAL', 'Special Achievement')
#     ]
#
#     name = models.CharField(max_length=100)
#     description = models.TextField()
#     image = models.ImageField(upload_to='badges/')
#     requirement = models.IntegerField(default=1)
#     category = models.CharField(
#         max_length=50,
#         choices=BADGE_CATEGORIES,
#         default='SALES'
#     )
#     created_at = models.DateTimeField(default=timezone.now)
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         ordering = ['requirement']
#
#
# # class SellerProfile(models.Model):
# #     user = models.OneToOneField(
# #         settings.AUTH_USER_MODEL,
# #         on_delete=models.CASCADE,
# #         related_name='seller_profile'
# #     )
# #     # Remove the through parameter initially
# #     badges = models.ManyToManyField(Badge)
# #     total_sales = models.IntegerField(default=0)
# #     rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
# #     response_time = models.DurationField(null=True)
# #     level = models.IntegerField(default=1)
#     class SellerProfile(models.Model):
#         user = models.OneToOneField(
#             settings.AUTH_USER_MODEL,
#             on_delete=models.CASCADE,
#             related_name='seller_profile'
#         )
#         badges = models.ManyToManyField('Badge', through='BadgeAward', blank=True)
#         total_sales = models.IntegerField(default=0)
#         rating = models.DecimalField(
#             max_digits=3,
#             decimal_places=2,
#             default=0.00
#         )
#         response_time = models.DurationField(null=True, blank=True)
#         level = models.IntegerField(default=1)
#     last_badge_check = models.DateTimeField(default=timezone.now)
#
#     def __str__(self):
#         return f"{self.user.username}'s Profile"


# We'll add this in a separate migration
# class BadgeAward(models.Model):
#     seller = models.ForeignKey('SellerProfile', on_delete=models.CASCADE)
#     badge = models.ForeignKey('Badge', on_delete=models.CASCADE)
#     awarded_at = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         unique_together = ('seller', 'badge')


# from django.db import models
# from django.conf import settings
# from django.utils import timezone
#
# class Badge(models.Model):
#     BADGE_CATEGORIES = [
#         ('SALES', 'Sales Milestone'),
#         ('RATING', 'Rating Achievement'),
#         ('CATEGORY', 'Category Specialist'),
#         ('PERFORMANCE', 'Performance'),
#         ('SPECIAL', 'Special Achievement')
#     ]
#
#     name = models.CharField(max_length=100)
#     description = models.TextField()
#     image = models.ImageField(upload_to='badges/')
#     requirement = models.IntegerField(default=1)
#     category = models.CharField(
#         max_length=50,  # Fixed: max_length instead of max_width
#         choices=BADGE_CATEGORIES,
#         default='SALES'
#     )
#     created_at = models.DateTimeField(default=timezone.now)
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         ordering = ['requirement']
#
# class SellerProfile(models.Model):
#     # Update this line to use settings.AUTH_USER_MODEL
#     user = models.OneToOneField(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name='seller_profile'  # Added for easier reverse lookup
#     )
#     badges = models.ManyToManyField(Badge, through='BadgeAward')
#     total_sales = models.IntegerField(default=0)
#     rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
#     response_time = models.DurationField(null=True)
#     level = models.IntegerField(default=1)
#     last_badge_check = models.DateTimeField(default=timezone.now)
#
#     def __str__(self):
#         return f"{self.user.username}'s Profile"
#
#
# class BadgeAward(models.Model):
#     seller = models.ForeignKey(SellerProfile, on_delete=models.CASCADE)
#     badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
#     awarded_at = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         unique_together = ('seller', 'badge')


# from django.db import models
# from django.contrib.auth.models import User
#
#
# class Badge(models.Model):
#     BADGE_CATEGORIES = [
#         ('SALES', 'Sales Milestone'),
#         ('RATING', 'Rating Achievement'),
#         ('CATEGORY', 'Category Specialist'),
#         ('PERFORMANCE', 'Performance'),
#         ('SPECIAL', 'Special Achievement')
#     ]
#
#     name = models.CharField(max_length=100)
#     description = models.TextField()
#     image = models.ImageField(upload_to='badges/')
#     requirement = models.IntegerField()
#     category = models.CharField(max_length=50, choices=BADGE_CATEGORIES)
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         ordering = ['requirement']
#
#
# class SellerProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     badges = models.ManyToManyField(Badge, through='BadgeAward')
#     total_sales = models.IntegerField(default=0)
#     rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
#     response_time = models.DurationField(null=True)
#     level = models.IntegerField(default=1)
#     last_badge_check = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"{self.user.username}'s Profile"
#
#
# class BadgeAward(models.Model):
#     seller = models.ForeignKey(SellerProfile, on_delete=models.CASCADE)
#     badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
#     awarded_at = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         unique_together = ('seller', 'badge')


# models.py
# from django.db import models
# from django.contrib.auth.models import User
#
#
# class Badge(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField()
#     image = models.ImageField(upload_to='badges/')
#     requirement = models.IntegerField()
#     category = models.CharField(max_length=50)
#
#     class Meta:
#         ordering = ['requirement']
#
# # class Badge(models.Model):
# #     name = models.CharField(max_length=100)
# #     description = models.TextField()
# #     image = models.ImageField(upload_to="badges/")
# #     # criteria = models.CharField(max_length=100, unique=True)  # Python code for criteria logic
# #
# #     def __str__(self):
# #         return self.name
#
# # class SellerProfile(models.Model):
# #     user = models.OneToOneField(User, on_delete=models.CASCADE)
# #     badges = models.ManyToManyField(Badge, blank=True)  # Sellers can earn multiple badges.
# #     total_sales = models.IntegerField(default=0)
# #
# #     def __str__(self):
# #         return self.user.username
#
# from django.conf import settings
#
# class SellerProfile(models.Model):
#     user = models.OneToOneField(User)
#     badges = models.ManyToManyField(Badge)
#     total_sales = models.IntegerField(default=0)
#     rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
#     response_time = models.DurationField(null=True)
#
#     def __str__(self):
#         return self.user.username
#

from django.db import models
from django.conf import settings
from django.db.models import F

class Order(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)  # The product being sold
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # The user who bought the product
    quantity = models.PositiveIntegerField()  # Number of items bought
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # Total price for the order
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the order was created

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
