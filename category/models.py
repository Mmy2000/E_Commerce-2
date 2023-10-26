from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(unique=True, max_length=50)
    slug = models.SlugField(unique=True, max_length=100)
    description = models.TextField( max_length=2000 , blank=True)
    image = models.ImageField( upload_to='cat_img' , blank=True)

    def get_url(self):
        return reverse('store:product_by_category',args=[self.slug])

    def __str__(self):
        return str(self.name)