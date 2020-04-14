from http import HTTPStatus
from json import JSONDecodeError

from aiohttp import web
from aiohttp.web_exceptions import HTTPBadRequest
from bson.objectid import ObjectId, InvalidId
from umongo import ValidationError

from .models import Product
from .utils import get_object_or_404
from .serializers import ProductDetailSerializer, ProductListSerializer


class ProductListView(web.View):
    async def get(self):
        products = Product.find(self._get_filter_query())
        serialized_products = [
            ProductListSerializer().dump(product).data
            async for product in products
        ]
        return web.json_response(serialized_products)

    async def post(self):
        try:
            data = await self.request.json()
        except JSONDecodeError:
            raise HTTPBadRequest(reason='Invalid json')

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
        return web.json_response(ProductDetailSerializer().dump(product).data)

    async def _get_object(self):
        return await get_object_or_404(
            Product, {'_id': self._get_object_id()})

    def _get_object_id(self):
        try:
            object_id = ObjectId(self.request.match_info['product_id'])
        except InvalidId:
            raise HTTPBadRequest(reason='Invalid id')
        return object_id
