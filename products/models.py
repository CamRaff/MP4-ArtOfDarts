from django.db import models

# Create your models here.


class Category(models.Model):
    """ Product categories model like 'Barrels', 'Flights', 'Shafts' """

    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=255)
    friendly_name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):
    """ Abstract base model for all products """

    class Meta:
        verbose_name_plural = 'Products'
        # abstract = True

    category = models.ForeignKey('Category', related_name='products',
                                 null=True, blank=True,
                                 on_delete=models.SET_NULL)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(max_digits=6, decimal_places=2,
                                 blank=True, null=True)
    sku = models.CharField(max_length=255, blank=True, null=True, unique=True)
    # sku = Stock Keeping Unit
    image = models.ImageField(blank=True, null=True)
    image_url = models.URLField(max_length=1024, blank=True, null=True)

    def __str__(self):
        return f'{self.name} ({self.category.name})'


class Barrel(Product):
    """ Dart barrel model with shape and weight """

    BARREL_SHAPES = [('Straight', 'Straight'), ('Tapered', 'Tapered')]
    barrel_shape = models.CharField(max_length=255, choices=BARREL_SHAPES)
    weight = models.DecimalField(max_digits=4, decimal_places=1)


class Stem(Product):
    """ Dart stem model with length """

    STEM_LENGTHS = [('Short', 'Short'), ('Medium', 'Medium'), ('Long', 'Long')]
    length = models.CharField(max_length=255, choices=STEM_LENGTHS)


class Flight(Product):
    """ Dart flight model with shape """

    FLIGHT_SHAPES = [('Standard', 'Standard'), ('Kite', 'Kite')]
    shape = models.CharField(max_length=255, choices=FLIGHT_SHAPES)
