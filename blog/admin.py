from django.contrib import admin
from .models import Kompaniya, Mahsulot, Savdo

@admin.register(Kompaniya)
class KompaniyaAdmin(admin.ModelAdmin):
    list_display = ('nom', 'telefon', 'manzil', 'mahsulotlar_soni')
    search_fields = ('nom',)
    readonly_fields = ('mahsulotlar_soni',)

    def has_delete_permission(self, request, obj=None):
        if obj and obj.mahsulotlar.count() > 0:
            return False
        return super().has_delete_permission(request, obj)

@admin.register(Mahsulot)
class MahsulotAdmin(admin.ModelAdmin):
    list_display = ('nom', 'kompaniya', 'soni', 'narx')
    search_fields = ('nom',)
    list_filter = ('kompaniya',)
    fields = ('nom', 'kompaniya', 'narx', 'soni')

    def get_readonly_fields(self, request, obj=None):
        if obj:  # mavjud obyektni tahrirlayotganda
            return []
        return []

@admin.register(Savdo)
class SavdoAdmin(admin.ModelAdmin):
    list_display = ('mijoz_nomi', 'mahsulot_nomi', 'kompaniya_nomi', 'soni', 'umumiy_narx', 'savdo_sanasi')
    search_fields = ('mijoz_nomi', 'mahsulot__nom')
    list_filter = ('savdo_sanasi', 'mahsulot__kompaniya')
    fields = ('mijoz_nomi', 'mahsulot', 'soni')

    def save_model(self, request, obj, form, change):
        if obj.mahsulot.soni >= obj.soni:
            super().save_model(request, obj, form, change)
        else:
            raise ValueError("Omborda yetarli mahsulot yo'q")
