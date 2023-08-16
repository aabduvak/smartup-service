from django.contrib import admin

# Register your models here.
from api.models import *

admin.site.register(User)
admin.site.register(Deal)
admin.site.register(Payment)
admin.site.register(Branch)
admin.site.register(District)
admin.site.register(Region)
admin.site.register(City)
admin.site.register(PaymentType)
admin.site.register(Currency)
admin.site.register(Brand)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    
    list_display = (
        'name',
        'code',
        'brand'
    )
    
    list_filter = ('brand',)
    
    sortable_by = ('code', 'brand')
    
    search_fields = ('code', 'name')

@admin.register(OrderDetails)
class OrderDetailsAdmin(admin.ModelAdmin):

    
    list_display = (
        'product',
        'deal',
    )
    