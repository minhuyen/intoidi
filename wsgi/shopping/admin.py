from django.contrib import admin
from .models import HomePage
from mezzanine.pages.admin import PageAdmin
# Register your models here.

admin.site.register(HomePage, PageAdmin)
