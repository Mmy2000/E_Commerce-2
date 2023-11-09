from django.shortcuts import render
from store.models import Product
from .models import HomeImage
# Create your views here.
def home(request):
    product = Product.objects.all().filter(is_available=True)
    image = HomeImage.objects.all()

    return render(request, 'settings/home.html',{
        'product' : product,
        'image':image,
    })