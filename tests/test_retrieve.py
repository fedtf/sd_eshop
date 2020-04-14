from http import HTTPStatus

from aiohttp.test_utils import unittest_run_loop
from bson import ObjectId

from sd_eshop.models import Product

from .utils import SDEshopTestCase, serialize_product


class ProductRetrieveTestCase(SDEshopTestCase):
    @unittest_run_loop
    async def test_retrieve(self):
        product = Product(
            name='cellar phone',
            description='can call',
            properties={
                'weight': 0.3,
                'length': 700,
            }
        )
        await product.commit()

        response = await self.client.get(f"/products/{product.id}/")
        self.assertEqual(response.status, HTTPStatus.OK)

        result = await response.json()

        self.assertEqual(result, serialize_product(product, detailed=True))

    @unittest_run_loop
    async def test_retrieve_nonexistent_id(self):
        response = await self.client.get(f"/products/{ObjectId()}/")
        self.assertEqual(response.status, HTTPStatus.NOT_FOUND)

        result = await response.json()

        self.assertEqual(result, {'error': 'Not Found'})

    @unittest_run_loop
    async def test_retrieve_invalid_id(self):
        response = await self.client.get(f"/products/nosuchid/")
        self.assertEqual(response.status, HTTPStatus.BAD_REQUEST)

        result = await response.json()

        self.assertEqual(result, {'error': 'Invalid id'})
