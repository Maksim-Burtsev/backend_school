from django.db import models
from django.core.exceptions import ValidationError


class Item(models.Model):
    """Категория"""

    TYPE_CHOICES = (
        ('offer', 'OFFER'),
        ('category', 'CATEGORY'),
    )

    _type = models.CharField(max_length=21, choices=TYPE_CHOICES)
    uuid = models.UUIDField(unique=True)
    parent = models.ForeignKey('self', null=True,
                               blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.IntegerField(null=True, default=None)
    last_update = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        #TODO move exception into api as validation
        if self._type == 'category' and self.price:
            raise ValidationError('Price of category must be null')
        if self._type == 'offer' and self.price < 0:
            raise ValidationError('Price of offer must be >=0')
        
        return super().save(*args, **kwargs)
