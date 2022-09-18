import re
from enum import Enum
from uuid import UUID

from ninja.errors import HttpError


class TypeEnum(str, Enum):
    CATEGORY = "CATEGORY"
    OFFER = "OFFER"


def validate_id(_id: str) -> None:
    """Валидирует id объекта (проверка на UUID)"""
    try:
        _id = UUID(_id)
    except ValueError:
        raise HttpError(400, "Validation error")


def validate_items(items: dict) -> None:
    """
    Валидирует type/price/parentId у списка элементов
    """
    # validate_type(items)
    validate_price(items)
    validate_parent(items)


def validate_type(type: str) -> None:
    """Проверка type на принадлежность CATEGORY или OFFER"""
    if type not in [TypeEnum.CATEGORY, TypeEnum.OFFER]:
        raise HttpError(400, "Validation error")


def validate_parent(id_: UUID, parentId: UUID) -> None:
    """Проверяет чтобы id != parentId"""
    if id_ == parentId:
        raise HttpError(400, "Validation error")


def validate_price(type_: TypeEnum, price: int | None) -> None:
    """Проверяет чтобы у price категории был null, а товара >=0"""
    if (type_ == TypeEnum.CATEGORY and price) or (
        type_ == TypeEnum.OFFER and price < 0
    ):
        raise HttpError(400, "Validation error")


def validate_date(date: str) -> None:
    if not _is_date_in_iso8601(date):
        raise HttpError(400, "Validation error")


def _is_date_in_iso8601(date: str) -> bool:
    """Проверяет время на соответствие формату ISO-8601"""
    regex = r"^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?(Z|[+-](?:2[0-3]|[01][0-9]):[0-5][0-9])?$"

    match_iso8601 = re.compile(regex).match

    try:
        if match_iso8601(date) is not None:
            return True
    except:
        pass
    return False
