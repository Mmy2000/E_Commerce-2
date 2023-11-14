from django.shortcuts import render
from store.models import Product
from .models import HomeImage
from store.models import ReviewRating
# Create your views here.
def home(request,):
    products = Product.objects.all().filter(is_available=True).order_by('-created_at')[:12]
    image = HomeImage.objects.all()
    for product in products:
        reviews = ReviewRating.objects.filter(product_id=product.id , status=True)

    return render(request, 'settings/home.html',{
        'products' : products,
        'image':image,
        'reviews':reviews,
    })