from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q

from .models import Product, Category, Barrel, Flight, Stem
from .forms import ProductForm


def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    template = 'products/all_products.html'
    query = None
    category = None
    product_type = request.GET.get('product')

    if request.GET:
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if product_type:
            if product_type in ['standard', 'kite']:  # Flight shapes
                products = Flight.objects.filter(
                    flight_shape__iexact=product_type
                    )
            elif product_type in ['tapered', 'straight']:  # Barrel shapes
                products = Product.objects.filter(
                    barrel__barrel_shape__iexact=product_type
                    )
            elif product_type in ['short', 'medium', 'long']:  # Stem lengths
                products = Product.objects.filter(
                    stem__stem_length__iexact=product_type
                    )

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request,
                               "You didn't enter any search criteria!")
                return redirect(reverse('products'))

            queries = (
                Q(name__icontains=query) | Q(description__icontains=query)
                )
            products = products.filter(queries)

    context = {
        'products': products,
        'search_term': query,
        'current_categories': category,
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
