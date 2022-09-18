from celery import shared_task

from main.models import Item
from main.services import save_in_history


@shared_task
def save_items_in_history(date: str) -> None:
    """Сохраняет состояние элементов в ItemsHistory"""
    items = Item.objects.filter(last_update=date)
    save_in_history(items)
