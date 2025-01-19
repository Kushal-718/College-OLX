from django.urls import path
from .views import login_view, index, register, home, products_page, add_product, cart_page, remove_from_cart, \
    add_to_cart, dashboard, place_order, order_confirmation, product_detail, logout_view,view_badges

urlpatterns = [
    path('login/',login_view,name= 'login'),
    path('',index,name='index'),
    path('logout/',logout_view,name="logout"),
    path('register/',register,name='register'),
    path('home/',home,name='home'),
    path('products_page/',products_page,name='products_page'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart_page, name='cart_page'),
    path('remove_from_cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('dashboard/', dashboard, name='dashboard'),
    path('add_product/',add_product,name='add_product'),
    path('place_order/<int:product_id>/', place_order, name='place_order'),
    path('order_confirmation/<int:order_id>/', order_confirmation, name='order_confirmation'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
path('badges/', view_badges, name='badges'),

]