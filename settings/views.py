from django.shortcuts import render
from store.models import Product
# Create your views here.
def home(request):
    product = Product.objects.all().filter(is_available=True)

    return render(request, 'settings/home.html',{
        'product' : product
    })