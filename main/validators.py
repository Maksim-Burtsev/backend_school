import re
from enum import Enum
from uuid import UUID

from ninja.errors import HttpError


class TypeEnum(str, Enum):
    CATEGORY = 'CATEGORY'
    OFFER = 'OFFER'

def validate_id(_id: str)-> None:
    try:
        _id = UUID(_id)
    except:
        raise HttpError(400, 'Validation error')

def validate_items(items: dict) -> None:

    validate_type(items)
    validate_price(items)
    validate_parent(items)


def validate_type(items: dict) -> None:
    types_list = [TypeEnum.CATEGORY, TypeEnum.OFFER]
    res_list = [(item['type'] in types_list) for item in items]

    if not all(res_list):
        raise HttpError(400, 'Validation error')


def validate_parent(items: dict) -> None:
    """
    Проверяет чтобы id != parentId
    """
    res_list = [(item['id'] == item['parentId']) for item in items]
    if any(res_list):
        raise HttpError(400, 'Validation error')


def validate_price(items: dict) -> None:
    """
    Проверяет чтобы у price категории был null, а товара >=0
    """
    for item in items:
        if (item['type'] == TypeEnum.CATEGORY and item['price']) or \
                (item['type'] == TypeEnum.OFFER and item['price']) < 0:
            raise HttpError(400, 'Validation error')


def validate_date(date: str) -> None:
    if not _is_date_in_iso8601(date):
        raise HttpError(400, 'Validation error')


def _is_date_in_iso8601(date: str) -> bool:
    """
    Проверяет время на соответствие формату ISO-8601
    """
    regex = r'^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?(Z|[+-](?:2[0-3]|[01][0-9]):[0-5][0-9])?$'

    match_iso8601 = re.compile(regex).match

    try:
        if match_iso8601(date) is not None:
            return True
    except:
        pass
    return False
