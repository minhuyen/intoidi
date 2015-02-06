from django.contrib import admin
from .models import HomePage, ProductsPage, Product, ProductImage, Category, ProductOption
from mezzanine.pages.admin import PageAdmin
# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'price', 'promotion_price')


class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('image', 'description', 'product')


class CategoryAdmin(admin.ModelAdmin):
    pass


class ProductOptionAdmin(admin.ModelAdmin):
    list_display = ('type', 'name')

admin.site.register(HomePage, PageAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(ProductsPage, PageAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductOption, ProductOptionAdmin)
