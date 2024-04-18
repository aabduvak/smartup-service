from django.contrib import admin

# Register your models here.
from api.models import *


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )
    list_display = (
        "id",
        "smartup_id",
        "name",
        "created_at",
    )

    list_filter = ("is_active",)

    sortable_by = (
        "smartup_id",
        "name",
        "created_at",
    )

    search_fields = ("id", "name", "smartup_id")


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )
    list_display = (
        "id",
        "smartup_id",
        "name",
        "created_at",
    )

    list_filter = ("is_active",)

    sortable_by = (
        "smartup_id",
        "name",
        "created_at",
    )

    search_fields = ("id", "name", "smartup_id")


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )
    list_display = (
        "id",
        "smartup_id",
        "name",
        "region",
        "created_at",
    )

    list_filter = (
        "region",
        "is_active",
    )

    sortable_by = (
        "smartup_id",
        "name",
        "created_at",
        "region",
    )

    search_fields = ("id", "name", "smartup_id")


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )
    list_display = (
        "id",
        "smartup_id",
        "name",
        "city",
        "created_at",
    )

    list_filter = (
        "city",
        "is_active",
    )

    sortable_by = (
        "smartup_id",
        "name",
        "created_at",
        "city",
    )

    search_fields = ("id", "name", "smartup_id")


@admin.register(PaymentType)
class PaymentTypeAdmin(admin.ModelAdmin):
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )
    list_display = (
        "id",
        "smartup_id",
        "name",
        "currency",
        "created_at",
    )

    list_filter = (
        "currency",
        "is_active",
    )

    sortable_by = (
        "smartup_id",
        "name",
        "currency",
        "created_at",
    )

    search_fields = ("id", "name", "smartup_id")


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )
    list_display = (
        "id",
        "name",
        "created_at",
    )

    list_filter = ("is_active",)

    sortable_by = (
        "name",
        "created_at",
    )

    search_fields = (
        "id",
        "name",
    )


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )
    list_display = (
        "id",
        "smartup_id",
        "name",
        "created_at",
    )

    list_filter = ("is_active",)

    sortable_by = (
        "smartup_id",
        "name",
        "created_at",
    )

    search_fields = ("id", "name", "smartup_id")


@admin.register(WorkPlace)
class WorkplaceAdmin(admin.ModelAdmin):
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )
    list_display = (
        "id",
        "smartup_id",
        "name",
        "code",
        "created_at",
    )

    filter_horizontal = ("customers",)

    list_filter = ("is_active",)

    sortable_by = (
        "smartup_id",
        "name",
        "code",
        "created_at",
    )

    search_fields = ("id", "name", "smartup_id", "code")


@admin.register(MessageTemplate)
class MessageTemplateAdmin(admin.ModelAdmin):
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    list_display = (
        "name",
        "created_at",
    )

    list_filter = ("is_active",)

    sortable_by = (
        "name",
        "created_at",
    )

    search_fields = ("name",)


@admin.register(ServiceConfiguration)
class ServiceConfigurationAdmin(admin.ModelAdmin):
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )
    list_display = (
        "name",
        "description",
        "created_at",
    )

    list_filter = ("is_active",)

    sortable_by = (
        "name",
        "description",
        "created_at",
    )

    search_fields = (
        "name",
        "description",
    )


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
