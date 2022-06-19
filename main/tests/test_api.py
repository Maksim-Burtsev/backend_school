from django.test import TestCase

from main.models import Item


data = {
    "items": [
        {
            "type": "CATEGORY",
            "name": "Смартфоны",
            "id": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
            "parentId": None,
        },
        {
            "type": "OFFER",
            "name": "jPhone 13",
            "id": "863e1a7a-1304-42ae-943b-179184c077e3",
            "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
            "price": 79999
        },
        {
            "type": "OFFER",
            "name": "Xomiа Readme 10",
            "id": "b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4",
            "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
            "price": 59999
        }
    ],
    "updateDate": "2022-02-02T12:00:00.000Z"
}


class ImportTestCase(TestCase):

    def test_correct_import(self):
        response = self.client.post(
            '/imports', data=data, content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Item.objects.all().count(), 3)

    def test_import_uncorrect_id(self):
        data = {"items": [
                {
                    "type": "CATEGORY",
                    "name": "Test",
                    "id": "wrong_id",
                    "parentId": None,
                }, ],
                "updateDate": "2022-02-02T12:00:00.000Z"
                }

        # снаружи это 400
        with self.assertRaises(TypeError):
            response = self.client.post(
                '/imports', data=data, content_type='application/json')

    def test_import_uncorrect_price(self):
        data = {"items": [
            {
                "type": "CATEGORY",
                "name": "Test",
                "id": "b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4",
                "parentId": None,
                "price": 123
            }, ],
            "updateDate": "2022-02-02T12:00:00.000Z"
        }
        response = self.client.post(
            '/imports', data=data, content_type='application/json')

        self.assertEqual(response.status_code, 400)

    def test_import_negative_price(self):

        data = {"items": [
            {
                "type": "OFFER",
                "name": "Test",
                "id": "b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4",
                "parentId": None,
                "price": -123
            }, ],
            "updateDate": "2022-02-02T12:00:00.000Z"
        }
        response = self.client.post(
            '/imports', data=data, content_type='application/json')

        self.assertEqual(response.status_code, 400)

    def test_import_uncorrect_parendId(self):
        """
        uncorrect -> id=parentId
        """

        data = {"items": [
            {
                "type": "CATEGORY",
                "name": "Test",
                "id": "b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4",
                "parentId": 'b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4',
                "price": None
            }, ],
            "updateDate": "2022-02-02T12:00:00.000Z"
        }
        response = self.client.post(
            '/imports', data=data, content_type='application/json')

        self.assertEqual(response.status_code, 400)

    def test_import_uncorrect_date(self):
        data = {"items": [
            {
                "type": "CATEGORY",
                "name": "Test",
                "id": "b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4",
                "parentId": None,
                "price": None
            }, ],
            "updateDate": "2022:02:22 22:22:22"  # not ISO-8601
        }
        response = self.client.post(
            '/imports', data=data, content_type='application/json')

        self.assertEqual(response.status_code, 400)

    def test_import_uncorrect_type(self):
        data = {"items": [
            {
                "type": "WRONG TYPE",
                "name": "Test",
                "id": "b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4",
                "parentId": None,
                "price": None
            }, ],
            "updateDate": "2022-02-02T12:00:00.000Z"
        }
        response = self.client.post(
            '/imports', data=data, content_type='application/json')

        self.assertEqual(response.status_code, 400)

    