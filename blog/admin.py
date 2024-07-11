from django.contrib import admin
from .models import Product, Company, Sale


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'quantity', 'price')
    fields = ('title', 'company', 'quantity', 'price')
    readonly_fields = ('company',)

    def has_delete_permission(self, request, obj=None):
        if obj and obj.quantity > 0:
            return False
        return super().has_delete_permission(request, obj=obj)


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('title', 'phone', 'address', 'products_count')

    def has_delete_permission(self, request, obj=None):
        if obj and obj.products.filter(quantity__gt=0).exists():
            return False
        return super().has_delete_permission(request, obj=obj)


class SaleAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'product', 'quantity', 'sale_date', 'total_price')
    readonly_fields = ('customer_name', 'product', 'quantity', 'sale_date', 'total_price')

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Product, ProductAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Sale, SaleAdmin)
