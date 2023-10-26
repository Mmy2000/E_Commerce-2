from django.shortcuts import render
from .models import Product
# Create your views here.

def store(request):
    product = Product.objects.all().filter(is_available=True)
    product_count = product.count()

    context = {
        'product' : product ,
        'product_count' : product_count
    }
    return render(request , 'store/store.html',context)