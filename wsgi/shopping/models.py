from cartridge.shop.models import Sale, Product
from django.db import models
from django.utils.translation import ugettext_lazy as _

from mezzanine.core.fields import FileField
from mezzanine.core.models import RichText
from mezzanine.pages.models import Page
from mezzanine.utils.models import upload_to
from pybb.models import Forum
from shopping.managers import NewSaleManager


class HomePage(Page, RichText):

    '''
    A page representing the format of the home page
    '''

    class Meta:
        verbose_name = _("Home page")
        verbose_name_plural = _("Home pages")


class ExtendForum(models.Model):
    forum = models.OneToOneField(Forum)
    image = FileField(verbose_name=_("Image"),
                      upload_to=upload_to("pybb.forum.image", "image"),
                      format="Image", max_length=255, null=True, blank=True)


class MySale(Sale):
    secondary = NewSaleManager()

    class Meta:
        proxy = True


class ProductExtend:
    def show_discount_percent(self):
        result = 100 - int((self.sale_price/self.unit_price)*100)
        return result

Product.__bases__ += (ProductExtend,)








