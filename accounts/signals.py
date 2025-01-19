from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models_base import SellerProfile

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_seller_profile(sender, instance, created, **kwargs):
    if created:
        # Only create if it doesn't exist
        SellerProfile.objects.get_or_create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_seller_profile(sender, instance, **kwargs):
    try:
        # Only save if profile exists
        if hasattr(instance, 'seller_profile'):
            instance.seller_profile.save()
    except SellerProfile.DoesNotExist:
        pass