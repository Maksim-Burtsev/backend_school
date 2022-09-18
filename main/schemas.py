from uuid import UUID
from typing import Optional

from pydantic import validator, root_validator
from ninja import Schema, Field

from main.services import get_price, get_date_in_iso
from main.validators import (
    validate_date,
    validate_id,
    validate_type,
    validate_price,
    validate_parent,
)

class QueryDates(Schema):
    dateStart: str | None
    dateEnd: str | None

    @root_validator
    def date_is_valid_format(cls, values: dict) -> dict:
        dateStart, dateEnd = values.get("dateStart"), values.get("dateEnd")

        if dateStart:
            validate_date(dateStart)
        if dateEnd:
            validate_date(dateEnd)

        return values

class QueryDate(Schema):
    date: str

    @validator("date")
    def date_is_valid(cls, date: str) -> str:
        validate_date(date)
        return date
 
class PathId(Schema):
    id: str

    @validator("id")
    def id_is_valid(cls, id: str) -> str:
        validate_id(id)
        return id

        

class ItemSchema(Schema):
    """Схема объекта Item"""

    type: str
    id: UUID
    name: str
    parentId: UUID = None
    price: int = None

    @validator("type")
    def type_is_valid(cls, type: str) -> str:
        validate_type(type)
        return type

    @root_validator
    def price_is_valid(cls, values: dict) -> dict:
        validate_price(values.get("type"), values.get("price"))
        return values

    @root_validator
    def parentId_is_valid(cls, values: dict) -> dict:
        validate_parent(values.get("id"), values.get("parentId"))
        return values


class ImportSchema(Schema):
    """Схема для /import"""

    items: list[ItemSchema]
    updateDate: str

    @validator("updateDate")
    def date_is_valid(cls, date: str) -> str:
        validate_date(date)
        return date


class NodesSchema(Schema):
    """
    Схема для /nodes
    """

    name: str
    id: UUID = Field(..., alias="uuid")
    price: int = None
    date: str
    type: str
    parentId: UUID = Field(None, alias="parent.uuid")
    children: list[Optional["NodesSchema"]] | None

    @staticmethod
    def resolve_type(obj):
        return obj._type.upper()

    @staticmethod
    def resolve_date(obj):
        return get_date_in_iso(obj)


NodesSchema.update_forward_refs()


class SaleSchema(Schema):
    """Схема для /sales"""

    id: UUID = Field(..., alias="uuid")
    name: str
    parentId: UUID = Field(None, alias="parent.uuid")
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

    id: UUID = Field(..., alias="uuid")
    name: str
    parentId: UUID = None
    type: str = Field(..., alias="_type")
    price: int = None
    date: str

    @staticmethod
    def resolve_date(obj):
        return get_date_in_iso(obj)
