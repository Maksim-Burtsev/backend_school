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
