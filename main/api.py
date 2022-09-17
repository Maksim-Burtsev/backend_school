from uuid import UUID
from datetime import timedelta

from dateutil import parser

from django.db.models import Q
from django.http import HttpResponse

from ninja import NinjaAPI
from ninja.errors import HttpError, ValidationError

from main.models import Item, ItemHistory
from main.schemas import (
    ImportSchema,
    NodesSchema,
    SaleSchema,
    ItemStaticticSchema,
)
from main.services import (
    update_categories_date,
    set_price_and_childrens,
    get_parents_id,
    save_items,
)
from main.tasks import save_items_in_history
from main.validators import validate_date, validate_id

api = NinjaAPI()


@api.exception_handler(ValidationError)
def validation_errors(request, exc):
    return HttpResponse("Validation Failed", status=400)


@api.post("/imports", response={200: str, 400: str})
def import_data(request, data: ImportSchema):
    request_data = data.dict()

    items = request_data.get("items")
    date = request_data.get("updateDate")

    save_items(items, date)
    update_categories_date(parents_id=get_parents_id(items), date=date)

    save_items_in_history.delay(date)

    return "Success"


@api.delete("/delete/{id}", response={200: str, 404: str})
def delete_item(request, id: UUID):
    try:
        item_obj = Item.objects.get(uuid=id)
    except Item.DoesNotExist:
        raise HttpError(404, "Item not found")
    else:
        item_obj.delete()
        return 200, "Success"


@api.get("/nodes/{id}", response=NodesSchema)
def nodes(request, id: str):
    validate_id(id)
    try:
        item = Item.objects.get(uuid=id)
    except Item.DoesNotExist:
        raise HttpError(404, "Item not found")

    descendants = item.get_descendants().select_related("parent")

    set_price_and_childrens(item, descendants)

    return item


@api.get("/sales", response=list[SaleSchema])
def sales(request, date: str):

    validate_date(date)

    end_date = parser.parse(date)
    start_date = end_date - timedelta(days=1)

    # TODO custom manager
    items = Item.objects.filter(
        Q(last_update__gte=start_date) & Q(last_update__lte=end_date)
    ).select_related("parent")

    return items


@api.get("/node/{id}/statistic", response=list[ItemStaticticSchema])
def statistic(request, id: UUID, dateStart: str = None, dateEnd: str = None):

    try:
        item = Item.objects.get(uuid=id)
    except Item.DoesNotExist:
        raise HttpError(404, "Item not found")

    item_history = ItemHistory.objects.filter(item=item)

    # TODO custom manager + date validators
    if dateStart:
        validate_date(dateStart)
        item_history = item_history.filter(last_update__gte=dateStart)

    if dateEnd:
        validate_date(dateEnd)
        item_history = item_history.filter(last_update__lte=dateEnd)

    return item_history
