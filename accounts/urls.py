from django.urls import path
from .views import login_view, index,register,home,products_page,add_product,cart_page,remove_from_cart,add_to_cart

urlpatterns = [
    path('login/',login_view,name= 'login'),
    path('',index,name='index'),
    path('register/',register,name='register'),
    path('home/',home,name='home'),
    path('products_page/',products_page,name='products_page'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart_page, name='cart_page'),
    path('remove_from_cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('add_product/',add_product,name='add_product')

]