from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from mezzanine.pages.page_processors import processor_for
from wsgi.shopping.models import HomePage, ProductsPage, Product, ProductImage, Category, ProductOption


@processor_for(ProductsPage)
def products_processor(request, page):
    product_image_list = []
    product_list = Product.objects.all().order_by("updated_date").reverse()
    paginator = Paginator(product_list, 4)

    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    for product in products:
        productImage = ProductImage.objects.filter(product_id=product.id)
        product_image_list.append(productImage[0].image)

    categories = Category.objects.all()
    color_list = ProductOption.objects.filter(type=2)
    return {"products": products, "product_image_list": product_image_list,
            "categories": categories, "color_list": color_list}





