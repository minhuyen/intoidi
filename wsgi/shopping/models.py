from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from mezzanine.core.fields import FileField, RichTextField
from mezzanine.core.models import RichText, Orderable, Slugged
from mezzanine.pages.models import Page
from mezzanine.utils.models import upload_to

class HomePage(Page, RichText):
    '''
    A page representing the format of the home page
    '''

    class Meta:
        verbose_name = _("Home page")
        verbose_name_plural = _("Home pages")


class Product(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    user = models.ForeignKey(User, null=False)
    price = models.FloatField()
    promotion_price = models.FloatField()
    view = models.IntegerField()
    like = models.IntegerField()
    created_date = models.DateTimeField(null=True, auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

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





