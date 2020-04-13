import sys

from aiohttp import web

from .db import setup_mongo
from .models import ensure_indexes
from .settings import get_config
from .routes import setup_routes
from .middlewares import error_middleware


def make_app(argv=None):
    app = web.Application(middlewares=[error_middleware])

    app['config'] = get_config(argv)

    app.on_startup.append(setup_mongo)
    app.on_startup.append(ensure_indexes)

    setup_routes(app)

    return app


def main(argv=None):
    app = make_app(argv)
    web.run_app(app, host=app['config']['host'], port=app['config']['port'])


if __name__ == '__main__':
    main(sys.argv[1:])
