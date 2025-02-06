from django.shortcuts import (
    render, redirect, get_object_or_404, reverse, HttpResponse
)
from django.contrib import messages
from products.models import Product, Barrel, Stem, Flight


def view_bag(request):
    """ A view that renders the bag contents page """

    bag = request.session.get('bag', {})
    bag_items = []

    for item_id, quantity in bag.items():
        product = get_object_or_404(Product, pk=item_id)

        try:
            barrel = Barrel.objects.get(pk=product.pk)
            product_type = f'{barrel.get_barrel_shape_display()} Barrel'
        except Barrel.DoesNotExist:
            try:
                stem = Stem.objects.get(pk=product.pk)
                product_type = f'{stem.get_stem_length_display()} Stem'
            except Stem.DoesNotExist:
                try:
                    flight = Flight.objects.get(pk=product.pk)
                    product_type = (
                        f'{flight.get_flight_shape_display()} Flight'
                        )
                except Flight.DoesNotExist:
                    product_type = 'Unknown Type'

        bag_items.append({
            'product': product,
            'quantity': quantity,
            'product_type': product_type,
        })

    context = {
        'bag_items': bag_items,
    }

    return render(request, 'bag/bag.html', context)


def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})

    item_id = str(item_id)
    if item_id in list(bag.keys()):
        bag[item_id] += quantity
    else:
        bag[item_id] = quantity
        messages.success(
            request, f'Successfully added {product.name} to your shopping bag'
            )

    request.session['bag'] = bag
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """ Adjust the quantity of a desired item in shopping bag """

    # product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    bag = request.session.get('bag', {})

    if quantity > 0:
        bag[str(item_id)] = quantity
    else:
        bag.pop(str(item_id), None)

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """ Remove the item from the shopping bag """
    try:
        bag = request.session.get('bag', {})

        bag.pop(str(item_id), None)
        request.session['bag'] = bag
        return HttpResponse(status=200)
    except Exception as e:
        return HttpResponse(status=500)
