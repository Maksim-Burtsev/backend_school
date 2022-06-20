from uuid import UUID
from typing import Optional

from ninja import Schema, Field

from main.services import _get_price_and_count_of_category


class ItemSchema(Schema):
    type: str
    id: UUID
    name: str
    parentId: UUID = None
    price: int = None


class ImportSchema(Schema):
    items: list[ItemSchema]
    updateDate: str


class NodesSchema(Schema):
    """
    Схема для /nodes
    """
    name: str
    id: UUID = Field(..., alias='uuid')
    price: int = None
    date: str
    type: str
    parentId: UUID = Field(None, alias='parent.uuid')
    children: list[Optional['NodesSchema']] | None

    @staticmethod
    def resolve_children(obj):
        children = obj.offers.all()
        if children:
            return children
        if obj._type == 'category':
            return []
        return None

    @staticmethod
    def resolve_type(obj):
        return obj._type.upper()

    @staticmethod
    def resolve_price(obj):
        if obj._type == 'offer':
            return obj.price
        res, offers = _get_price_and_count_of_category(obj)
        if res == 0:
            return None
        return int(res/offers)

    @staticmethod
    def resolve_date(obj):
        return obj.last_update.isoformat()[:-6] + '.000Z'


NodesSchema.update_forward_refs()


class SaleSchema(Schema):
    id: UUID = Field(..., alias='uuid')
    name: str
    parentId: UUID = Field(None, alias='parent.uuid')
    type: str
    price: int = None
    date: str

    @staticmethod
    def resolve_type(obj):
        return obj._type.upper()

    @staticmethod
    def resolve_date(obj):
        return obj.last_update.isoformat()[:-6] + '.000Z'

    @staticmethod
    def resolve_price(obj):
        if obj._type == 'offer':
            return obj.price
        res, offers = _get_price_and_count_of_category(obj)
        if res == 0:
            return None
        return int(res/offers)
