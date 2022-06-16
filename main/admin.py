from django.contrib import admin

from main.models import Category, Offer

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'name', 'price', 'last_update')


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'name', 'price', 'last_update')
