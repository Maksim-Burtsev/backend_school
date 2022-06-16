from django.db import models


class Category(models.Model):
    """Категория"""

    uuid = models.UUIDField(unique=True)
    parent = models.ForeignKey('self', null=True,
                               blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.IntegerField(null=True, default=None)
    last_update = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name


class Offer(models.Model):
    """Товар"""

    uuid = models.UUIDField()
    parent = models.ForeignKey(Category, null=True,
                               on_delete=models.CASCADE, related_name='offers')
    name = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    last_update = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name
