from motor.motor_asyncio import AsyncIOMotorClient

from .utils import joining


async def setup_mongo(app):
    connection_uri = _get_mongo_connetion_uri(app['config']['mongo'])
    app['db'] = AsyncIOMotorClient(connection_uri)

    async def close_mongo(app):
        app['db'].close()
    app.on_cleanup.append(close_mongo)


@joining('')
def _get_mongo_connetion_uri(mongo_conf):
    username, password, host, port, database = tuple(map(
        mongo_conf.get,
        ('username', 'password', 'host', 'port', 'database')
    ))

    yield "mongodb://"

    if username and password:
        yield f"{username}:{password}@"

    yield f"{host}:{port}"

    if database:
        yield f"/{database}"
