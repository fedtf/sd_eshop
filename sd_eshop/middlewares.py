from aiohttp import web


@web.middleware
async def error_middleware(request, handler):
    try:
        response = await handler(request)
    except web.HTTPClientError as e:
        return web.json_response({'error': e.reason}, status=e.status)
    return response
