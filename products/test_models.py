from django.test import TestCase
from .models import Category, Product, Barrel, Stem, Flight


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Barrels',
            friendly_name='Dart Barrels'
        )

    def test_string_representation(self):
        self.assertEqual(str(self.category), 'Barrels')

    def test_get_friendly_name(self):
        self.assertEqual(self.category.get_friendly_name(), 'Dart Barrels')


class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Barrels')
        self.product = Product.objects.create(
            category=self.category,
            name='Premium Barrel',
            description='High quality dart barrel.',
            price=19.99,
            sku='SKU12345'
        )

    def test_string_representation(self):
        self.assertEqual(str(self.product), 'Premium Barrel (Barrels)')

    def test_product_fields(self):
        self.assertEqual(self.product.name, 'Premium Barrel')
        self.assertEqual(self.product.category.name, 'Barrels')
        self.assertEqual(self.product.price, 19.99)
        self.assertIsNone(self.product.rating)
        self.assertFalse(bool(self.product.image))  # Check if image is empty
        self.assertIsNone(self.product.image_url)


class BarrelModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Barrels')
        self.barrel = Barrel.objects.create(
            category=self.category,
            name='Straight Barrel',
            description='Straight shaped dart barrel.',
            price=15.99,
            sku='SKU54321',
            barrel_shape='Straight'
        )

    def test_string_representation(self):
        self.assertEqual(str(self.barrel), 'Straight Barrel (Barrels)')

    def test_barrel_shape(self):
        self.assertEqual(self.barrel.barrel_shape, 'Straight')


class StemModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Shafts')
        self.stem = Stem.objects.create(
            category=self.category,
            name='Medium Stem',
            description='Medium length dart stem.',
            price=9.99,
            sku='SKU67890',
            stem_length='Medium'
        )

    def test_string_representation(self):
        self.assertEqual(str(self.stem), 'Medium Stem (Shafts)')

    def test_stem_length(self):
        self.assertEqual(self.stem.stem_length, 'Medium')


class FlightModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Flights')
        self.flight = Flight.objects.create(
            category=self.category,
            name='Standard Flight',
            description='Standard shape dart flight.',
            price=5.99,
            sku='SKU98765',
            flight_shape='Standard'
        )

    def test_string_representation(self):
        self.assertEqual(str(self.flight), 'Standard Flight (Flights)')

    def test_flight_shape(self):
        self.assertEqual(self.flight.flight_shape, 'Standard')


if __name__ == '__main__':
    TestCase.main()
