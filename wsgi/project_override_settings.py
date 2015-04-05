#############################
# PROJECT OVERRIDE SETTINGS #
#############################

#
# settings.py are the generic Mezzanine projects settings.
# local_settings.py are the environment settings crafted to fit both Openshift 
# environment and local development.
# You should not need to change anything in those two. 
# Best practice is to inspire form the main settings.py file and use the 
# project_override_settings.py for project related adjustements.
# This practice assures you can safely and carbon upgrade settings related to 
# the next upgrade of Mezzanine.
# 

# Search box adjustement
# http://mezzanine.jupo.org/docs/search-engine.html
SEARCH_MODEL_CHOICES = None

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
#TIME_ZONE = None

TIME_ZONE = 'Asia/Ho_Chi_Minh'

SHOP_USE_VARIATIONS = True
SHOP_OPTION_ADMIN_ORDER = (2, 1)
SHOP_OPTION_TYPE_CHOICES = (
    (1, "Size"),
    (2, "Colour"),
)

SHOP_USE_RELATED_PRODUCTS = True
SHOP_USE_UPSELL_PRODUCTS = True

PYBB_TEMPLATE = "site_base.html"

PYBB_PROFILE_RELATED_NAME = "pybb_customprofile"
AUTH_USER_MODEL = "profiles.CustomUser"

DEBUG = True

EXTRA_MODEL_FIELDS = (
    (
        "cartridge.shop.models.Product.user",
        "ForeignKey",
        (AUTH_USER_MODEL,),
        {"blank": True, "null": True},
    ),
)

