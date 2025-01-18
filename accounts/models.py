from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


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
    # category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)


    def __str__(self):
        return self.name




# models.py
from django.db import models
from django.contrib.auth.models import User

class Badge(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to="badges/")
    criteria = models.TextField()  # Explain criteria for earning this badge.

    def __str__(self):
        return self.name

# class SellerProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     badges = models.ManyToManyField(Badge, blank=True)  # Sellers can earn multiple badges.
#     total_sales = models.IntegerField(default=0)
#
#     def __str__(self):
#         return self.user.username

from django.conf import settings

class SellerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    badges = models.ManyToManyField(Badge, blank=True)  # Sellers can earn multiple badges.
    total_sales = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username
