from django.shortcuts import render , get_object_or_404
from .models import Product
from category.models import Category
from carts.models import CartItem
from carts.views import _cart_id
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.db.models.query_utils import Q


# Create your views here.

def store(request , category_slug=None):
    categories = None
    product = None

    if category_slug != None :
        categories = get_object_or_404(Category , slug = category_slug )
        product = Product.objects.filter(category=categories,is_available=True)
        paginator = Paginator(product,1)
        page = request.GET.get('page')
        paged_product = paginator.get_page(page)
        product_count = product.count()

    else:
        product = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(product,6)
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

def search(request):
    if 'q' in request.GET:
        q = request.GET['q']
        if q :
            product = Product.objects.order_by('-created_at').filter(
                Q(description__icontains=q ) |
                Q( name__icontains=q)
                )
            product_count = product.count()
        else :
            return render(request , 'store/store.html')
    context = {
        'product':product , 
        'product_count':product_count
    }
    return render(request , 'store/store.html', context)