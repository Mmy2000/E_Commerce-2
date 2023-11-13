from django.contrib import admin
from .models import Product , Variation , ReviewRating , ProductGallary
import admin_thumbnails
# Register your models here.
@admin_thumbnails.thumbnail('image')
class ProductGallaryInline(admin.TabularInline):
    model = ProductGallary
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name' , 'price' , 'stock' , 'category' , 'modified_date' , 'is_available')
    prepopulated_fields = {'slug' : ('name',)}
    inlines = [ProductGallaryInline]


class VariationAdmin(admin.ModelAdmin):
    list_display = ('product' , 'variation_category' , 'variation_value' , 'created_at' , 'is_active' )
    list_editable = ('is_active',)
    list_filter = ('product' , 'variation_category' , 'variation_value')

admin.site.register(Variation,VariationAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(ReviewRating)
admin.site.register(ProductGallary)


