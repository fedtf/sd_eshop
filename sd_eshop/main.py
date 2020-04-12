import sys

from aiohttp import web

from .db import setup_mongo
from .models import ensure_indexes
from .settings import get_config
from .routes import setup_routes


def main(argv=None):
    app = web.Application()
    config = get_config(argv)

    app['config'] = config
    app.on_startup.append(setup_mongo)
    app.on_startup.append(ensure_indexes)
    setup_routes(app)

    web.run_app(app, host=config['host'], port=config['port'])


if __name__ == '__main__':
    main(sys.argv[1:])
