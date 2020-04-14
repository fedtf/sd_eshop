from .models import Product


ProductDetailSerializer = Product.schema.as_marshmallow_schema()


class ProductListSerializer(ProductDetailSerializer):
    class Meta:
        fields = ('id', 'name')
