import re

from ninja.errors import HttpError

from main.schemas import TypeEnum


def validate_price(items: dict):
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
