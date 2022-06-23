from main.models import Item, ItemHistory
from main.services import get_price


def _save_items_in_history(items: list[Item], date: str):
    """Сохраняет состояние элементов в ItemsHistory"""
    items_list = []
    for item in items:
        if item._type == 'category':
            item.price = get_price(item)
        items_list.append(ItemHistory(
            item=item,
            _type=item._type,
            uuid=item.uuid,
            name=item.name,
            price=item.price,
            last_update=date
        ))

    ItemHistory.objects.bulk_create(items_list)
