from django.contrib import admin
from pybb.admin import ForumAdmin
from pybb.models import Forum
from .models import HomePage, ProductsPage, Product, ProductImage, Category, ProductOption, Sale, ProductVariation, DiscountCode
from mezzanine.pages.admin import PageAdmin
from mezzanine.core.admin import DisplayableAdmin, TabularDynamicInlineAdmin
from django.db.models import ImageField
from .fields import MoneyField
from .forms import (ImageWidget, MoneyWidget, DiscountAdminForm,
                    ProductVariationAdminForm, ProductVariationAdminFormset, ProductAdminForm)
from django.utils.translation import ugettext_lazy as _
from shopping.models import ExtendForum
from wsgi import settings
from copy import deepcopy

# Lists of field names.
option_fields = [f.name for f in ProductVariation.option_fields()]


class ProductImageAdmin(TabularDynamicInlineAdmin):
    model = ProductImage
    formfield_overrides = {ImageField: {"widget": ImageWidget}}


class CategoryInline(TabularDynamicInlineAdmin):
    model = Category.products.through


class CategoryAdmin(admin.ModelAdmin):
    pass

################
#  VARIATIONS  #
################

# If variations aren't used, the variation inline should always
# provide a single inline for managing the single variation per
# product.

variation_fields = ["sku", "num_in_stock", "unit_price",
                    "sale_price", "sale_from", "sale_to", "image"]

if settings.SHOP_USE_VARIATIONS:
    variation_fields.insert(1, "default")
    variations_max_num = None
    variations_extra = 0
else:
    variations_max_num = 1
    variations_extra = 1


class ProductVariationAdmin(admin.TabularInline):
    verbose_name_plural = _("Current variations")
    model = ProductVariation
    fields = variation_fields
    max_num = variations_max_num
    extra = variations_extra
    formfield_overrides = {MoneyField: {"widget": MoneyWidget}}
    form = ProductVariationAdminForm
    formset = ProductVariationAdminFormset
    ordering = ["option%s" % i for i in settings.SHOP_OPTION_ADMIN_ORDER]

product_fieldsets = deepcopy(DisplayableAdmin.fieldsets)
product_fieldsets[0][1]["fields"].insert(1, "user")
product_fieldsets[0][1]["fields"].insert(2, "manufacturer")
product_fieldsets[0][1]["fields"].insert(2, "available")
product_fieldsets[0][1]["fields"].extend(["content", "categories"])
product_fieldsets = list(product_fieldsets)

other_product_fields = []
if settings.SHOP_USE_RELATED_PRODUCTS:
    other_product_fields.append("related_products")
if settings.SHOP_USE_UPSELL_PRODUCTS:
    other_product_fields.append("upsell_products")
if len(other_product_fields) > 0:
    product_fieldsets.append((_("Other products"), {
        "classes": ("collapse-closed",),
        "fields": tuple(other_product_fields)}))

##############
#  PRODUCTS  #
##############

product_list_display = ["admin_thumb", "title", "status", "available",
                        "admin_link"]
product_list_editable = ["status", "available"]

# If variations are used, set up the product option fields for managing
# variations. If not, expose the denormalised price fields for a product
# in the change list view.
if settings.SHOP_USE_VARIATIONS:
    product_fieldsets.insert(1, (_("Create new variations"),
                                 {"classes": ("create-variations",), "fields": option_fields}))
else:
    extra_list_fields = ["sku", "unit_price", "sale_price", "num_in_stock"]
    product_list_display[4:4] = extra_list_fields
    product_list_editable.extend(extra_list_fields)


