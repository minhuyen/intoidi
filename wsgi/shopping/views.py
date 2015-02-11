from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.

def product(request, slug):
    return HttpResponse("Hello, world. You're at the poll index.")
from wsgi.shopping.models import Product, ProductImage, ProductVariation


def productDetail(request, product_id):

    product = get_object_or_404(Product, pk=product_id)
    product_image_list = ProductImage.objects.filter(product_id=product_id)
    product_option_list = ProductVariation.objects.filter(product_id=product_id)

    return render(request, "pages/product_detail.html", {"product": product,
                  "product_image_list": product_image_list,
                  "product_option_list": product_option_list
    })
