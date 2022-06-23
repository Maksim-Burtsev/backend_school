from celery import shared_task

from main.models import Item, ItemHistory
from main.services import get_price


@shared_task
def _save_items_in_history(date: str) -> None:
    """Сохраняет состояние элементов в ItemsHistory"""
    items = Item.objects.filter(last_update=date)

    items_history = []
    for item in items:
        if item._type == 'category':
            item.price = get_price(item)
        items_history.append(ItemHistory(
            item=item,
            _type=item._type,
            uuid=item.uuid,
            name=item.name,
            price=item.price,
            last_update=date
        ))

    ItemHistory.objects.bulk_create(items_history)
