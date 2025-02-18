from django import forms
from .models import Product, Category, Barrel, Flight, Stem


class ProductForm(forms.ModelForm):
    """ Form for adding products to the database """

    class Meta:
        model = Product
        fields = '__all__'

    barrel_shape = forms.ChoiceField(choices=Barrel.BARREL_SHAPES,
                                     required=False)
    stem_length = forms.ChoiceField(choices=Stem.STEM_LENGTHS, required=False)
    flight_shape = forms.ChoiceField(choices=Flight.FLIGHT_SHAPES,
                                     required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        self.fields['category'].choices = friendly_names

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded white black'

    def save(self, commit=True):
        """
        Override the save method to ensure the product is saved
        as the correct subclass (Barrel, Stem, or Flight)
        """
        product = super().save(commit=False)  # Create product instance but don’t save yet
        category = self.cleaned_data.get('category')

        print(f"Category selected: {category}")  # Debugging

        if category:
            # Collect common fields
            category_name = category.name.lower()

            print(f"Category name after conversion: {category_name}")  # Debugging

            common_fields = {
                "name": self.cleaned_data.get('name'),
                "description": self.cleaned_data.get('description'),
                "price": self.cleaned_data.get('price'),
                "rating": self.cleaned_data.get('rating'),
                "sku": self.cleaned_data.get('sku'),
                "image": self.cleaned_data.get('image'),
                "image_url": self.cleaned_data.get('image_url'),
                "category": category,
            }

            print(f"Common fields: {common_fields}")  # Debugging

            # Check which subclass should be created
            if category_name == 'barrels':
                print("Creating Barrel instance...")
                return Barrel.objects.create(**common_fields, barrel_shape=self.cleaned_data.get('barrel_shape'))
            elif category_name == 'shafts':
                print("Creating Stem instance...")
                return Stem.objects.create(**common_fields, stem_length=self.cleaned_data.get('stem_length'))
            elif category_name == 'flights':
                print("Creating Flight instance...")
                return Flight.objects.create(**common_fields, flight_shape=self.cleaned_data.get('flight_shape'))
            else:
                print("Unknown category, saving as Product.")

        # If no category is selected, save as a generic Product
        return super().save(commit)


        # if category:
        #     if category.name == 'Barrels':
        #         product = Barrel.objects.create(
        #             name=product.name,
        #             description=product.description,
        #             price=product.price,
        #             rating=product.rating,
        #             sku=product.sku,
        #             image=product.image,
        #             image_url=product.image_url,
        #             category=category,
        #             barrel_shape=self.cleaned_data.get('barrel_shape')
        #         )
        #     elif category.name == 'Shafts':
        #         product = Stem.objects.create(
        #             name=product.name,
        #             description=product.description,
        #             price=product.price,
        #             rating=product.rating,
        #             sku=product.sku,
        #             image=product.image,
        #             image_url=product.image_url,
        #             category=category,
        #             stem_length=self.cleaned_data.get('stem_length')
        #         )
        #     elif category.name == 'Flights':
        #         product = Flight.objects.create(
        #             name=product.name,
        #             description=product.description,
        #             price=product.price,
        #             rating=product.rating,
        #             sku=product.sku,
        #             image=product.image,
        #             image_url=product.image_url,
        #             category=category,
        #             flight_shape=self.cleaned_data.get('flight_shape')
        #         )

        # if commit:
        #     product.save()

        # return product

    # def clean(self):
    #     cleaned_data = super().clean()
    #     category = cleaned_data.get('category')

    #     if category and category.name == 'Barrel':
    #         if not cleaned_data.get('barrel_shape'):
    #             self.add_error('barrel_shape',
    #                            'This field is required for Barrels.')
    #     elif category and category.name == 'Shafts':
    #         if not cleaned_data.get('stem_length'):
    #             self.add_error('stem_length',
    #                            'This field is required for Shafts.')
    #     elif category and category.name == 'Flights':
    #         if not cleaned_data.get('flight_shape'):
    #             self.add_error('flight_shape',
    #                            'This field is required for Flights.')

    #     return cleaned_data
