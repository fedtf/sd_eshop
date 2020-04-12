from umongo import Document, fields

from .db import instance


@instance.register
class Product(Document):
    name = fields.StrField(required=True)
    description = fields.StrField(required=True)
    properties = fields.DictField(default=dict)


async def ensure_indexes(app):
    await Product.ensure_indexes()
