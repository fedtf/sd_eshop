from aiohttp import web


class ProductListView(web.View):
    async def get(self):
        return web.Response(text='product list')

    async def post(self):
        return web.Response(text='product create')


class ProductDetailView(web.View):
    async def get(self):
        return web.Response(text='product get')
