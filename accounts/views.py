from django.conf import Settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages #to display messages
from accounts.forms import UserRegistrationForm
from .forms import CustomLoginPage
from .models import Product
from .forms import ProductForm

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
            product.user = request.user  # Associate the product with the logged-in user
            product.save()
            return redirect('product_page')  # Redirect to the product list view
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})