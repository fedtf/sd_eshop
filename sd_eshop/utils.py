from uuid import uuid4

from aiohttp.web_exceptions import HTTPNotFound


def joining(sep):
    """Joins decorated function results with sep."""
    def deco(func):
        def wrapped_func(*args, **kwargs):
            return sep.join(map(str, func(*args, **kwargs)))
        return wrapped_func
    return deco


def generate_random_string():
    return str(uuid4()).replace('-', '')


async def get_object_or_404(model, query):
    obj = await model.find_one(query)

    if not obj:
        raise HTTPNotFound()

    return obj
