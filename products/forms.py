from django import forms
from .models import Product, Category, Barrel, Flight, Stem


class ProductForm(forms.ModelForm):
    """ Form for adding products to the database """

    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        barrels = Barrel.objects.all()
        flights = Flight.objects.all()
        stems  = Stem.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        self.fields['category'].choices = friendly_names
        self.fields['barrels'] = forms.ChoiceField(
            choices=[(b.id, b.get_shape_display()) for b in Barrel.objects.all()]
        )
        self.fields['flights'] = forms.ChoiceField(
            choices=[(f.id, f.get_shape_display()) for f in Flight.objects.all()]
        )
        self.fields['stems'] = forms.ChoiceField(
            choices=[(s.id, s.get_length_display()) for s in Stem.objects.all()]
        )
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded'
