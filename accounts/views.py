from django.conf import Settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages #to display messages
from accounts.forms import UserRegistrationForm
from .forms import CustomLoginPage
from .models import Product
from django.utils import timezone
from .forms import ProductForm
from .models_base import Badge,BadgeAward
from django.shortcuts import render, get_object_or_404, redirect
from .models import Order

def login_view(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = CustomLoginPage(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            college_email = form.cleaned_data.get('college_email')
            user = authenticate(request, username=username, password=password,college_email=college_email)
            if user is not None:
                login(request, user)
                #return HttpResponse("Succesfully logged in")
                return redirect('home')  # Redirect to a homepage or dashboard

            else:
                # Invalid credentials
                messages.error(request,'Invalid username or password.')
                # form.add_error(None, "Invalid username or password.")
                return render(request, 'login.html', {'form': form})
        else:
            print(form.errors)
            messages.error(request,'Please correct the errors below.')
            return render(request, 'login.html', {'form': form})

    else:
         # Form is invalid
        form = CustomLoginPage()
        return render(request, 'login.html', {'form': form})


def index(request):
    return render(request,'index.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('login')
        else:
            print(form.errors)  # Print the form errors in the below terminal for debugging
            messages.error(request,"Registration Failed.Please try again.")
            # return render(request, 'register.html', {'form': form})

    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})


# Home page view
@login_required
def home(request):
    # return HttpResponse
    request.session['visited_home'] = True  # Mark that the user visited the home page
    return render(request,'home.html')




@login_required
def products_page(request):
    # Check if the user visited the home page
    if not request.session.get('visited_home'):
            return redirect('home')  # Redirect to home page if not visited
    products = Product.objects.all()
    return render(request,'products_page.html',{'products' : products})




@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user  # Associate the product with the logged-in user
            product.save()
            return redirect('products_page')  # Redirect to the product list view
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})



# views.py for add to cart
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product

def add_to_cart(request, product_id):
    # Fetch the cart from the session or create a new one
    cart = request.session.get('cart', {})
    cart[product_id] = cart.get(product_id, 0) + 1  # Increment quantity
    request.session['cart'] = cart
    return redirect('cart_page')  # Redirect to the cart page

def cart_page(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())
    cart_items = [
        {
            'product': product,
            'quantity': cart[str(product.id)],
            'total_price': product.price * cart[str(product.id)],
        }
        for product in products
    ]
    cart_total = sum(item['total_price'] for item in cart_items)
    return render(request, 'cart_page.html', {'cart_items': cart_items, 'cart_total': cart_total})

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
    request.session['cart'] = cart
    return redirect('cart_page')




 # dashboard
from django.shortcuts import render
from .models_base import SellerProfile, Badge

from django.shortcuts import render
from django.contrib import messages
from .models import SellerProfile
from .badges import check_badges

from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models_base import Badge, BadgeAward


@login_required
def dashboard_view(request):
    seller_profile = request.user.sellerprofile
    new_badges = check_badges(seller_profile)

    # Get all badges with their status
    all_badges = Badge.objects.all()
    badges_with_status = []
    for badge in all_badges:
        earned = BadgeAward.objects.filter(seller=seller_profile, badge=badge).exists()
        progress = calculate_progress(seller_profile, badge)
        badges_with_status.append({
            'badge': badge,
            'earned': earned,
            'progress': progress
        })

    context = {
        'seller_profile': seller_profile,
        'badges_with_status': badges_with_status,
        'new_badges': new_badges,
        'level_progress': calculate_level_progress(seller_profile),
        'sales_to_next_level': calculate_sales_to_next_level(seller_profile),
        'active_listings': get_active_listings(seller_profile),
        'recent_activities': get_recent_activities(seller_profile),
    }

    if new_badges:
        messages.success(
            request,
            f'Congratulations! You\'ve earned {len(new_badges)} new badge(s)!'
        )

    return render(request, 'dashboard.html', context)


