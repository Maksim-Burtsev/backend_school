from django.contrib import admin

from main.models import Item, ItemHistory


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("_type", "uuid", "name", "price", "last_update")


@admin.register(ItemHistory)
class ItemHistoryAdmin(admin.ModelAdmin):
    list_display = ("_type", "uuid", "name", "price", "last_update")
