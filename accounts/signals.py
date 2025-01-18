# accounts/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import SellerProfile

@receiver(post_save, sender=User)
def create_seller_profile(sender, instance, created, **kwargs):
    if created:  # Only create SellerProfile when a new User is created
        SellerProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_seller_profile(sender, instance, **kwargs):
    try:
        instance.sellerprofile.save()  # Save the SellerProfile after the user is created
    except SellerProfile.DoesNotExist:
        pass
