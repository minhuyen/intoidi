from cartridge.shop.admin import ProductAdmin
from cartridge.shop.models import Product
from copy import deepcopy
from django.contrib import admin
from pybb.admin import ForumAdmin
from pybb.models import Forum
from mezzanine.pages.admin import PageAdmin
from profiles.models import CustomUser
from shopping.models import ExtendForum, HomePage


class ExtendForumInline(admin.TabularInline):
    model = ExtendForum


class MyForumAdmin(ForumAdmin):
    inlines = ForumAdmin.inlines + [ExtendForumInline]


product_fieldsets = deepcopy(ProductAdmin.fieldsets)
product_fieldsets[0][1]["fields"].insert(2, "user")
product_fieldsets[0][1]["fields"].insert(3, "manufacturer")
product_fieldsets[0][1]["fields"].insert(4, "review_point")


class MyProductAdmin(ProductAdmin):
    fieldsets = product_fieldsets

admin.site.unregister(Product)
admin.site.register(Product, MyProductAdmin)

admin.site.unregister(Forum)
admin.site.register(Forum, MyForumAdmin)
# admin.site.register(CustomUser)
admin.site.register(HomePage, PageAdmin)
