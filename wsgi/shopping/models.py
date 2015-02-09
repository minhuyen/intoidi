from django.contrib.auth.models import User
from django.db import models, connection
from django.utils.translation import ugettext_lazy as _

from mezzanine.core.fields import FileField, RichTextField
from mezzanine.core.models import RichText, Orderable, Slugged
from mezzanine.core.managers import DisplayableManager
from mezzanine.generic.fields import RatingField
from mezzanine.pages.models import Page
from mezzanine.utils.models import upload_to, AdminThumbMixin
from django.utils.timezone import now
from decimal import Decimal
from . import fields
from . import managers
from future.utils import with_metaclass
from django.db.models.base import ModelBase
from operator import iand, ior
from django.db.models import Q
from wsgi import settings
from mezzanine.core.models import Displayable, RichText, Orderable, SiteRelated


class Priced(models.Model):
    """
    Abstract model with unit and sale price fields. Inherited by
    ``Product`` and ``ProductVariation`` models.
    """

    unit_price = fields.MoneyField(_("Unit price"))
    sale_id = models.IntegerField(null=True)
    sale_price = fields.MoneyField(_("Sale price"))
    sale_from = models.DateTimeField(_("Sale start"), blank=True, null=True)
    sale_to = models.DateTimeField(_("Sale end"), blank=True, null=True)
    sku = fields.SKUField(unique=True, blank=True, null=True)
    num_in_stock = models.IntegerField(_("Number in stock"), blank=True, null=True)

    class Meta:
        abstract = True

    def on_sale(self):
        """
        Returns True if the sale price is applicable.
        """
        n = now()
        valid_from = self.sale_from is None or self.sale_from < n
        valid_to = self.sale_to is None or self.sale_to > n
        return self.sale_price is not None and valid_from and valid_to

    def has_price(self):
        """
        Returns True if there is a valid price.
        """
        return self.on_sale() or self.unit_price is not None

    def price(self):
        """
        Returns the actual price - sale price if applicable otherwise
        the unit price.
        """
        if self.on_sale():
            return self.sale_price
        elif self.has_price():
            return self.unit_price
        return Decimal("0")

    def copy_price_fields_to(self, obj_to):
        """
        Copies each of the fields for the ``Priced`` model from one
        instance to another. Used for synchronising the denormalised
        fields on ``Product`` instances with their default variation.
        """
        for field in Priced._meta.fields:
            if not isinstance(field, models.AutoField):
                setattr(obj_to, field.name, getattr(self, field.name))
        obj_to.save()


class HomePage(Page, RichText):

    '''
    A page representing the format of the home page
    '''

    class Meta:
        verbose_name = _("Home page")
        verbose_name_plural = _("Home pages")


