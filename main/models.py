from django.db import models


class Item(models.Model):
    """Товар/категория"""

    TYPE_CHOICES = (
        ('offer', 'OFFER'),
        ('category', 'CATEGORY'),
    )

    _type = models.CharField(max_length=21, choices=TYPE_CHOICES)
    uuid = models.UUIDField(unique=True)
    parent = models.ForeignKey('self', null=True,
                               blank=True, on_delete=models.CASCADE, related_name='offers')
    name = models.CharField(max_length=255)
    price = models.IntegerField(null=True, default=None, blank=True)
    last_update = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name


class ItemHistory(models.Model):
    """История товара/категории"""

    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name='history', null=True)
    _type = models.CharField(max_length=21, choices=Item.TYPE_CHOICES)
    uuid = models.UUIDField()
    name = models.CharField(max_length=255)
    parentId = models.UUIDField(null=True)
    price = models.PositiveIntegerField(blank=True, null=True)
    last_update = models.DateTimeField()

    def __str__(self) -> str:
        return self.name