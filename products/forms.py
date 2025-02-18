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

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')

        if category and category.name == 'Barrel':
            if not cleaned_data.get('barrel_shape'):
                self.add_error('barrel_shape',
                               'This field is required for Barrels.')
        elif category and category.name == 'Shafts':
            if not cleaned_data.get('stem_length'):
                self.add_error('stem_length',
                               'This field is required for Shafts.')
        elif category and category.name == 'Flights':
            if not cleaned_data.get('flight_shape'):
                self.add_error('flight_shape',
                               'This field is required for Flights.')

        return cleaned_data
