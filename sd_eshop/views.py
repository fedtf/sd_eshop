from http import HTTPStatus

from aiohttp import web
from aiohttp.web_exceptions import HTTPBadRequest
from bson.objectid import ObjectId, InvalidId
from umongo import ValidationError

from .models import Product
from .utils import get_object_or_404


class ProductListView(web.View):
    async def get(self):
        products = Product.find(self._get_filter_query())
        return web.json_response(
            [product.dump() async for product in products])

    async def post(self):
        data = await self.request.json()

        try:
            product = Product(**data)
            await product.commit()
        except ValidationError as e:
            raise HTTPBadRequest(reason=e.normalized_messages())

        return web.json_response(product.dump(), status=HTTPStatus.CREATED)

    def _get_filter_query(self):
        query = {}
        request_query = self.request.query

        if 'name' in request_query:
            query['name'] = request_query['name']

        if 'property' in request_query:
            query[f"properties.{request_query['property']}"] = (
                request_query.get('value', {'$exists': True}))

        return query


class ProductDetailView(web.View):
    async def get(self):
        product = await self._get_object()
        return web.json_response(product.dump())

    async def _get_object(self):
        return await get_object_or_404(
            Product, {'_id': self._get_object_id()})

    def _get_object_id(self):
        try:
            object_id = ObjectId(self.request.match_info['product_id'])
        except InvalidId:
            raise HTTPBadRequest(reason='Invalid id')
        return object_id
