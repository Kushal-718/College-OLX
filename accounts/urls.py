from django.urls import path
from .views import login_view, index,register,home,products_page,add_product


urlpatterns = [
    path('login/',login_view,name= 'login'),
    path('',index,name='index'),
    path('register/',register,name='register'),
    path('home/',home,name='home'),
    path('products_page/',products_page,name='products_page'),
    path('add_product/',add_product,name='add_product')
]