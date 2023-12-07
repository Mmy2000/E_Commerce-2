from django.shortcuts import render , get_object_or_404 , redirect
from .models import Product , ReviewRating , ProductGallary
from category.models import Category
from carts.models import CartItem
from orders.models import OrderProduct
from carts.views import _cart_id
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.db.models.query_utils import Q
from .forms import ReviewForm
from django.contrib import messages



# Create your views here.

def store(request , category_slug=None ):
    categories = None
    products = None
    

    if category_slug != None :
        categories = get_object_or_404(Category , slug = category_slug )
        products = Product.objects.filter(category=categories,is_available=True).order_by('-created_at')
        for product in products:
            reviews = ReviewRating.objects.filter(product_id=product.id , status=True)
        paginator = Paginator(products,6)
        page = request.GET.get('page')
        paged_product = paginator.get_page(page)
        product_count = products.count()
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')

        if min_price:
            products = products.filter(price=min_price)

        if max_price:
            products = products.filter(price=max_price)

    else:
        products = Product.objects.all().filter(is_available=True).order_by('-created_at')
        for product in products:
            reviews = ReviewRating.objects.filter(product_id=product.id , status=True)
        paginator = Paginator(products,6)
        page = request.GET.get('page')
        paged_product = paginator.get_page(page)
        product_count = products.count()
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')

        if min_price:
            products = products.filter(price=min_price)

        if max_price:
            products = products.filter(price=max_price)

    context = {
        'products' : paged_product ,
        'product_count' : product_count,
        'reviews':reviews,
    }
    return render(request , 'store/store.html',context)

def product_by_price(request):
    products = Product.objects.filter(is_available=True)

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if min_price:
            products = products.filter(price__gte=min_price)

    if max_price:
            products = products.filter(price__lte=max_price)
        
    context = {'products': products}
    return render(request , 'store/store.html',context)

def product_by_size(request):
    products = Product.objects.filter(is_available=True)
    variation_name = request.GET.get('variation_name')
    if variation_name:
        products = products.filter(variation__variation_value__icontains=variation_name)
    context = {'products':products}
    return render(request , 'store/store.html',context)


def product_detail(request,category_slug,product_slug):
    try :
        single_product = Product.objects.get(category__slug=category_slug,slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()
    except Exception as e:
        raise e
    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(user=request.user , product_id=single_product.id).exists()
        except OrderProduct.DoesNotExist:
            orderproduct = None
    else :
        orderproduct = None
    
    orderproduct_2 =  OrderProduct.objects.filter(user=request.user , product_id=single_product.id)
    orderproduct_count = orderproduct_2.count()
    

    reviews = ReviewRating.objects.filter(product_id=single_product.id , status=True)
    product_gallary = ProductGallary.objects.filter(product_id=single_product.id)
    context = {
        'single_product':single_product,
        'in_cart':in_cart,
        'orderproduct':orderproduct,
        'reviews':reviews,
        'product_gallary':product_gallary,
        'orderproduct_count':orderproduct_count,
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

def submit_review(request,product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method =="POST":
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id , product__id=product_id)
            form = ReviewForm(request.POST , instance=reviews)
            form.save()
            messages.success(request,'Thank You , Your Review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request,'Thank You , Your Review has been submitted.')
                return redirect(url)

