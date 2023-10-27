from django.urls import path
from . views import carts 

app_name = 'carts'

urlpatterns = [
    path('', carts ,name = 'cart'),
]