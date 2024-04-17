from django.contrib import admin

# Register your models here.
from api.models import *

admin.site.register(Branch)
admin.site.register(District)
admin.site.register(Region)
admin.site.register(City)
admin.site.register(PaymentType)
admin.site.register(Currency)
admin.site.register(Brand)
admin.site.register(WorkPlace)
admin.site.register(MessageTemplate)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    list_display = (
        "smartup_id",
        "customer",
        "amount",
        "payment_type",
        "date_of_payment",
        "branch",
    )

    list_filter = ("payment_type__currency", "branch__name")

    sortable_by = (
        "smartup_id",
        "customer",
        "amount",
        "payment_type",
        "date_of_payment",
    )

    search_fields = ("customer__phone", "customer__name", "smartup_id")


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):

    list_display = (
        "smartup_id",
        "customer",
        "total",
        "payment_type",
        "date_of_order",
        "date_of_shipment",
    )

    list_filter = ("payment_type__currency",)

    sortable_by = (
        "smartup_id",
        "customer",
        "total",
        "payment_type",
        "date_of_order",
        "date_of_shipment",
    )

    search_fields = ("customer__phone", "customer__name", "smartup_id")


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = ("smartup_id", "name", "phone")

    list_filter = ("district__name",)

    sortable_by = ("name", "smartup_id", "phone")

    search_fields = ("phone", "name", "smartup_id")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = ("name", "code", "brand")

    list_filter = ("brand",)

    sortable_by = ("code", "brand")

    search_fields = ("code", "name")


@admin.register(OrderDetails)
class OrderDetailsAdmin(admin.ModelAdmin):

    list_display = (
        "product",
        "deal",
    )
