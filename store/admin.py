from django.contrib import admin
from .models import Product , Variation
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name' , 'price' , 'stock' , 'category' , 'modified_date' , 'is_available')
    prepopulated_fields = {'slug' : ('name',)}



class VariationAdmin(admin.ModelAdmin):
    list_display = ('product' , 'variation_category' , 'variation_value' , 'created_at' , 'is_active' )
    list_editable = ('is_active',)
    list_filter = ('product' , 'variation_category' , 'variation_value')

admin.site.register(Variation,VariationAdmin)
admin.site.register(Product,ProductAdmin)