def calculate_level_progress(seller_profile):
    return (seller_profile.total_sales % 10) * 10


def calculate_sales_to_next_level(seller_profile):
    return 10 - (seller_profile.total_sales % 10)


def get_active_listings(seller_profile):
    return Product.objects.filter(seller=seller_profile, is_active=True).count()


def get_recent_activities(seller_profile):
    activities = []

    # Get recent sales
    recent_sales = Product.objects.filter(
        seller=seller_profile,
        is_sold=True
    ).order_by('-sold_date')[:5]

    for sale in recent_sales:
        activities.append({
            'type': 'sale',
            'action': f'Sold {sale.name} for ${sale.price}',
            'timestamp': sale.sold_date,
            'icon': 'fa-shopping-cart'
        })

    # Get recent badge awards
    recent_badges = BadgeAward.objects.filter(
        seller=seller_profile
    ).order_by('-awarded_at')[:3]

    for badge in recent_badges:
        activities.append({
            'type': 'badge',
            'action': f'Earned the {badge.badge.name} badge',
            'timestamp': badge.awarded_at,
            'icon': 'fa-award'
        })

    # Sort by timestamp and return most recent 5
    return sorted(activities, key=lambda x: x['timestamp'], reverse=True)[:5]


def check_badges(seller_profile):
    new_badges = []
    all_badges = Badge.objects.all()

    for badge in all_badges:
        if badge not in seller_profile.badges.all():
            if check_badge_eligibility(seller_profile, badge):
                seller_profile.badges.add(badge)
                BadgeAward.objects.create(seller=seller_profile, badge=badge)
                new_badges.append(badge)

    return new_badges


def check_badge_eligibility(seller_profile, badge):
    if badge.category == 'SALES':
        return seller_profile.total_sales >= badge.requirement
    elif badge.category == 'RATING':
        return seller_profile.rating >= (badge.requirement / 10)
    # Add other category checks as needed
    return False

# def dashboard_view(request):
#     seller_profile = request.user.sellerprofile
#     new_badges = check_badges(seller_profile)
#
#     context = {
#         'seller_profile': seller_profile,
#         'badges': seller_profile.badges.all(),
#         'new_badges': new_badges,
#         'level_progress': calculate_level_progress(seller_profile),
#         'sales_to_next_level': calculate_sales_to_next_level(seller_profile),
#         'active_listings': get_active_listings(seller_profile),
#         'recent_activities': get_recent_activities(seller_profile),
#     }
#
#     if new_badges:
#         messages.success(
#             request,
#             f'Congratulations! You\'ve earned {len(new_badges)} new badge(s)!'
#         )
#
#     return render(request, 'dashboard.html', context)
#
#
# # Helper functions for dashboard
# def calculate_level_progress(seller_profile):
#     # Add your level calculation logic
#     return (seller_profile.total_sales % 10) * 10
#
#
# def calculate_sales_to_next_level(seller_profile):
#     # Add your next level calculation logic
#     return 10 - (seller_profile.total_sales % 10)
#
#
# def get_active_listings(seller_profile):
#     # Add your active listings logic
#     return seller_profile.product_set.filter(is_active=True).count()
#
#
# def get_recent_activities(seller_profile):
#     # Add your recent activities logic
#     return []  # Replace with actual activity query


@login_required
def dashboard(request):
    try:
        # Attempt to fetch the SellerProfile for the logged-in user
        seller_profile = SellerProfile.objects.get(user=request.user)
    except SellerProfile.DoesNotExist:
        # If SellerProfile does not exist, create one
        seller_profile = SellerProfile.objects.create(user=request.user)

    # Now you can proceed with your dashboard logic
    return render(request, 'dashboard.html', {
        'seller_profile': seller_profile,
        'badges' : seller_profile.badges.all()
                                              })

def some_view(request):
    seller_profile, created = SellerProfile.objects.get_or_create(user=request.user)






