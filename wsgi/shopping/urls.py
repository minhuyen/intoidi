from __future__ import unicode_literals

from django.conf.urls import patterns, url
from . import views

from mezzanine.conf import settings

_slash = "/" if settings.APPEND_SLASH else ""

urlpatterns = patterns("shopping.views",
                       url("^product/(?P<slug>.*)%s$" % _slash, views.product, name="shop_product"),
                       url(r'^(?P<product_id>\d{1,2})/$', views.productDetail, name="detail"),
                       url(r'^like_product/$', views.like_product, name='like_product'),

                       )
