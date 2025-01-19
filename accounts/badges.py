from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
from .models import Badge, BadgeAward


def check_badges(seller_profile):
    """Check all badge criteria and award new badges"""
    new_badges = []

    # Prevent checking too frequently
    if timezone.now() - seller_profile.last_badge_check < timedelta(hours=1):
        return []

    # Sales Milestone Badges
    sales_badges = {
        'First Sale': 1,
        'Rising Star': 10,
        'Super Seller': 50,
        'Elite Seller': 100,
        'Master Seller': 500
    }

    for badge_name, requirement in sales_badges.items():
        if seller_profile.total_sales >= requirement:
            badge = add_badge(seller_profile, badge_name, 'SALES')
            if badge:
                new_badges.append(badge)

    # Rating Badges
    if seller_profile.rating >= 4.5:
        badge = add_badge(seller_profile, 'Top Rated', 'RATING')
        if badge:
            new_badges.append(badge)

    # Category Specialist Badges
    category_sales = get_category_sales(seller_profile)
    for category, sales in category_sales.items():
        if sales >= 10:
            badge_name = f'{category.title()} Expert'
            badge = add_badge(seller_profile, badge_name, 'CATEGORY')
            if badge:
                new_badges.append(badge)

    # Update last check time
    seller_profile.last_badge_check = timezone.now()
    seller_profile.save()

    return new_badges


def add_badge(seller_profile, badge_name, category):
    """Add a badge if it doesn't exist"""
    try:
        badge = Badge.objects.get(name=badge_name)
        _, created = BadgeAward.objects.get_or_create(
            seller=seller_profile,
            badge=badge
        )
        if created:
            return badge
    except Badge.DoesNotExist:
        return None


def get_category_sales(seller_profile):
    """Get sales count per category"""
    return (Order.objects.filter(seller=seller_profile)
            .values('product__category')
            .annotate(total=Count('id'))
            .filter(total__gte=10))