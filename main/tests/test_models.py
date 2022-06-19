from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError

from main.models import Item


class ModelTestCase(TestCase):

    def test_correct_model(self):
        Item.objects.create(
            _type='offer',
            uuid='98883e8f-0507-482f-bce2-2fb306cf6483',
            name='Test',
            price=None,
            last_update=timezone.now()
        )

        self.assertEqual(Item.objects.all().count(), 1)
        self.assertTrue(Item.objects.filter(
            uuid='98883e8f-0507-482f-bce2-2fb306cf6483').exists())

    def test_uncorrect_model(self):

        with self.assertRaises(ValidationError):
            Item.objects.create(
                _type='offer',
                uuid='bad_uuid',
                name='Test',
                price=None,
                last_update=timezone.now()
            )
