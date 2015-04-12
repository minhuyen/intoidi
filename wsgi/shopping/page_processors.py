from cartridge.shop.models import Sale, Category, ProductOption
from mezzanine.pages.page_processors import processor_for
from shopping.models import HomePage, MySale


@processor_for(HomePage)
def deal_of_week(request, page):
    deals = MySale.secondary.get_active()
    list_products = []
    context = {}
    if deals:
        for deal in deals:
            list_products.extend(deal.all_products())
    context = {"deals": list_products}
    print "context: ", context
    return context

@processor_for(Category)
def get_product_option_color(request, page):
    color = 2
    color_list = ProductOption.objects.filter(type=color)
    context = {"color_list": color_list}
    return context