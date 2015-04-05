from django.db import models
from datetime import datetime
from django.db.models.query_utils import Q


class NewSaleManager(models.Manager):
    def get_active(self, *args, **kwargs):
        """
        Items fladgged as active and within date range as well checking
        """
        n = datetime.now()
        valid_from = Q(valid_from__isnull=True) | Q(valid_from__lte=n)
        valid_to = Q(valid_to__isnull=True) | Q(valid_to__gte=n)
        valid = self.filter(valid_from, valid_to, active=True)
        return valid