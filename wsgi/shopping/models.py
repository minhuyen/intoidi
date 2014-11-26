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
