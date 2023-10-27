from django.shortcuts import render , get_object_or_404
from .models import Product
from category.models import Category
from carts.models import CartItem
from carts.views import _cart_id
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator

# Create your views here.

def store(request , category_slug=None):
    categories = None
    product = None

    if category_slug != None :
        categories = get_object_or_404(Category , slug = category_slug )
        product = Product.objects.filter(category=categories,is_available=True)
        product_count = product.count()

    else:
        product = Product.objects.all().filter(is_available=True)
        paginator = Paginator(product,2)
        page = request.GET.get('page')
        paged_product = paginator.get_page(page)
        product_count = product.count()

    context = {
        'product' : paged_product ,
        'product_count' : product_count
    }
    return render(request , 'store/store.html',context)


def product_detail(request,category_slug,product_slug):
    try :
        single_product = Product.objects.get(category__slug=category_slug,slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()
    except Exception as e:
        raise e
    context = {
        'single_product':single_product,
        'in_cart':in_cart,
    }
    return render(request,'store/product_detail.html',context)