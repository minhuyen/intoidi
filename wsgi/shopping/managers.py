__author__ = 'dominhuyen'
from django.db.models import Manager, Q
from django.utils.datastructures import SortedDict
from collections import defaultdict
from django.utils.timezone import now


class ProductVariationManager(Manager):

    use_for_related_fields = True

    def _empty_options_lookup(self, exclude=None):
        """
        Create a lookup dict of field__isnull for options fields.
        """
        if not exclude:
            exclude = {}
        return dict([("%s__isnull" % f.name, True)
                     for f in self.model.option_fields() if f.name not in exclude])

    def create_from_options(self, options):
        """
        Create all unique variations from the selected options.
        """
        if options:
            options = SortedDict(options)
            # Build all combinations of options.
            variations = [[]]
            for values_list in list(options.values()):
                variations = [x + [y] for x in variations for y in values_list]
            for variation in variations:
                # Lookup unspecified options as null to ensure a
                # unique filter.
                variation = dict(list(zip(list(options.keys()), variation)))
                lookup = dict(variation)
                lookup.update(self._empty_options_lookup(exclude=variation))
                try:
                    self.get(**lookup)
                except self.model.DoesNotExist:
                    self.create(**variation)

    def manage_empty(self):
        """
        Create an empty variation (no options) if none exist,
        otherwise if multiple variations exist ensure there is no
        redundant empty variation. Also ensure there is at least one
        default variation.
        """
        total_variations = self.count()
        if total_variations == 0:
            self.create()
        elif total_variations > 1:
            self.filter(**self._empty_options_lookup()).delete()
        try:
            self.get(default=True)
        except self.model.DoesNotExist:
            first_variation = self.all()[0]
            first_variation.default = True
            first_variation.save()

    def set_default_images(self, deleted_image_ids):
        """
        Assign the first image for the product to each variation that
        doesn't have an image. Also remove any images that have been
        deleted via the admin to avoid invalid image selections.
        """
        variations = self.all()
        if not variations:
            return
        image = variations[0].product.images.exclude(id__in=deleted_image_ids)
        if image:
            image = image[0]
        for variation in variations:
            save = False
            if str(variation.image_id) in deleted_image_ids:
                variation.image = None
                save = True
            if image and not variation.image:
                variation.image = image
                save = True
            if save:
                variation.save()


class ProductOptionManager(Manager):

    def as_fields(self):
        """
        Return a dict of product options as their field names and
        choices.
        """
        options = defaultdict(list)
        for option in self.all():
            options["option%s" % option.type].append(option.name)
        return options


class DiscountCodeManager(Manager):

    def active(self, *args, **kwargs):
        """
        Items flagged as active and in valid date range if date(s) are
        specified.
        """
        n = now()
        valid_from = Q(valid_from__isnull=True) | Q(valid_from__lte=n)
        valid_to = Q(valid_to__isnull=True) | Q(valid_to__gte=n)
        valid = self.filter(valid_from, valid_to, active=True)
        return valid.exclude(uses_remaining=0)

    def get_valid(self, code, cart):
        """
        Items flagged as active and within date range as well checking
        that the given cart contains items that the code is valid for.
        """
        total_price_valid = (Q(min_purchase__isnull=True) |
                             Q(min_purchase__lte=cart.total_price()))
        discount = self.active().get(total_price_valid, code=code)
        products = discount.all_products()
        if products.count() > 0:
            if products.filter(variations__sku__in=cart.skus()).count() == 0:
                raise self.model.DoesNotExist
        return discount


class SaleManager(Manager):
    def get_active(self, *args, **kwargs):
        """
        Items fladgged as active and within date range as well checking
        """
        n = now()
        valid_from = Q(valid_from__isnull=True) | Q(valid_from__lte=n)
        valid_to = Q(valid_to__isnull=True) | Q(valid_to__gte=n)
        valid = self.filter(valid_from, valid_to, active=True)
        return valid

