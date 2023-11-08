from django.contrib import admin
from .models import Payment , Order , OrderProduct

# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display = ('full_name','email','order_total','created_at','is_orderd')
    list_editable = ('is_orderd',)

admin.site.register(Payment)
admin.site.register(OrderProduct)
admin.site.register(Order,OrderAdmin)