class ProductAdmin(DisplayableAdmin):

    class Media:
        js = ("js/admin/product_variations.js",)
        css = {"all": ("css/admin/product.css",)}

    list_display = product_list_display
    list_display_links = ("admin_thumb", "title")
    list_editable = product_list_editable
    list_filter = ("status", "available", "categories")
    filter_horizontal = ("categories",) + tuple(other_product_fields)
    search_fields = ("title", "content", "categories__title",
                     "variations__sku")
    inlines = (ProductImageAdmin, ProductVariationAdmin)
    form = ProductAdminForm
    fieldsets = product_fieldsets

    def save_model(self, request, obj, form, change):
        """
        Store the product object for creating variations in save_formset.
        """
        super(ProductAdmin, self).save_model(request, obj, form, change)
        self._product = obj

    def save_formset(self, request, form, formset, change):
        """
        Here be dragons. We want to perform these steps sequentially:
        - Save variations formset
        - Run the required variation manager methods:
          (create_from_options, manage_empty, etc)
        - Save the images formset
        The variations formset needs to be saved first for the manager
        methods to have access to the correct variations. The images
        formset needs to be run last, because if images are deleted
        that are selected for variations, the variations formset will
        raise errors when saving due to invalid image selections. This
        gets addressed in the set_default_images method.
        An additional problem is the actual ordering of the inlines,
        which are in the reverse order for achieving the above. To
        address this, we store the images formset as an attribute, and
        then call save on it after the other required steps have
        occurred.
        """

        # Store the images formset for later saving, otherwise save the
        # formset.
        if formset.model == ProductImage:
            self._images_formset = formset
        else:
            super(ProductAdmin, self).save_formset(request, form, formset,
                                                   change)

        # Run each of the variation manager methods if we're saving
        # the variations formset.
        if formset.model == ProductVariation:

            # Build up selected options for new variations.
            options = dict([(f, request.POST.getlist(f)) for f in option_fields
                            if request.POST.getlist(f)])
            # Create a list of image IDs that have been marked to delete.
            deleted_images = [request.POST.get(f.replace("-DELETE", "-id"))
                              for f in request.POST if f.startswith("images-")
                and f.endswith("-DELETE")]

            # Create new variations for selected options.
            self._product.variations.create_from_options(options)
            # Create a default variation if there are none.
            self._product.variations.manage_empty()

            # Remove any images deleted just now from variations they're
            # assigned to, and set an image for any variations without one.
            self._product.variations.set_default_images(deleted_images)

            # Save the images formset stored previously.
            super(ProductAdmin, self).save_formset(request, form,
                                                   self._images_formset, change)

            # Run again to allow for no images existing previously, with
            # new images added which can be used as defaults for variations.
            self._product.variations.set_default_images(deleted_images)

            # Copy duplicate fields (``Priced`` fields) from the default
            # variation to the product.
            self._product.copy_default_variation()


class ProductOptionAdmin(admin.ModelAdmin):
    ordering = ("type", "name")
    list_display = ("type", "name")
    list_display_links = ("type",)
    list_editable = ("name",)
    list_filter = ("type",)
    search_fields = ("type", "name")
    radio_fields = {"type": admin.HORIZONTAL}


class SaleAdmin(admin.ModelAdmin):
    list_display = ("title", "active", "discount_deduct", "discount_percent",
                    "discount_exact", "valid_from", "valid_to")
    list_editable = ("active", "discount_deduct", "discount_percent",
                     "discount_exact", "valid_from", "valid_to")
    filter_horizontal = ("categories", "products")
    formfield_overrides = {MoneyField: {"widget": MoneyWidget}}
    form = DiscountAdminForm
    fieldsets = (
        (None, {"fields": ("title", "active")}),
        (_("Apply to product and/or products in categories"),
         {"fields": ("products", "categories")}),
        (_("Reduce unit price by"),
         {"fields": (("discount_deduct", "discount_percent",
                      "discount_exact"),)}),
        (_("Sale period"), {"fields": (("valid_from", "valid_to"),)}),
    )


class DiscountCodeAdmin(admin.ModelAdmin):
    list_display = ("title", "active", "code", "discount_deduct",
                    "discount_percent", "min_purchase", "free_shipping", "valid_from",
                    "valid_to")
    list_editable = ("active", "code", "discount_deduct", "discount_percent",
                     "min_purchase", "free_shipping", "valid_from", "valid_to")
    filter_horizontal = ("categories", "products")
    formfield_overrides = {MoneyField: {"widget": MoneyWidget}}
    form = DiscountAdminForm
    fieldsets = (
        (None, {"fields": ("title", "active", "code")}),
        (_("Apply to product and/or products in categories"),
         {"fields": ("products", "categories")}),
        (_("Reduce unit price by"),
         {"fields": (("discount_deduct", "discount_percent"),)}),
        (None, {"fields": (("min_purchase", "free_shipping"),)}),
        (_("Valid for"),
         {"fields": (("valid_from", "valid_to", "uses_remaining"),)}),
    )


class ExtendForumInline(admin.TabularInline):
    model = ExtendForum


class MyForumAdmin(ForumAdmin):
    inlines = ForumAdmin.inlines + [ExtendForumInline]


admin.site.register(HomePage, PageAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Sale, SaleAdmin)
admin.site.register(ProductsPage, PageAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductOption, ProductOptionAdmin)
admin.site.register(DiscountCode, DiscountCodeAdmin)

admin.site.unregister(Forum)
admin.site.register(Forum, MyForumAdmin)
