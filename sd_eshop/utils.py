from uuid import uuid4


def joining(sep):
    """Joins decorated function results with sep."""
    def deco(func):
        def wrapped_func(*args, **kwargs):
            return sep.join(map(str, func(*args, **kwargs)))
        return wrapped_func
    return deco


def generate_random_string():
    return str(uuid4()).replace('-', '')
