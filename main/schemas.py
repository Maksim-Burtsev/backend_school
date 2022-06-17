from enum import Enum
from uuid import UUID

from ninja import Schema


class TypeEnum(str, Enum):
    CATEGORY = 'CATEGORY'
    OFFER = 'OFFER'


class ItemSchema(Schema):
    type: TypeEnum
    id: UUID
    name: str
    parentID: UUID = None
    price: int = None


class ImportSchema(Schema):
    items: list[ItemSchema]
    updateDate: str