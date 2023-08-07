from django.contrib import admin

# Register your models here.
from api.models import *

admin.site.register(User)
admin.site.register(Product)
admin.site.register(Deal)
admin.site.register(Payment)
admin.site.register(Branch)
admin.site.register(District)
admin.site.register(Region)
admin.site.register(City)
admin.site.register(OrderDetails)
admin.site.register(PaymentType)
admin.site.register(Currency)