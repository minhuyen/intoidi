from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from mezzanine.core.fields import FileField, RichTextField
from mezzanine.core.models import RichText, Orderable, Slugged
from mezzanine.pages.models import Page
from mezzanine.utils.models import upload_to
from django.utils.timezone import now
from decimal import Decimal
from . import fields
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


class Product(Priced):
    name = models.CharField(max_length=255, null=False, blank=False)
    user = models.ForeignKey(User, null=False, verbose_name=_("Manufacturer"))
    product_code = models.CharField(max_length=255, blank=True, null=True)
    review_point = models.IntegerField(default=0)
    available = models.BooleanField(default=False)
    view = models.IntegerField(default=0)
    like = models.IntegerField(default=0)
    created_date = models.DateTimeField(null=True, auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name


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
        #order_with_respect_to = "product"

SHOP_OPTION_TYPE_CHOICES = (
    (1, "Size"),
    (2, "Colour"),
)


class ProductOption(models.Model):
    """
    A selectable option for a product such as size or colour.
    """
    type = models.IntegerField(_("Type"),choices=SHOP_OPTION_TYPE_CHOICES)
    name = fields.OptionField(_("Name"))

    def __unicode__(self):
        return self.name


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
    discount_deduct = models.FloatField(_("Reduce by amount"))
    discount_percent = models.FloatField(_("Reduce by percent"),blank=True, null=True)
    discount_exact = models.FloatField(_("Reduce to amount"))
    valid_from = models.DateTimeField(_("Valid from"), blank=True, null=True)
    valid_to = models.DateTimeField(_("Valid to"), blank=True, null=True)

    def __unicode__(self):
        self.title





