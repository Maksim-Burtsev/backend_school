from uuid import UUID
from datetime import timedelta

from dateutil import parser

from django.db.models import Q
from django.http import HttpResponse

from ninja import NinjaAPI, Path, Query
from ninja.errors import HttpError, ValidationError

from main.models import Item, ItemHistory
from main.schemas import (
    PathId,
    QueryDate,
    QueryDates,
    SaleSchema,
    NodesSchema,
    ImportSchema,
    ItemStaticticSchema,
)
from main.services import (
    save_items,
    get_parents_id,
    update_categories_date,
    set_price_and_childrens,
)
from main.tasks import save_items_in_history

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
def nodes(request, params: PathId = Path(...)):
    try:
        item = Item.objects.get(uuid=params.id)
    except Item.DoesNotExist:
        raise HttpError(404, "Item not found")

    descendants = item.get_descendants().select_related("parent")

    set_price_and_childrens(item, descendants)

    return item


@api.get("/sales", response=list[SaleSchema])
def sales(request, params: QueryDate = Query(...)):
    date = parser.parse(params.date)

    items = Item.objects.last_day_from(date)
    return items


@api.get("/node/{id}/statistic", response=list[ItemStaticticSchema])
def statistic(
    request,
    path_params: PathId = Path(...),
    query_params: QueryDates = Query(default=None),
):

    date_start, date_end = query_params.dateStart, query_params.dateEnd

    try:
        item = Item.objects.get(uuid=path_params.id)
    except Item.DoesNotExist:
        raise HttpError(404, "Item not found")

    item_history = ItemHistory.objects.item_between_dates(item, date_start, date_end)

    return item_history
