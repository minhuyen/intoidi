from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from mezzanine.core.fields import FileField, RichTextField
from mezzanine.core.models import RichText, Orderable, Slugged
from mezzanine.pages.models import Page
from mezzanine.utils.models import upload_to
from django.utils.timezone import now
from decimal import Decimal


class HomePage(Page, RichText):

    '''
    A page representing the format of the home page
    '''

    class Meta:
        verbose_name = _("Home page")
        verbose_name_plural = _("Home pages")


class Product(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    user = models.ForeignKey(User, null=False, verbose_name=_("Manufacturer"))
    unit_price = models.FloatField(_("Price"))
    product_code = models.CharField(max_length=255, blank=True, null=True)
    review_point = models.IntegerField(default=0)
    available = models.BooleanField(default=False)
    sale_price = models.FloatField(_("Sale price"))
    sale_from = models.DateTimeField(_("Sale start"), blank=True, null=True)
    sale_to = models.DateTimeField(_("Sale end"), blank=True, null=True)
    view = models.IntegerField(default=0)
    like = models.IntegerField(default=0)
    created_date = models.DateTimeField(null=True, auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    sku = models.CharField(unique=True, blank=True, null=True, max_length=20, verbose_name=_("SKU"))
    num_in_stock = models.IntegerField(_("Number in stock"), blank=True, null=True)

    def __unicode__(self):
        return self.name

    def on_sale(self):
        """
        Returns True if the sale price is applicable.
        """
        n = now()
        valid_from = self.sale_from is None or self.sale_from < n
        valid_to = self.sale_to is None or self.sale_to > n
        return self.promotion_price is not None and valid_from and valid_to

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


class ProductsPage(Page):
    class Meta:
        verbose_name = _("Products Page")
        verbose_name_plural = _("Products Page")


class ProductImage(models.Model):
    image = FileField(verbose_name=_("Image Product"), upload_to=upload_to("product.images.file", "production"))
    description = models.CharField(_("Description"), blank=True, max_length=100)
    product = models.ForeignKey("Product", related_name="images")

    def __unicode__(self):
        value = self.description
        if not value:
            value = ""
        return value

SHOP_OPTION_TYPE_CHOICES = (
    (1, "Size"),
    (2, "Colour"),
)


class ProductOption(models.Model):
    """
    A selectable option for a product such as size or colour.
    """
    type = models.IntegerField(_("Type"),choices=SHOP_OPTION_TYPE_CHOICES)
    name = models.CharField(max_length=255, blank=True)

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





