from django.db import models

# Create your models here.
class HomeImage(models.Model):
    name = models.CharField( max_length=50 ,default="image")
    home_image=models.ImageField(upload_to='home images/')

    def __str__(self):
        return self.name
    
class Settings(models.Model):
    site_name = models.CharField( max_length=50)
    logo = models.ImageField( upload_to='setting/')
    phone = models.CharField( max_length=30)
    email = models.EmailField( max_length=254)
    description = models.TextField(max_length=1000)
    fb_link = models.URLField( max_length=200)
    twitter_link = models.URLField( max_length=200)
    instagram_link = models.URLField( max_length=200)
    address = models.CharField( max_length=50)

    def __str__(self):
        return self.site_name