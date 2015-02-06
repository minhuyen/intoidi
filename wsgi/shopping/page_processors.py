from mezzanine.pages.page_processors import processor_for
from wsgi.shopping.models import HomePage, ProductsPage, Product, ProductImage


@processor_for(ProductsPage)
def products_processor(request, page):
    product_list = Product.objects.all().order_by("updated_date")
    product_image_list = []
    for product in product_list:

        productImage = ProductImage.objects.get(product_id=product.id)
        product_image_list.append(productImage.image)
    # product_image_list = ProductImage.objects.all()
    return {"product_list": product_list, "product_image_list": product_image_list}

