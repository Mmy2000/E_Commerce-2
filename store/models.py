from django.db import models
from django.urls import reverse

# Create your models here.
class Product(models.Model):
    name = models.CharField( max_length=50 , unique=True)
    slug = models.SlugField(max_length=50 , unique=True)
    description = models.TextField( max_length=2000 , blank=True)
    image = models.ImageField( upload_to='product_img')
    price = models.IntegerField()
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey("category.Category", verbose_name=("category product"), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateField( auto_now=True)

    def get_absolute_url(self):
        return reverse("store:product_detail", args=[self.category.slug ,self.slug])
    

    def __str__(self):
        return self.name

variation_category_choice=(
    ('color','color'),
    ('size','size')
)

class Variation(models.Model):
    product = models.ForeignKey(Product,  on_delete=models.CASCADE)
    variation_category = models.CharField( max_length=50 , choices=variation_category_choice)
    variation_value = models.CharField( max_length=50 )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(  auto_now_add=True)

    def __str__(self):
        return str(self.product)
    