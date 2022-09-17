from typing import NamedTuple
from uuid import UUID

from django.db.models import QuerySet

from main.models import Item


class ItemsParentsTuple(NamedTuple):
    items_id: list[UUID]
    parentd_id: list[UUID]


def get_parents_id(items: dict) -> list[UUID | None]:
    """Возвращает уникальный список UUID родителей полученных объектов"""
    return list(set([item["parentId"] for item in items if item["parentId"]]))


def save_items(items: dict, date: str) -> None:
    """Сохраняет объекты в базу"""
    items_dict = {i["id"]: i for i in items}

    parents_id = get_parents_id(items)
    items_id = list(set([item["id"] for item in items] + parents_id))

    db_items = Item.objects.filter(uuid__in=items_id)
    for item in items:
        save_item(item, db_items, date, items_dict)


def get_price(item: Item):
    """Возвращает стоимость объекта. Если это категория, то возвращает среднюю стоимость среди всех потомков"""
    if item._type == "offer":
        return item.price
    # TODO calculate_category_price
    total, count = 0, 0
    descendants = item.get_descendants().select_related("parent")
    for descendant in descendants:
        if descendant.price:
            total += descendant.price
            count += 1

    return None if total == 0 else int(total / count)


def set_price_and_childrens(item: Item, descendants: list[Item]):
    """Находит стоимость категории и всех её потомков, а после добавляет их в качестве свойств объекта"""

    set_children_for_descendants(descendants)
    set_price_for_descendants_cats(descendants)
    set_item_price_and_childrens(item, descendants)


def set_item_price_and_childrens(item: Item, descendants: list[Item]):
    """
    Добавляет объекту атрибуты .children и .price

    Значение каждого из них вычисляется в результате обхода списка потомков
    """
    item.children = []
    count, price = 0, 0
    for i in descendants:
        if i.parent == item:
            item.children.append(i)
        if i._type == "offer":
            count += 1
            price += i.price
    item.price = int(price / count) if count > 0 else None


def set_children_for_descendants(descendants: list[Item]):
    """Добавляет атрибут .children к каждому потомку, в котором содержатся дочерние объекты"""
    for descendant in descendants:
        if descendant._type == "offer":
            descendant.children = None
            continue
        descendant.children = [j for j in descendants if j.parent == descendant]


def set_price_for_descendants_cats(descendants: list[Item]) -> None:
    """Вычисляет стоимость для всех категорий среди потомков и добавляет её в качестве атрибута .price"""
    for i in descendants:
        if i._type == "category":
            cat_items = get_cat_items(i)
            price, count = 0, 0
            for j in cat_items:
                price += j.price
                count += 1
            i.price = int(price / count) if count != 0 else None


def get_cat_items(cat_obj: Item) -> list[Item | None]:
    """Возвращает список всех товаров, которые являются потомками данной категории"""

    items_list = []
    for child in cat_obj.children:
        if child._type == "category":
            items_list.extend(get_cat_items(child))
        else:
            items_list.append(child)

    return items_list


def get_date_in_iso(obj: Item) -> str:
    """Возвращает дату объекта в ISO-8601"""
    return obj.last_update.isoformat()[:-6] + ".000Z"


def get_parent_obj(
    db_items: QuerySet, parent_id: UUID, items_dict: dict, date: str
) -> Item:
    """Возвращает объект родителя из QuerySet'a если он он существует, иначе
    создаёт новый

    db_items - QuerySet объектов, которые пришли в запросе и уже существуют в
    базе (т.е. их обновляют)"""
    if db_items.filter(uuid=parent_id).exists():
        parent_obj = db_items.get(uuid=parent_id)
    else:
        parent_data = items_dict[parent_id]
        parent_obj, _ = Item.objects.get_or_create(
            _type="category",
            name=parent_data["name"],
            uuid=parent_data["id"],
            last_update=date,
        )
    return parent_obj


def save_item(item: dict, db_items: dict, date: str, items_dict: dict) -> None:
    """
    Создаёт/обновляет объект в базе данных

    Если при создании объекта его родителя не существует, то он создаётся
    """

    item_obj, _ = db_items.get_or_create(uuid=item["id"])
    item_obj._type = item["type"].lower()
    item_obj.name = item["name"]
    item_obj.price = item["price"]
    item_obj.last_update = date

    if parent_id := item["parentId"]:
        parent_obj = get_parent_obj(db_items, parent_id, items_dict, date)
        item_obj.parent = parent_obj

    item_obj.save()


def update_categories_date(parents_id: list[UUID], date) -> None:
    """Обновляет дату последнего обновления у всех категорий и их родителей (до самого корня дерева)"""
    categories = Item.objects.filter(uuid__in=parents_id)
    categories.update(last_update=date)

    categories_parents = [
        category.parent.uuid for category in categories if category.parent
    ]
    for parent_id in categories_parents:
        update_parent_date(parent_id, date)


def update_parent_date(parent_id: UUID, date: str) -> None:
    """
    Рекурсивно обходит всех родителей категории до корня и обновляет у них дату
    """

    item_obj = Item.objects.get(uuid=parent_id)
    item_obj.last_update = date
    item_obj.save()
    if item_obj.parent:
        update_parent_date(item_obj.parent.uuid, date)


def get_items_and_parents_id(items: dict) -> ItemsParentsTuple:
    """
    Формирует на основе входных данных два списка: id всех элементов и id родителей
    """
    items_id = [item["id"] for item in items]
    parents_id = list(set([item["parentId"] for item in items if item["parentId"]]))

    items_id.extend(parents_id)
    items_id = list(set(items_id))

    return ItemsParentsTuple(items_id=items_id, parentd_id=parents_id)
