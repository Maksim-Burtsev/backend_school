from uuid import UUID
from datetime import timedelta

from dateutil import parser

from django.db.models import Q

from ninja import NinjaAPI
from ninja.errors import HttpError

from main.models import Item
from main.schemas import ImportSchema, ChildrenSchema, SaleSchema
from main.services import (
    _is_date_in_iso8601,
    _save_item,
    _update_parents_date,
    _get_items_and_parents_id
)

api = NinjaAPI()

# TODO обработать 422


@api.post("/imports", response={200: str, 400: str})
def import_data(request, data: ImportSchema):
    request_data = data.dict()

    items = request_data.get('items')
    date = request_data.get('updateDate')

    if not _is_date_in_iso8601(date):
        raise HttpError(400, 'Validation error')

    items_dict = {i['id']: i for i in items}
    items_id, parents_id = _get_items_and_parents_id(items)

    db_items = Item.objects.filter(uuid__in=items_id)

    for item in items:
        _save_item(item=item, db_items=db_items,
                   date=date, items_dict=items_dict)

    for parent_id in parents_id:
        _update_parents_date(parent_id=parent_id, date=date)

    return "Success"

# TODO 422 -> 400


@api.delete("/delete/{id}", response={200: str, 404: str})
def delete_item(request, id: UUID):
    try:
        item_obj = Item.objects.get(uuid=id)
    except Item.DoesNotExist:
        raise HttpError(404, 'Item not found')
    else:
        item_obj.delete()
        return 200, "Success"


@api.get('/nodes/{id}', response=ChildrenSchema)
def nodes(request, id: UUID):
    try:
        item_obj = Item.objects.get(uuid=id)
    except Item.DoesNotExist:
        raise HttpError(404, 'Item not found')

    return item_obj


@api.get('/sales', response=list[SaleSchema])
def sales(request, date: str):

    if not _is_date_in_iso8601(date):
        raise HttpError(400, 'Validation error')

    end_date = parser.parse(date)
    start_date = end_date - timedelta(days=10)

    items = Item.objects.filter(
        Q(last_update__gte=start_date) & Q(last_update__lte=end_date))

    return items
