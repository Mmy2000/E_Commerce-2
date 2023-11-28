from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField( max_length=50 , blank=True)
    date_added = models.DateField( auto_now_add=True)


    def __str__(self):
        return self.cart_id
    
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE , null=True)
    product = models.ForeignKey("store.Product", on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE , null=True)
    variations = models.ManyToManyField("store.Variation",blank=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)


    def sub_total(self):
        if self.product.discount:
            return self.product.discount * self.quantity
        else:
            return self.product.price * self.quantity

    def __str__(self):
        return str(self.product)
    