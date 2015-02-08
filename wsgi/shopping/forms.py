__author__ = 'dominhuyen'
from django import forms
from django.utils.safestring import mark_safe
from mezzanine.conf import settings
from mezzanine.core.templatetags.mezzanine_tags import thumbnail

#######################
#    ADMIN WIDGETS    #
#######################

class ImageWidget(forms.FileInput):
    """
    Render a visible thumbnail for image fields.
    """
    def render(self, name, value, attrs):
        rendered = super(ImageWidget, self).render(name, value, attrs)
        if value:
            orig = u"%s%s" % (settings.MEDIA_URL, value)
            thumb = u"%s%s" % (settings.MEDIA_URL, thumbnail(value, 48, 48))
            rendered = (u"<a target='_blank' href='%s'>"
                        u"<img style='margin-right:6px;' src='%s'>"
                        u"</a>%s" % (orig, thumb, rendered))
        return mark_safe(rendered)
