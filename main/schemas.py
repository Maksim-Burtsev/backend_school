from uuid import UUID
from typing import Optional

from ninja import Schema, Field

from main.services import get_price, get_date_in_iso


class ItemSchema(Schema):
    """Схема объекта Item"""
    type: str
    id: UUID
    name: str
    parentId: UUID = None
    price: int = None


class ImportSchema(Schema):
    """Схема для /import"""
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
        return obj.children

    @staticmethod
    def resolve_type(obj):
        return obj._type.upper()

    @staticmethod
    def resolve_date(obj):
        return get_date_in_iso(obj)


NodesSchema.update_forward_refs()


class SaleSchema(Schema):
    """Схема для /sales"""
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
        return get_date_in_iso(obj)

    @staticmethod
    def resolve_price(obj):
        price = get_price(obj)
        return price


class ItemStaticticSchema(Schema):
    """Схема для /node/{id}/statistic"""
    id: UUID = Field(..., alias='uuid')
    name: str
    parentId: UUID = None
    type: str = Field(..., alias='_type')
    price: int = None
    date: str

    @staticmethod
    def resolve_date(obj):
        return get_date_in_iso(obj)
