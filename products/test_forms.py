from django.test import TestCase
from .models import Category, Barrel, Stem, Flight
from .forms import ProductForm


class ProductFormTest(TestCase):
    def setUp(self):
        # Create categories for testing
        self.barrel_category = Category.objects.create(
            name='Barrels', friendly_name='Barrels')
        self.stem_category = Category.objects.create(
            name='Shafts', friendly_name='Shafts')
        self.flight_category = Category.objects.create(
            name='Flights', friendly_name='Flights')

    def test_product_form_valid(self):
        form_data = {
            'name': 'Test Barrel',
            'description': 'A great test barrel.',
            'price': 29.99,
            'rating': 4,
            'sku': 'TESTBARREL123',
            'category': self.barrel_category.id,
            'barrel_shape': 'Tapered',
        }
        form = ProductForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_product_form_invalid_without_name(self):
        form_data = {
            'description': 'A great test barrel.',
            'price': 29.99,
            'category': self.barrel_category.id,
            'sku': 'TESTBARREL123',
        }
        form = ProductForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_product_form_invalid_without_price(self):
        form_data = {
            'name': 'Test Barrel',
            'description': 'A great test barrel.',
            'category': self.barrel_category.id,
            'sku': 'TESTBARREL123',
        }
        form = ProductForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('price', form.errors)

    def test_save_creates_barrel_instance(self):
        form_data = {
            'name': 'Test Barrel',
            'description': 'A great test barrel.',
            'price': 29.99,
            'sku': 'TESTBARREL123',
            'category': self.barrel_category.id,
            'barrel_shape': 'Tapered',
        }
        form = ProductForm(data=form_data)
        self.assertTrue(form.is_valid())  # Validate the form
        product = form.save()

        self.assertIsInstance(product, Barrel)
        self.assertEqual(product.name, 'Test Barrel')

    def test_save_creates_stem_instance(self):
        form_data = {
            'name': 'Test Stem',
            'description': 'A great test stem.',
            'price': 19.99,
            'sku': 'TESTSTEM123',
            'category': self.stem_category.id,
            'stem_length': 'Medium',
        }
        form = ProductForm(data=form_data)
        self.assertTrue(form.is_valid())  # Validate the form
        product = form.save()

        self.assertIsInstance(product, Stem)
        self.assertEqual(product.name, 'Test Stem')

    def test_save_creates_flight_instance(self):
        form_data = {
            'name': 'Test Flight',
            'description': 'A great test flight.',
            'price': 14.99,
            'sku': 'TESTFLIGHT123',
            'category': self.flight_category.id,
            'flight_shape': 'Kite',
        }
        form = ProductForm(data=form_data)
        self.assertTrue(form.is_valid())  # Validate the form
        product = form.save()

        self.assertIsInstance(product, Flight)
        self.assertEqual(product.name, 'Test Flight')
