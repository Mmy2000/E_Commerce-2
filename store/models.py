from django.db.models import Avg
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

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
    
    def avr_review(self):
        reviews = ReviewRating.objects.filter(product=self , status=True).aggregate(average=Avg('rating'))
        avg =0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def __str__(self):
        return self.name

class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager,self).filter(variation_category='color',is_active=True)
    
    def sizes(self):
        return super(VariationManager,self).filter(variation_category='size',is_active=True)

variation_category_choice=(
    ('color','color'),
    ('size','size'),
)

class Variation(models.Model):
    product = models.ForeignKey(Product,  on_delete=models.CASCADE)
    variation_category = models.CharField( max_length=200 , choices=variation_category_choice)
    variation_value = models.CharField( max_length=200 )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(  auto_now_add=True)
    objects = VariationManager()

    def __str__(self):
        return self.variation_value
    
class ReviewRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    subject = models.CharField(max_length=500 , blank=True)
    review = models.TextField(max_length=500 , blank=True)
    rating = models.FloatField()
    ip = models.CharField( max_length=50 , blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField( auto_now_add=True)
    updated_at = models.DateTimeField( auto_now=True)

    def __str__(self):
        return self.subject
    