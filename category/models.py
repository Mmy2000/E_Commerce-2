from django.db import models
from django.utils.text import slugify 


# Create your models here.
class Category(models.Model):
    name = models.CharField(unique=True, max_length=50)
    slug = models.SlugField(unique=True, max_length=100)
    description = models.TextField( max_length=2000 , blank=True)
    image = models.ImageField( upload_to='cat_img' , blank=True)


    def __str__(self):
        return self.name