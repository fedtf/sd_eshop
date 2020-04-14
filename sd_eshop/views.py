from http import HTTPStatus
from json import JSONDecodeError

from aiohttp import web
from aiohttp.web_exceptions import HTTPBadRequest, HTTPNotFound
from bson.objectid import ObjectId, InvalidId
from umongo import ValidationError

from .models import Product
from .utils import get_object_or_404, Paginator, InvalidPage
from .serializers import ProductDetailSerializer, ProductListSerializer


class ProductListView(web.View):
    async def get(self):
        # would be nicer not to evaluate everything, and only take pages
        # via `skip`/`limit`, but looks like motor doesn't support
        # count on cursor, so we need to cast to list
        # in order to get the amount of objects anyway
        product_list = [
            product async for product in Product.find(self._get_filter_query())
        ]
        product_page = self._paginate_objects(product_list)

        return web.json_response({
            'results': ProductListSerializer(
                many=True).dump(product_page).data,
            'count': product_page.paginator.count,
            'next': self._get_next_page_link(product_page),
            'previous': self._get_previous_page_link(product_page),
        })

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

    def _paginate_objects(self, object_list):
        page_number = self.request.query.get('page', 1)
        paginator = Paginator(
            object_list,
            per_page=self.request.app['config']['objects_per_page']
        )
        try:
            return paginator.page(page_number)
        except InvalidPage as e:
            raise HTTPNotFound(reason=f'Invalid page {page_number}: {str(e)}')

    def _get_next_page_link(self, page):
        if page.has_next():
            return str(
                self.request.url.update_query(page=page.next_page_number()))

    def _get_previous_page_link(self, page):
        if page.has_previous():
            return str(
                self.request.url.update_query(page=page.previous_page_number())
            )


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
