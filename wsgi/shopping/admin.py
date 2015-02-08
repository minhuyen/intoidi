from django.contrib import admin
from .models import HomePage, ProductsPage, Product, ProductImage, Category, ProductOption
from mezzanine.pages.admin import PageAdmin
from mezzanine.core.admin import DisplayableAdmin, TabularDynamicInlineAdmin
from django.db.models import ImageField
from .forms import ImageWidget
# Register your models here.


class ProductImageAdmin(TabularDynamicInlineAdmin):
    model = ProductImage
    formfield_overrides = {ImageField: {"widget": ImageWidget}}




class CategoryInline(TabularDynamicInlineAdmin):
    model = Category.products.through


class CategoryAdmin(admin.ModelAdmin):
    pass

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'unit_price', 'sale_price',)
    inlines = (ProductImageAdmin, CategoryInline, )


class ProductOptionAdmin(admin.ModelAdmin):
    list_display = ('type', 'name')

admin.site.register(HomePage, PageAdmin)
admin.site.register(Product, ProductAdmin)
#admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(ProductsPage, PageAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductOption, ProductOptionAdmin)
