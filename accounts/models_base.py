from django.db import models
from django.conf import settings
from django.utils import timezone


class Badge(models.Model):
    BADGE_CATEGORIES = [
        ('SALES', 'Sales Milestone'),
        ('RATING', 'Rating Achievement'),
        ('CATEGORY', 'Category Specialist'),
        ('PERFORMANCE', 'Performance'),
        ('SPECIAL', 'Special Achievement')
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='badges/')
    requirement = models.IntegerField(default=1)
    category = models.CharField(
        max_length=50,
        choices=BADGE_CATEGORIES,
        default='SALES'
    )
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['requirement']


class SellerProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='seller_profile'
    )
    badges = models.ManyToManyField(Badge, blank=True)
    total_sales = models.IntegerField(default=0)
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.00
    )
    response_time = models.DurationField(null=True, blank=True)
    level = models.IntegerField(default=1)
    last_badge_check = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class BadgeAward(models.Model):
    seller = models.ForeignKey(SellerProfile, on_delete=models.CASCADE)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    awarded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('seller', 'badge')

    def __str__(self):
         return f"{self.seller.user.username} - {self.badge.name}"