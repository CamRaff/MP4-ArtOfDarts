from django.test import TestCase
from checkout.forms import OrderForm


class TestOrderForm(TestCase):
    """Tests for the OrderForm"""

    def test_form_valid_data(self):
        """Test form with valid data"""
        form = OrderForm(data={
            'full_name': 'John Doe',
            'email': 'john@example.com',
            'phone_number': '123456789',
            'street_address1': '123 Main St',
            'street_address2': '',
            'town_or_city': 'Testville',
            'postcode': '12345',
        })
        self.assertTrue(form.is_valid())

    def test_form_missing_required_fields(self):
        """Test form with missing required fields"""
        form = OrderForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('full_name', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('phone_number', form.errors)
        self.assertIn('street_address1', form.errors)
        self.assertIn('town_or_city', form.errors)
        self.assertIn('postcode', form.errors)

    def test_postcode_is_required(self):
        """Test that postcode is required"""
        form = OrderForm(data={
            'full_name': 'John Doe',
            'email': 'john@example.com',
            'phone_number': '123456789',
            'street_address1': '123 Main St',
            'street_address2': '',
            'town_or_city': 'Testville',
            'postcode': '',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('postcode', form.errors)

    def test_field_placeholders(self):
        """Test form field placeholders"""
        form = OrderForm()
        self.assertEqual(
            form.fields['full_name'].widget.attrs['placeholder'],
            'Full Name *')
        self.assertEqual(
            form.fields['email'].widget.attrs['placeholder'],
            'Email Address *')
        self.assertEqual(
            form.fields['phone_number'].widget.attrs['placeholder'],
            'Phone Number *')
        self.assertEqual(
            form.fields['street_address1'].widget.attrs['placeholder'],
            'Street Address 1 *')
        self.assertEqual(
            form.fields['street_address2'].widget.attrs['placeholder'],
            'Street Address 2')
        self.assertEqual(
            form.fields['town_or_city'].widget.attrs['placeholder'],
            'Town or City *')
        self.assertEqual(
            form.fields['postcode'].widget.attrs['placeholder'],
            'Postcode *')

    def test_autofocus_on_full_name(self):
        """Test that autofocus is set on full_name"""
        form = OrderForm()
        self.assertTrue(form.fields['full_name'].widget.attrs.get('autofocus'))
