from http import HTTPStatus

from aiohttp.test_utils import unittest_run_loop

from sd_eshop.models import Product

from .utils import SDEshopTestCase


class ProductCreateTestCase(SDEshopTestCase):
    @unittest_run_loop
    async def test_create_item(self):
        data = {
            'name': 'cellar phone',
            'description': 'can call',
            'properties': {
                'weight': 0.3,
                'length': 700,
            }
        }
        response = await self.client.post("/products/", json=data)
        self.assertEqual(response.status, HTTPStatus.CREATED)

        products = [product async for product in Product.find({})]

        self.assertEqual(len(products), 1)
        self.assertHasProperties(products[0], **data)

    @unittest_run_loop
    async def test_cant_create_wo_empty_required_fields(self):
        data = {
            'name': 'cellar phone',
            'description': 'can call',
            'properties': {
                'weight': 0.3,
                'length': 700,
            }
        }
        required_fields = ('name', 'description')
        for field in required_fields:
            with self.subTest(required_field=field):
                response = await self.client.post(
                    "/products/",
                    json={
                        key: value for key, value in data.items()
                        if key != field
                    }
                )
                self.assertEqual(response.status, HTTPStatus.BAD_REQUEST)

                products = [product async for product in Product.find({})]

                self.assertEqual(len(products), 0)
