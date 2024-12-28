from django.urls import path
from .views import login_view, index,register,home,products_page


urlpatterns = [
    path('login/',login_view,name= 'login'),
    path('',index,name='index'),
    path('register/',register,name='register'),
    path('home/',home,name='home'),
    path('products_page/',products_page,name='products_page')
]