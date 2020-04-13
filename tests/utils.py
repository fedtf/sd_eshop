import sys

from aiohttp.test_utils import AioHTTPTestCase

from sd_eshop.main import make_app
from sd_eshop.utils import generate_random_string


class SDEshopTestCase(AioHTTPTestCase):
    async def get_application(self):
        app = make_app(sys.argv[:1])

        random_str = generate_random_string()
        app['config']['mongo']['database'] = f'test_db_{random_str}'

        return app

    async def tearDownAsync(self):
        await self.app['db'].client.drop_database(self.app['db'])

    def assertHasProperties(self, obj, **properties):
        for name, expected_value in properties.items():
            if not hasattr(obj, name):
                raise AssertionError('Object has no "%s" property' % name)
            value = getattr(obj, name)
            self.assertEqual(
                value,
                expected_value,
                'Object has unexpected value for "%s" property' % name
            )


def serialize_product(product):
    return {
        'id': str(product.id),
        'name': product.name,
        'description': product.description,
        'properties': product.properties,
    }