# from django.shortcuts import render, get_object_or_404, redirect
# from .models import Product, Order
# from django.contrib.auth.decorators import login_required
#
# @login_required
# def place_order(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#
#     if request.method == 'POST':
#         quantity = int(request.POST['quantity'])
#
#         # Check if the requested quantity is available
#         if quantity > product.stock:
#             return render(request, 'error.html', {'message': 'Not enough stock available.'})
#
#         # Create the order
#         order = Order.objects.create(
#             product=product,
#             buyer=request.user,
#             quantity=quantity
#         )
#
#         # Decrease stock of the product
#         product.stock -= quantity
#         product.save()
#
#         # Redirect to a confirmation page or dashboard
#         return redirect('order_confirmation', order_id=order.id)
#
#     return render(request, 'place_order.html', {'product': product})
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order, Product, SellerProfile



# def place_order(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#
#     if request.method == 'POST':
#         quantity = int(request.POST.get('quantity'))
#
#         if quantity > product.stock:
#             # Handle insufficient stock
#             return render(request, 'insufficient_stock.html', {'product': product})
#
#         # Update product stock
#         product.stock -= quantity
#         product.save()
#
#         # Calculate total price
#         total_price = product.price * quantity
#
#         # Create the order
#         order = Order.objects.create(
#             user=request.user,
#             product=product,
#             quantity=quantity,
#             total_price=total_price
#         )
#
#         # Increment seller's sales count
#         seller_profile = product.seller.seller_profile
#         seller_profile.total_sales += quantity
#         seller_profile.save()
#
#         new_badges = evaluate_badges(seller_profile)
#         seller_profile.badges.set(new_badges)
#         seller_profile.save()
#         # Redirect to order confirmation page
#         return redirect('order_confirmation', order_id=order.id)
#
#     return redirect('product_detail', product_id=product.id)
# def place_order(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#
#     # Use seller_profile instead of sellerprofile
#     seller_profile = product.seller.seller_profile
#
#     if request.method == 'POST':
#         # Create order
#         order = Order.objects.create(
#             buyer=request.user,
#             seller=product.seller,
#             product=product,
#             # Add other order fields as needed
#         )
#
#         # Update seller stats
#         seller_profile.total_sales += 1
#         seller_profile.save()
#
#         # Update product status
#         product.is_sold = True
#         product.sold_date = timezone.now()
#         product.save()
#
#         # Check for new badges
#         check_badges(seller_profile)
#
#         messages.success(request, 'Order placed successfully!')
#         return redirect('order_confirmation')
#
#     context = {
#         'product': product,
#         'seller': product.seller,
#         'seller_profile': seller_profile,
#     }
#     return render(request, 'place_order.html', context)

from django.shortcuts import render, get_object_or_404


# def order_confirmation(request, order_id):
#     order = get_object_or_404(Order, id=order_id)
#
#     # Render the confirmation template with the order details
#     return render(request, 'order_confirmation.html', {'order': order})

from decimal import Decimal
from .models import Order


