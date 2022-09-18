from datetime import datetime, timedelta


from django.db import models
from django.db.models import Q
from django.apps import apps


class ItemManager(models.Manager):
    def last_day_from(self, date: datetime):
        Item = apps.get_model("main", "Item")
        start_date = date - timedelta(days=1)

        queryset = Item.objects.filter(
            Q(last_update__gte=start_date) & Q(last_update__lte=date)
        ).select_related("parent")

        return queryset


class ItemHistoryManager(models.Manager):
    def item_between_dates(
        self, item_obj, date_start: str | None, date_end: str | None
    ):
        ItemHistory = apps.get_model("main", "ItemHistory")

        queryset = ItemHistory.objects.filter(item=item_obj)
        if date_start:
            queryset = queryset.filter(last_update__gte=date_start)

        if date_end:
            queryset = queryset.filter(last_update__lte=date_end)

        return queryset
