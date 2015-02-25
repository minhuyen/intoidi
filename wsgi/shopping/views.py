from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.template import RequestContext

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


def product(request, slug):
    return HttpResponse("Hello, world. You're at the poll index.")
from wsgi.shopping.models import Product, ProductImage, ProductVariation


def productDetail(request, product_id):

    product = get_object_or_404(Product, pk=product_id)
    if product:
        views = product.view + 1
        product.view = views
        product.save()
    product_image_list = ProductImage.objects.filter(product_id=product_id)
    product_option_list = ProductVariation.objects.filter(product_id=product_id)


    return render(request, "pages/product_detail.html", {"product": product,
                  "product_image_list": product_image_list,
                  "product_option_list": product_option_list
    })


@login_required
def like_product(request):
    product_id = None
    if request.method == 'GET':
        product_id = request.GET['product_id']

    if product_id:
        product = Product.objects.get(id=product_id)
        if product:
            is_liked = "is_liked" + product_id
            checkLiked = request.session.get(is_liked, False)
            if(checkLiked):
                likes = product.like - 1
                response = HttpResponse(likes)
                request.session[is_liked] = False
            else:
                likes = product.like + 1
                response = HttpResponse(likes)
                request.session[is_liked] = True
            product.like = likes
            product.save()
            # print is_liked
    return response
