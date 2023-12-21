from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('',views.store ,name='store'),
    path('category/<slug:category_slug>/',views.store ,name='product_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/',views.product_detail ,name='product_detail'),
    path('search/',views.search ,name='search'),
    path('submit_review/<int:product_id>/',views.submit_review ,name='submit_review'),
    path('product_by_price/',views.product_by_price ,name='product_by_price'),
    path('product_by_size/',views.product_by_size ,name='product_by_size'),
    path('<int:id>/like_or_dislike',views.like_or_unlike , name='like'),
]