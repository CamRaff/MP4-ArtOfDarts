from django.shortcuts import render, get_object_or_404

from .models import Product, Category, Barrel, Flight, Stem
from .forms import ProductForm


def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    template = 'products/all_products.html'
    context = {
        'products': products,
    }

    return render(request, template, context)


def product_details(request, product_id):
    """ A view to show the details of a selected product """

    product = get_object_or_404(Product, pk=product_id)
    template = 'products/product_details.html'
    context = {
        'product': product,
    }

    return render(request, template, context)


def add_product(request):
    """ Add a product to the store """

    form = ProductForm()
    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)
