from django.urls import path
from . views import carts , add_cart , remove_cart , remove_cart_item

app_name = 'carts'

urlpatterns = [
    path('', carts ,name = 'cart'),
    path('add_cart/<int:product_id>/', add_cart ,name = 'add_cart'),
    path('remove_cart/<int:product_id>/', remove_cart ,name = 'remove_cart'),
    path('remove_cart_item/<int:product_id>/', remove_cart_item ,name = 'remove_cart_item'),
]