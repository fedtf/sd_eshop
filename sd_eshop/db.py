from motor.motor_asyncio import AsyncIOMotorClient
from umongo import MotorAsyncIOInstance

from .utils import joining


instance = MotorAsyncIOInstance()


async def setup_mongo(app):
    connection_uri = _get_mongo_connetion_uri(app['config']['mongo'])
    app['db'] = AsyncIOMotorClient(connection_uri).get_database()

    instance.init(app['db'])

    async def close_mongo(app):
        app['db'].client.close()
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
