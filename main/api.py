from ninja import NinjaAPI

from main.models import Item
from main.schemas import ImportSchema
from main.services import _is_date_in_iso8601, _save_item

api = NinjaAPI()

# TODO обработать 422


@api.post("/imports", response={200: str, 400: str})
def hello(request, data: ImportSchema):
    request_data = data.dict()
    date = request_data.get('updateDate')
    if not _is_date_in_iso8601(date):
        # тут раиз 400
        pass

    items = request_data.get('items')
    items_dict = {i['id']: i for i in items}

    items_id = [item['id'] for item in items]

    db_items = Item.objects.filter(uuid__in=items_id)

    for i in items:
        _save_item(item=i, db_items=db_items, date=date, items_dict=items_dict)

    return "Seems good"
