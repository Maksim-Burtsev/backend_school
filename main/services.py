import re
from typing import NamedTuple
from uuid import UUID

from main.models import Item


class PriceCountTuple(NamedTuple):
    price: int
    count: int


class ItemsParentsTuple(NamedTuple):
    items_id: list[UUID]
    parentd_id: list[UUID]


def _save_item(item: dict, db_items: dict, date: str, items_dict: dict) -> None:
    """
    Создаёт/обновляет объект в базе данных 

    Если при создании объекта его родителя не существует, то сперва создаётся родитель
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


def _is_date_in_iso8601(date: str) -> bool:
    """
    Проверяет время на соответствие формату ISO-8601
    """
    regex = r'^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?(Z|[+-](?:2[0-3]|[01][0-9]):[0-5][0-9])?$'

    match_iso8601 = re.compile(regex).match

    try:
        if match_iso8601(date) is not None:
            return True
    except:
        pass
    return False


# TODO rename
def _get_price_of_category(category_obj: Item) -> PriceCountTuple:
    """
    Вычисляет price категории. Рекурсивно обходит все подкатегории.
    """
    res, item_count = 0, 0
    for item in category_obj.offers.all():
        if item._type == "category":
            sub_res, sub_count = _get_price_of_category(item)
            res += sub_res
            item_count += sub_count
        else:
            if item.price:
                res += item.price
                item_count += 1
    return PriceCountTuple(price=res, count=item_count)


def _update_parents_date(parent_id: UUID, date: str) -> None:
    """
    Обновляет дату у всех родителей
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
