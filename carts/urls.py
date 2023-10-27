from django.urls import path
from . views import carts , add_cart

app_name = 'carts'

urlpatterns = [
    path('', carts ,name = 'cart'),
    path('add_cart/<int:product_id>/', add_cart ,name = 'add_cart'),
]