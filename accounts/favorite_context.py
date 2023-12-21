from store.models import Product
def counter(request):
    product_counter = 0
    if request.user.is_authenticated:
        if 'admin' in request.path:
            return{}
        else :
            
            try :
                user_favourites = Product.objects.filter(like=request.user)
                product_counter = user_favourites.count()

            except Product.DoesNotExist:
                product_counter=0

    return dict(product_counter=product_counter)