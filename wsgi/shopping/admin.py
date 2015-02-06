from django.contrib import admin
from .models import HomePage, ProductsPage, Product, ProductImage
from mezzanine.pages.admin import PageAdmin
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'price', 'promotion_price')

class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('image', 'description', 'product')

admin.site.register(HomePage, PageAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(ProductsPage, PageAdmin)
