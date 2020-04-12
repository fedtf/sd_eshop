import sys
import asyncio

from aiohttp import web

from .db import setup_mongo
from .settings import get_config
from .routes import setup_routes


def main(argv=None):
    app = web.Application()
    config = get_config(argv)

    app['config'] = config
    asyncio.get_event_loop().run_until_complete(setup_mongo(app))
    setup_routes(app)

    web.run_app(app, host=config['host'], port=config['port'])


if __name__ == '__main__':
    main(sys.argv[1:])
