from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.functions import Lower

from .models import Product, Category, Barrel, Stem, Flight
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


@login_required
def add_product(request):
    """ Add a product to the store """

    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_details', args=[product.id]))
        else:
            messages.error(request, 'Failed to add product. \
                Please ensure the form is valid.')
    else:
        form = ProductForm()

    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


def get_product_subclass(product):  # For editing a product
    """ Ensure we retrieve the correct subclass instance """

    if Barrel.objects.filter(pk=product.pk).exists():
        return Barrel.objects.get(pk=product.pk)
    elif Stem.objects.filter(pk=product.pk).exists():
        return Stem.objects.get(pk=product.pk)
    elif Flight.objects.filter(pk=product.pk).exists():
        return Flight.objects.get(pk=product.pk)
    return product  # If it's a base Product, return as-is


@login_required
def edit_product(request, product_id):
    """ Edit a product in the store """

    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    # Get the correct subclass instance
    product = get_object_or_404(Product, pk=product_id)
    product_subclass = get_product_subclass(product)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES,
                           instance=product_subclass)

        if form.is_valid():
            print(f'DEBUG: Before saving, Instance PK: \
                  {form.instance.pk}, ID: {form.instance.id}')
            form.save()
            print(f'DEBUG: After saving, Instance PK: \
                  {form.instance.pk}, ID: {form.instance.id}')
            messages.success(request, f'Successfully updated {product.name}')
            return redirect(reverse('product_details', args=[product.id]))
        else:
            messages.error(request,
                           'Failed to update product. \
                            Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product_subclass)
        messages.info(request, f'You are about to edit {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product_subclass,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """ Delete a product from the store """

    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, f'{product.name} has been deleted!')
    return redirect(reverse('products'))
