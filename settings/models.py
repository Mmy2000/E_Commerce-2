from django.db import models

# Create your models here.
class HomeImage(models.Model):
    name = models.CharField( max_length=50 ,default="image")
    home_image=models.ImageField(upload_to='home images/')

    def __str__(self):
        return self.name