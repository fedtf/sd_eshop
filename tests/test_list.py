from http import HTTPStatus

from aiohttp.test_utils import unittest_run_loop

from sd_eshop.models import Product

from .utils import SDEshopTestCase, serialize_product


class ProductListTestCase(SDEshopTestCase):
    async def setUpAsync(self):
        self.product0 = Product(
            name='product0',
            description='desc0',
            properties={'prop0': '0', 'prop1': '1'}
        )
        self.product1 = Product(
            name='product1',
            description='desc1',
            properties={'prop0': '1', 'prop1': '0', 'additional_prop': 'abc'}
        )

        await self.product0.commit()
        await self.product1.commit()

    @unittest_run_loop
    async def test_list(self):
        response = await self.client.get("/products/")
        self.assertEqual(response.status, HTTPStatus.OK)

        results = await response.json()

        self.assertEqual(
            results,
            list(map(serialize_product, (self.product0, self.product1)))
        )

    @unittest_run_loop
    async def test_filter_by_name(self):
        response = await self.client.get(
            "/products/", params={'name': 'product0'})
        self.assertEqual(response.status, HTTPStatus.OK)

        results = await response.json()

        self.assertEqual(
            results, list(map(serialize_product, (self.product0,))))

    @unittest_run_loop
    async def test_filter_by_common_property(self):
        response = await self.client.get(
            "/products/", params={'property': 'prop0', 'value': '0'})
        self.assertEqual(response.status, HTTPStatus.OK)

        results = await response.json()

        self.assertEqual(
            results, list(map(serialize_product, (self.product0,))))

    @unittest_run_loop
    async def test_filter_by_noncommon_property(self):
        response = await self.client.get(
            "/products/",
            params={'property': 'additional_prop', 'value': 'abc'}
        )
        self.assertEqual(response.status, HTTPStatus.OK)

        results = await response.json()

        self.assertEqual(
            results, list(map(serialize_product, (self.product1,))))

    @unittest_run_loop
    async def test_filter_by_nonexistant_property(self):
        response = await self.client.get(
            "/products/", params={'property': 'fake_prop', 'value': 'abc'})
        self.assertEqual(response.status, HTTPStatus.OK)

        results = await response.json()

        self.assertEqual(results, [])

    @unittest_run_loop
    async def test_filter_by_property_wo_value(self):
        response = await self.client.get(
            "/products/", params={'property': 'additional_prop'})
        self.assertEqual(response.status, HTTPStatus.OK)

        results = await response.json()

        self.assertEqual(
            results, list(map(serialize_product, (self.product1,))))

    @unittest_run_loop
    async def test_irrelevant_params(self):
        response = await self.client.get(
            "/products/",
            params={
                'value': '0',
                'description': 'desc0',
                'random_param': 'random_value'
            }
        )
        self.assertEqual(response.status, HTTPStatus.OK)

        results = await response.json()

        self.assertEqual(
            results,
            list(map(serialize_product, (self.product0, self.product1)))
        )
