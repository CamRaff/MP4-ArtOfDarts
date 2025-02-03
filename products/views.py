from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower

from .models import Product, Category
from .forms import ProductForm


def all_products(request):
    """ A view to show all products, with sorting and search functionality """

    products = Product.objects.all()
    categories = Category.objects.all()
    query = request.GET.get('q')
    category_filter = request.GET.get('category')
    product_type = request.GET.get('product')
    sort = None
    direction = None

    # Capture current URL for invalid query redirect
    current_url = request.META.get('HTTP_REFERER', reverse('products'))

    # Sorting Products
    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

    current_sorting = f'{sort}_{direction}'

    # Filter by Category
    if 'category' in request.GET:
        categories = request.GET['category'].split(',')
        products = products.filter(category__name__in=categories)
        categories = Category.objects.filter(name__in=categories)

    # Filter by Product Type (Flights, Barrels, Stems)
    if product_type:
        product_filters = {
            'standard': Q(flight__flight_shape__iexact='standard'),
            'kite': Q(flight__flight_shape__iexact='kite'),
            'tapered': Q(barrel__barrel_shape__iexact='tapered'),
            'straight': Q(barrel__barrel_shape__iexact='straight'),
            'short': Q(stem__stem_length__iexact='short'),
            'medium': Q(stem__stem_length__iexact='medium'),
            'long': Q(stem__stem_length__iexact='long'),
        }
        filter_condition = product_filters.get(product_type)
        if filter_condition:
            products = products.filter(filter_condition)

    # Filter by Search Query
    if query:
        if not query.strip():
            messages.error(request, "You didn't enter any search criteria!")
            return redirect(reverse('products'))

        keywords = query.strip().split()
        search_query = Q()

        for keyword in keywords:
            search_query &= (
                Q(name__icontains=keyword) | Q(description__icontains=keyword)
                )

        products = products.filter(search_query)

        # Redirect if no products are found
        if not products.exists():
            messages.warning(request, f'No products found for "{query}".')
            return redirect(current_url)

    context = {
        'products': products,
        'search_term': query,
        'current_sorting': current_sorting,
        'current_categories': category_filter,
        'categories': categories,
    }

    return render(request, 'products/all_products.html', context)


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
