from .views import ProductListView, ProductDetailView


def setup_routes(app):
    app.router.add_view('/products/', ProductListView)
    app.router.add_view('/products/{product_id}', ProductDetailView)