class Product(Displayable, Priced, RichText, AdminThumbMixin):
    """
    Container model for a product that stores information common to
    all of its variations such as the product's title and description.
    """

    name = models.CharField(max_length=255, null=False, blank=False)
    user = models.ForeignKey(User, null=False, verbose_name=_("Member"))
    manufacturer = models.CharField(max_length=255, verbose_name=_("Manufacturer"), blank=True, null=True)
    review_point = models.IntegerField(default=0, verbose_name=_("Review point"))
    available = models.BooleanField(_("Available for purchase"), default=False)
    view = models.IntegerField(default=0)
    like = models.IntegerField(default=0)
    created_date = models.DateTimeField(null=True, auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    image = models.CharField(_("Image"), max_length=100, blank=True, null=True)
    categories = models.ManyToManyField("Category", blank=True,
                                        verbose_name=_("Product categories"))

    related_products = models.ManyToManyField("self",
                                              verbose_name=_("Related products"), blank=True)
    upsell_products = models.ManyToManyField("self",
                                             verbose_name=_("Upsell products"), blank=True)

    rating = RatingField(verbose_name=_("Rating"))

    objects = DisplayableManager()

    admin_thumb_field = "image"

    search_fields = {"variations__sku": 100}

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Copies the price fields to the default variation when
        ``SHOP_USE_VARIATIONS`` is False, and the product is
        updated via the admin change list.
        """
        updating = self.id is not None
        super(Product, self).save(*args, **kwargs)
        if updating and not settings.SHOP_USE_VARIATIONS:
            default = self.variations.get(default=True)
            self.copy_price_fields_to(default)

    @models.permalink
    def get_absolute_url(self):
        return ("shopping:shop_product", (), {"slug": self.slug})

    def copy_default_variation(self):
        """
        Copies the price and image fields from the default variation
        when the product is updated via the change view.
        """
        default = self.variations.get(default=True)
        default.copy_price_fields_to(self)
        if default.image:
            self.image = default.image.image.name
        self.save()


class ProductsPage(Page):
    class Meta:
        verbose_name = _("Products Page")
        verbose_name_plural = _("Products Page")


class ProductImage(Orderable):
    image = FileField(verbose_name=_("Image Product"), upload_to=upload_to("product.images.file", "production"))
    description = models.CharField(_("Description"), blank=True, max_length=100)
    product = models.ForeignKey("Product", related_name="images")

    def __unicode__(self):
        value = self.description
        if not value:
            value = ""
        return value

    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Images")
        order_with_respect_to = "product"


class ProductOption(models.Model):
    """
    A selectable option for a product such as size or colour.
    """
    type = models.IntegerField(_("Type"),choices=settings.SHOP_OPTION_TYPE_CHOICES)
    name = fields.OptionField(_("Name"))

    objects = managers.ProductOptionManager()

    def __unicode__(self):
        return self.name


class ProductVariationMetaclass(ModelBase):
    """
    Metaclass for the ``ProductVariation`` model that dynamcally
    assigns an ``fields.OptionField`` for each option in the
    ``SHOP_PRODUCT_OPTIONS`` setting.
    """
    def __new__(cls, name, bases, attrs):
        # Only assign new attrs if not a proxy model.
        if not ("Meta" in attrs and getattr(attrs["Meta"], "proxy", False)):
            for option in settings.SHOP_OPTION_TYPE_CHOICES:
                attrs["option%s" % option[0]] = fields.OptionField(option[1])
        args = (cls, name, bases, attrs)
        return super(ProductVariationMetaclass, cls).__new__(*args)


class ProductVariation(with_metaclass(ProductVariationMetaclass, Priced)):
    """
    A combination of selected options from
    ``SHOP_OPTION_TYPE_CHOICES`` for a ``Product`` instance.
    """

    product = models.ForeignKey("Product", related_name="variations")
    default = models.BooleanField(_("Default"), default=False)
    image = models.ForeignKey("ProductImage", verbose_name=_("Image"),
                              null=True, blank=True, on_delete=models.SET_NULL)

    objects = managers.ProductVariationManager()

    class Meta:
        ordering = ("-default",)

    def __unicode__(self):
        """
        Display the option names and values for the variation.
        """
        options = []
        for field in self.option_fields():
            name = getattr(self, field.name)
            if name is not None:
                option = u"%s: %s" % (field.verbose_name, name)
                options.append(option)
        result = u"%s %s" % (str(self.product), u", ".join(options))
        return result.strip()

    def save(self, *args, **kwargs):
        """
        Use the variation's ID as the SKU when the variation is first
        created.
        """
        super(ProductVariation, self).save(*args, **kwargs)
        if not self.sku:
            self.sku = self.id
            self.save()

    def get_absolute_url(self):
        return self.product.get_absolute_url()

    @classmethod
    def option_fields(cls):
        """
        Returns each of the model fields that are dynamically created
        from ``SHOP_OPTION_TYPE_CHOICES`` in
        ``ProductVariationMetaclass``.
        """
        all_fields = cls._meta.fields
        return [f for f in all_fields if isinstance(f, fields.OptionField)]

    def options(self):
        """
        Returns the field values of each of the model fields that are
        dynamically created from ``SHOP_OPTION_TYPE_CHOICES`` in
        ``ProductVariationMetaclass``.
        """
        return [getattr(self, field.name) for field in self.option_fields()]

    # def live_num_in_stock(self):
    #     """
    #     Returns the live number in stock, which is
    #     ``self.num_in_stock - num in carts``. Also caches the value
    #     for subsequent lookups.
    #     """
    #     if self.num_in_stock is None:
    #         return None
    #     if not hasattr(self, "_cached_num_in_stock"):
    #         num_in_stock = self.num_in_stock
    #         carts = Cart.objects.current()
    #         items = CartItem.objects.filter(sku=self.sku, cart__in=carts)
    #         aggregate = items.aggregate(quantity_sum=models.Sum("quantity"))
    #         num_in_carts = aggregate["quantity_sum"]
    #         if num_in_carts is not None:
    #             num_in_stock = num_in_stock - num_in_carts
    #         self._cached_num_in_stock = num_in_stock
    #     return self._cached_num_in_stock

    def has_stock(self, quantity=1):
        """
        Returns ``True`` if the given quantity is in stock, by checking
        against ``live_num_in_stock``. ``True`` is returned when
        ``num_in_stock`` is ``None`` which is how stock control is
        disabled.
        """
        live = self.live_num_in_stock()
        return live is None or quantity == 0 or live >= quantity

    def update_stock(self, quantity):
        """
        Update the stock amount - called when an order is complete.
        Also update the denormalised stock amount of the product if
        this is the default variation.
        """
        if self.num_in_stock is not None:
            self.num_in_stock += quantity
            self.save()
            if self.default:
                self.product.num_in_stock = self.num_in_stock
                self.product.save()


class Category(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    products = models.ManyToManyField("Product", blank=True, verbose_name=_("Products"))
    options = models.ManyToManyField("ProductOption", blank=True, verbose_name=_("Product options"),
                                     related_name="product_options")
    def __unicode__(self):
        return self.name


class Discount(models.Model):
    title = models.CharField(_("Title"), max_length=100)
    active = models.BooleanField(_("Active"), default=False)
    products = models.ManyToManyField("Product", blank=True,
                                      verbose_name=_("Products"))
    categories = models.ManyToManyField("Category", blank=True,
                                        related_name="%(class)s_related",
                                        verbose_name=_("Categories"))
    discount_deduct = fields.MoneyField(_("Reduce by amount"))
    discount_percent = fields.PercentageField(_("Reduce by percent"),
                                              max_digits=5, decimal_places=2,
                                              blank=True, null=True)
    discount_exact = fields.MoneyField(_("Reduce to amount"))
    valid_from = models.DateTimeField(_("Valid from"), blank=True, null=True)
    valid_to = models.DateTimeField(_("Valid to"), blank=True, null=True)

    def __unicode__(self):
        self.title

    class Meta:
        abstract = True

    def all_products(self):
        """
        Return the selected products as well as the products in the
        selected categories.
        """
        filters = [category.filters() for category in self.categories.all()]
        filters = reduce(ior, filters + [Q(id__in=self.products.only("id"))])
        return Product.objects.filter(filters).distinct()


class Sale(Discount):
    """
    Stores sales field values for price and date range which when saved
    are then applied across products and variations according to the
    selected categories and products for the sale.
    """

    class Meta:
        verbose_name = _("Sale")
        verbose_name_plural = _("Sales")

    def save(self, *args, **kwargs):
        super(Sale, self).save(*args, **kwargs)
        self.update_products()

    def update_products(self):
        """
        Apply sales field value to products and variations according
        to the selected categories and products for the sale.
        """
        self._clear()
        if self.active:
            extra_filter = {}
            if self.discount_deduct is not None:
                # Don't apply to prices that would be negative
                # after deduction.
                extra_filter["unit_price__gt"] = self.discount_deduct
                sale_price = models.F("unit_price") - self.discount_deduct
            elif self.discount_percent is not None:
                sale_price = models.F("unit_price") - (
                    models.F("unit_price") / "100.0" * self.discount_percent)
            elif self.discount_exact is not None:
                # Don't apply to prices that are cheaper than the sale
                # amount.
                extra_filter["unit_price__gt"] = self.discount_exact
                sale_price = self.discount_exact
            else:
                return
            products = self.all_products()
            variations = ProductVariation.objects.filter(product__in=products)
            for priced_objects in (products, variations):
                update = {"sale_id": self.id,
                          "sale_price": sale_price,
                          "sale_to": self.valid_to,
                          "sale_from": self.valid_from}
                using = priced_objects.db
                if "mysql" not in settings.DATABASES[using]["ENGINE"]:
                    priced_objects.filter(**extra_filter).update(**update)
                else:
                    # Work around for MySQL which does not allow update
                    # to operate on subquery where the FROM clause would
                    # have it operate on the same table, so we update
                    # each instance individually: http://bit.ly/1xMOGpU
                    #
                    # Also MySQL may raise a 'Data truncated' warning here
                    # when doing a calculation that exceeds the precision
                    # of the price column. In this case it's safe to ignore
                    # it and the calculation will still be applied, but
                    # we need to massage transaction management in order
                    # to continue successfully: http://bit.ly/1xMOJCd
                    for priced in priced_objects.filter(**extra_filter):
                        for field, value in list(update.items()):
                            setattr(priced, field, value)
                        try:
                            priced.save()
                        except Warning:
                            connection.set_rollback(False)

    def delete(self, *args, **kwargs):
        """
        Clear this sale from products when deleting the sale.
        """
        self._clear()
        super(Sale, self).delete(*args, **kwargs)

    def _clear(self):
        """
        Clears previously applied sale field values from products prior
        to updating the sale, when deactivating it or deleting it.
        """
        update = {"sale_id": None, "sale_price": None,
                  "sale_from": None, "sale_to": None}
        for priced_model in (Product, ProductVariation):
            priced_model.objects.filter(sale_id=self.id).update(**update)







