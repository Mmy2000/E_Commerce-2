from .models import Category
from django.views.generic import ListView 


class CategoryList(ListView):
    model = Category