from django import forms
from .models import Product, Category, Barrel, Flight, Stem
from .widgets import CustomClearableFileInput


class ProductForm(forms.ModelForm):
    """ Form for adding products to the database """

    class Meta:
        model = Product
        fields = '__all__'

    image = forms.ImageField(label='Image', required=False,
                             widget=CustomClearableFileInput)

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
        category = self.cleaned_data.get('category')

        print(f"Category selected: {category}")  # Debugging

        if category:
            # Collect common fields
            category_name = category.name.lower()

            # Debugging
            print(f"Category name after conversion: {category_name}")

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

            # Debugging
            print(f"Common fields: {common_fields}")

            if self.instance.pk:
                # Get the existing instance based on subclass
                if isinstance(self.instance, Barrel):
                    print("Updating Barrel instance...")
                    for key, value in common_fields.items():
                        setattr(self.instance, key, value)
                    self.instance.barrel_shape = (
                        self.cleaned_data.get('barrel_shape'))
                    self.instance.save()
                    return self.instance

                elif isinstance(self.instance, Stem):
                    print("Updating Stem instance...")
                    for key, value in common_fields.items():
                        setattr(self.instance, key, value)
                    self.instance.stem_length = (
                        self.cleaned_data.get('stem_length'))
                    self.instance.save()
                    return self.instance

                elif isinstance(self.instance, Flight):
                    print("Updating Flight instance...")
                    for key, value in common_fields.items():
                        setattr(self.instance, key, value)
                    self.instance.flight_shape = (
                        self.cleaned_data.get('flight_shape'))
                    self.instance.save()
                    return self.instance

            # Check which subclass should be created
            if category_name == 'barrels':
                print("Creating Barrel instance...")
                return Barrel.objects.create(
                    **common_fields,
                    barrel_shape=self.cleaned_data.get('barrel_shape'))
            elif category_name == 'shafts':
                print("Creating Stem instance...")
                return Stem.objects.create(
                    **common_fields,
                    stem_length=self.cleaned_data.get('stem_length'))
            elif category_name == 'flights':
                print("Creating Flight instance...")
                return Flight.objects.create(
                    **common_fields,
                    flight_shape=self.cleaned_data.get('flight_shape'))
            else:
                print("Unknown category, saving as Product.")

        # If no category is selected, save as a generic Product
        return super().save(commit)
