from aiohttp import web


class ProductListView(web.View):
    async def get(self):
        return web.json_response({})

    async def post(self):
        return web.json_response({})


class ProductDetailView(web.View):
    async def get(self):
        return web.json_response({})