# def place_order(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     seller_profile = product.seller.seller_profile
#
#     # Check if product is already sold
#     if product.is_sold:
#         messages.error(request, 'Sorry, this product has already been sold.')
#         return redirect('product_detail', product_id=product_id)
#
#     # Check if user is trying to buy their own product
#     if request.user == product.seller:
#         messages.error(request, 'You cannot buy your own product.')
#         return redirect('product_detail', product_id=product_id)
#
#     if request.method == 'POST':
#         try:
#             # Create order
#             order = Order.objects.create(
#                 product=product,
#                 user=request.user,
#                 quantity=1,  # Default to 1 or get from form if you have quantity field
#                 total_price=product.price  # Or calculate based on quantity
#             )
#
#             # Update seller stats
#             seller_profile.total_sales += 1
#             seller_profile.save()
#
#             # Update product status
#             product.is_sold = True
#             product.sold_date = timezone.now()
#             product.save()
#
#             # Check for new badges
#             check_badges(seller_profile)
#
#             messages.success(request, 'Order placed successfully!')
#             return redirect('order_confirmation', order_id=order.id)
#
#         except Exception as e:
#             messages.error(request, f'Error placing order: {str(e)}')
#             return redirect('product_detail', product_id=product_id)
#
#     context = {
#         'product': product,
#         'seller': product.seller,
#         'seller_profile': seller_profile,
#     }
#     return render(request, 'place_order.html', context)
@login_required
def place_order(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    seller_profile = product.seller.seller_profile

    # Check if product is out of stock
    if product.stock <= 0:
        messages.error(request, 'Sorry, this product is out of stock.')
        return redirect('product_detail', product_id=product_id)

    # Check if user is trying to buy their own product
    if request.user == product.seller:
        messages.error(request, 'You cannot buy your own product.')
        return redirect('product_detail', product_id=product_id)

    if request.method == 'POST':
        try:
            quantity = 1  # Default to 1 or get from form if you have quantity field

            # Check if requested quantity is available
            if quantity > product.stock:
                messages.error(request, 'Requested quantity not available.')
                return redirect('product_detail', product_id=product_id)

            # Calculate total price
            total_price = product.price * quantity

            # Create order
            order = Order.objects.create(
                product=product,
                user=request.user,
                quantity=quantity,
                total_price=total_price
            )

            # Update product stock
            product.stock -= quantity
            if product.stock == 0:
                product.is_sold = True
                product.sold_date = timezone.now()
            product.save()

            # Update seller stats
            seller_profile.total_sales += 1
            seller_profile.save()

            # Check for new badges
            check_badges(seller_profile)

            messages.success(request, 'Order placed successfully!')
            return redirect('order_confirmation', order_id=order.id)

        except Exception as e:
            messages.error(request, f'Error placing order: {str(e)}')
            return redirect('product_detail', product_id=product_id)

    context = {
        'product': product,
        'seller': product.seller,
        'seller_profile': seller_profile,
    }
    return render(request, 'place_order.html', context)

@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_confirmation.html', {'order': order})

from django.shortcuts import render, get_object_or_404
from .models import Product


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    return render(request, 'product_detail.html', {'product': product})


from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Method 1: Simple logout view
@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return render(request, 'logout.html')


# Method 2: More comprehensive logout view with next page handling
@login_required
def logout_view(request):
    """Handle user logout with next page redirect and session cleanup"""
    # Store any messages or data you want to persist after logout
    messages.success(request, 'You have been successfully logged out.')

    # Get next page URL if provided
    next_page = request.GET.get('next', 'home')

    # Clear any custom session data if you have any
    # request.session.pop('cart', None)  # Example: clearing shopping cart

    # Logout the user
    logout(request)

    # If AJAX request, return JSON response
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success', 'message': 'Logged out successfully'})

    # For regular requests, render the logout page
    return render(request, 'logout.html', {
        'next_page': next_page,
    })


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Badge, BadgeAward


@login_required
def view_badges(request):
    # Get user's earned badges
    earned_badges = Badge.objects.filter(badgeaward__seller=request.user.seller_profile)

    # Get all available badges
    all_badges = Badge.objects.all()

    # Create a list of badges with earned status
    badges_with_status = []
    for badge in all_badges:
        badges_with_status.append({
            'badge': badge,
            'earned': badge in earned_badges,
            'progress': calculate_progress(request.user.seller_profile, badge)
        })

    context = {
        'badges_with_status': badges_with_status,
    }
    return render(request, 'badges.html', context)


def calculate_progress(seller_profile, badge):
    """Calculate progress towards earning a badge"""
    if badge.category == 'SALES':
        return min(100, (seller_profile.total_sales / badge.requirement) * 100)
    elif badge.category == 'RATING':
        return min(100, (float(seller_profile.rating) / (badge.requirement / 10)) * 100)
    # Add other category calculations as needed
    return 0