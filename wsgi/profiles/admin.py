from django.contrib import admin

# Register your models here.
from profiles.models import CustomProfile

admin.site.register(CustomProfile)
