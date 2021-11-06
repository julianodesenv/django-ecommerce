from django.contrib import admin
from .models import Product, Variations


class VariationInline(admin.TabularInline):
    model = Variations
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    inlines = [
        VariationInline
    ]
    

admin.site.register(Product, ProductAdmin)
admin.site.register(Variations)