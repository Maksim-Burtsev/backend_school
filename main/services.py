from typing import NamedTuple
from uuid import UUID

from main.models import Item


class PriceCountTuple(NamedTuple):
    price: int
    count: int


class ItemsParentsTuple(NamedTuple):
    items_id: list[UUID]
    parentd_id: list[UUID]


def get_date_in_iso(obj: Item) -> str:
    """Возвращает дату объекта в ISO-8601"""
    return obj.last_update.isoformat()[:-6] + '.000Z'


def get_children(obj: Item) -> list[Item] | list | None:
    """Возващает список всех подкатегорий или пустое значение"""
    children = obj.offers.all()
    if children:
        return children
    if obj._type == 'category':
        return []
    return None


def get_price(obj: Item) -> None | int:
    """Возвращает price объекта или категории"""
    if obj._type == 'offer':
        return obj.price
    res, offers = _get_price_and_count_of_category(obj)
    if res == 0:
        return None
    return int(res/offers)


def _save_item(item: dict, db_items: dict, date: str, items_dict: dict) -> None:
    """
    Создаёт/обновляет объект в базе данных 

    Если при создании объекта его родителя не существует, то он создаётся
    """

    item_obj, _ = db_items.get_or_create(uuid=item['id'])
    item_obj._type = item['type'].lower()
    item_obj.name = item['name']
    item_obj.price = item['price']
    item_obj.last_update = date

    if item['parentId']:
        if db_items.filter(uuid=item['parentId']).exists():
            parent_obj = db_items.get(uuid=item['parentId'])
            parent_obj.last_update = date
            parent_obj.save()
            item_obj.parent = parent_obj
        else:
            parent_data = items_dict[item['parentId']]
            parent_obj, _ = Item.objects.get_or_create(
                _type='category',
                name=parent_data['name'],
                uuid=parent_data['id'],
                last_update=date,
            )
            item_obj.parent = parent_obj

    item_obj.save()


def _get_price_and_count_of_category(category_obj: Item) -> PriceCountTuple:
    """
    Вычисляет price категории. Рекурсивно обходит все подкатегории.
    """
    res, item_count = 0, 0
    for item in category_obj.offers.all():
        if item._type == "category":
            sub_res, sub_count = _get_price_and_count_of_category(item)
            res += sub_res
            item_count += sub_count
        else:
            if item.price:
                res += item.price
                item_count += 1
    return PriceCountTuple(price=res, count=item_count)


def _update_parents_date(parent_id: UUID, date: str) -> None:
    """
    Обновляет дату последнего обновления у всех родителей
    """

    item_obj = Item.objects.get(uuid=parent_id)
    item_obj.last_update = date
    item_obj.save()
    if item_obj.parent:
        _update_parents_date(item_obj.parent.uuid, date)


def _get_items_and_parents_id(items: dict) -> ItemsParentsTuple:
    """
    Формирует на основе входных данных два списка: id всех элементов и id родителей
    """
    items_id = [item['id'] for item in items]
    parents_id = list(set([item['parentId']
                      for item in items if item['parentId']]))

    items_id.extend(parents_id)
    items_id = list(set(items_id))

    return ItemsParentsTuple(items_id=items_id, parentd_id=parents_id)
