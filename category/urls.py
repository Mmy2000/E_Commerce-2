from django.urls import path
from . views import  CategoryList

app_name = 'category'

urlpatterns = [
    path('category', CategoryList.as_view() ,name = 'category_list'),
]