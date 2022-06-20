import uuid
import json

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


class APITestCase(TestCase):

    def test_delete(self):
        Item.objects.create(
            _type='category',
            uuid='b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4',
            name='test',
            last_update='2022-02-02T12:00:00.000Z'
        )

        self.assertEqual(Item.objects.count(), 1)
        _id = 'b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4'
        response = self.client.delete(f'/delete/{_id}')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Item.objects.count(), 0)

    def test_delete_404(self):
        pass

    def test_nodes(self):
        main_cat = Item.objects.create(
            _type='category',
            uuid=uuid.uuid4(),
            name='Main category',
            last_update='2022-02-02T12:00:00.000Z'
        )

        for _ in range(3):
            subcategory = Item.objects.create(
                _type='category',
                uuid=uuid.uuid4(),
                name='test',
                last_update='2022-02-02T12:00:00.000Z',
                parent=main_cat
            )

        for _ in range(3):
            Item.objects.create(
                _type='category',
                uuid=uuid.uuid4(),
                name='Main category',
                last_update='2022-02-02T12:00:00.000Z',
                parent=subcategory

            )

        self.assertEqual(Item.objects.all().count(), 7)

        response = self.client.get(f'/nodes/{main_cat.uuid}')

        self.assertEqual(response.status_code, 200)

        res = json.loads(response.content)
        self.assertEqual(len(res['children']), 3)

    def test_nodes_404(self):
        no_existent_id = uuid.uuid4()
        response = self.client.get(f'/nodes/{no_existent_id}')

        self.assertEqual(response.status_code, 404)

    def test_nodes_offer_childs(self):
        main_cat = Item.objects.create(
            _type='category',
            uuid=uuid.uuid4(),
            name='Main category',
            last_update='2022-02-02T12:00:00.000Z'
        )
        Item.objects.create(
            _type='category',
            uuid=uuid.uuid4(),
            name='test cat',
            last_update='2022-02-02T12:00:00.000Z',
            parent=main_cat
        )
        Item.objects.create(
            _type='offer',
            uuid=uuid.uuid4(),
            name='test offer',
            last_update='2022-02-02T12:00:00.000Z',
            parent=main_cat
        )

        response = self.client.get(f'/nodes/{main_cat.uuid}')

        self.assertEqual(response.status_code, 200)

        res = json.loads(response.content)
        cat = res['children'][0]
        offer = res['children'][1]

        self.assertEqual(cat['children'], [])
        self.assertEqual(offer['children'], None)

    def test_sales(self):
        self.client.post(
            '/imports', data=data, content_type='application/json')
        date = '2022-02-02T12:00:00.000Z'
        response = self.client.get(f'/sales?date={date}')

        self.assertEqual(response.status_code, 200)

        res = json.loads(response.content)
        self.assertEqual(len(res), 3)

    def test_sales_empty(self):
        date = '2022-02-22T12:00:00.000Z'
        response = self.client.get(f'/sales?date={date}')

        self.assertEqual(response.status_code, 200)

        res = json.loads(response.content)
        self.assertEqual(len(res), 0)

    def test_sales_wrong_date(self):
        date = '11:11:1111'
        response = self.client.get(f'/sales?date={date}')

        self.assertEqual(response.status_code, 400)