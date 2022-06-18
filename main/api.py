from uuid import UUID

from ninja import NinjaAPI
from ninja.errors import HttpError

from main.models import Item
from main.schemas import ImportSchema, ChildrenSchema
from main.services import _is_date_in_iso8601, _save_item

api = NinjaAPI()

# TODO обработать 422


@api.post("/imports", response={200: str, 400: str})
def import_data(request, data: ImportSchema):
    request_data = data.dict()
    date = request_data.get('updateDate')
    if not _is_date_in_iso8601(date):
        raise HttpError(400, 'Validation error')

    items = request_data.get('items')
    items_dict = {i['id']: i for i in items}

    items_id = [item['id'] for item in items]

    parents_id = [item['parentId'] for item in items]
    items_id.extend(parents_id)
    items_id = list(set(items_id))

    db_items = Item.objects.filter(uuid__in=items_id)

    for i in items:
        _save_item(item=i, db_items=db_items, date=date, items_dict=items_dict)

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
