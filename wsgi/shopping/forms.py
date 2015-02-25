__author__ = 'dominhuyen'
from django import forms
from django.utils.safestring import mark_safe
from mezzanine.conf import settings
from mezzanine.core.templatetags.mezzanine_tags import thumbnail
from django.utils.translation import ugettext_lazy as _
from django.forms.models import BaseInlineFormSet, ModelFormMetaclass
from .models import ProductOption, Product
from future.utils import with_metaclass
from .utils import make_choices

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


class MoneyWidget(forms.TextInput):
    """
    Render missing decimal places for money fields.
    """
    def render(self, name, value, attrs):
        try:
            value = float(value)
        except (TypeError, ValueError):
            pass
        else:
            #set_locale()
            frac_digits = 2
            value = ("%%.%sf" % frac_digits) % value
            attrs["style"] = "text-align:right;"
        return super(MoneyWidget, self).render(name, value, attrs)


class DiscountAdminForm(forms.ModelForm):
    """
    Ensure only one discount field is given a value and if not, assign
    the error to the first discount field so that it displays correctly.
    """
    def clean(self):
        fields = [f for f in self.fields if f.startswith("discount_")]
        reductions = [self.cleaned_data.get(f) for f in fields
                      if self.cleaned_data.get(f)]
        if len(reductions) > 1:
            error = _("Please enter a value for only one type of reduction.")
            self._errors[fields[0]] = self.error_class([error])
        return super(DiscountAdminForm, self).clean()


class ProductVariationAdminForm(forms.ModelForm):
    """
    Ensure the list of images for the variation are specific to the
    variation's product.
    """
    def __init__(self, *args, **kwargs):
        super(ProductVariationAdminForm, self).__init__(*args, **kwargs)
        if "instance" in kwargs:
            product = kwargs["instance"].product
            qs = self.fields["image"].queryset.filter(product=product)
            self.fields["image"].queryset = qs


class ProductVariationAdminFormset(BaseInlineFormSet):
    """
    Ensure no more than one variation is checked as default.
    """
    def clean(self):
        super(ProductVariationAdminFormset, self).clean()
        if len([f for f in self.forms if hasattr(f, "cleaned_data") and
                f.cleaned_data.get("default", False)]) > 1:
            error = _("Only one variation can be checked as the default.")
            raise forms.ValidationError(error)

class ProductAdminFormMetaclass(ModelFormMetaclass):
    """
    Metaclass for the Product Admin form that dynamically assigns each
    of the types of product options as sets of checkboxes for selecting
    which options to use when creating new product variations.
    """
    def __new__(cls, name, bases, attrs):
        for option in settings.SHOP_OPTION_TYPE_CHOICES:
            field = forms.MultipleChoiceField(label=option[1],
                                              required=False, widget=forms.CheckboxSelectMultiple)
            attrs["option%s" % option[0]] = field
        args = (cls, name, bases, attrs)
        return super(ProductAdminFormMetaclass, cls).__new__(*args)


class ProductAdminForm(with_metaclass(ProductAdminFormMetaclass,
                                      forms.ModelForm)):
    """
    Admin form for the Product model.
    """

    class Meta:
        model = Product
        exclude = []

    def __init__(self, *args, **kwargs):
        """
        Set the choices for each of the fields for product options.
        Also remove the current instance from choices for related and
        upsell products (if enabled).
        """
        super(ProductAdminForm, self).__init__(*args, **kwargs)
        for field, options in list(ProductOption.objects.as_fields().items()):
            self.fields[field].choices = make_choices(options)
        instance = kwargs.get("instance")
        if instance:
            queryset = Product.objects.exclude(id=instance.id)
            if settings.SHOP_USE_RELATED_PRODUCTS:
                self.fields["related_products"].queryset = queryset
            if settings.SHOP_USE_UPSELL_PRODUCTS:
                self.fields["upsell_products"].queryset = queryset
