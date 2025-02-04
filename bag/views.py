from django.shortcuts import render, redirect, get_object_or_404
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
                    product_type = f'{flight.get_flight_shape_display()} Flight'
                except Flight.DoesNotExist:
                    product_type = 'Unknown Type'
        # if isinstance(product, Barrel):
        #     product_type = f'{product.get_barrel_shape_display()} Barrel'
        # elif isinstance(product, Stem):
        #     product_type = f'{product.get_stem_length_display()} Stem'
        # elif isinstance(product, Flight):
        #     product_type = f'{product.get_flight_shape_display()} Flight'
        # else:
        #     product_type = 'Unknown Type'

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

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})

    if item_id in list(bag.keys()):
        bag[item_id] += quantity
    else:
        bag[item_id] = quantity

    request.session['bag'] = bag
    # print(request.session['bag'])
    return redirect(redirect_url)
