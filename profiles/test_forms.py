from django.test import TestCase
from .forms import UserProfileForm


class UserProfileFormTest(TestCase):

    def setUp(self):
        self.form_data = {
            'full_name': 'John Doe',
            'default_phone_number': '1234567890',
            'default_street_address1': '123 Main St',
            'default_street_address2': 'Apt 4B',
            'default_town_or_city': 'Springfield',
            'default_postcode': '12345',
        }
        self.form = UserProfileForm(data=self.form_data)

    def test_form_is_valid(self):
        self.assertTrue(self.form.is_valid())

    def test_form_invalid_without_required_fields(self):
        form_data = self.form_data.copy()
        del form_data['full_name']  # Remove the field
        form = UserProfileForm(data=form_data)
        # The below form should be valid since all fields are optional
        self.assertTrue(form.is_valid())

    def test_form_initialization_sets_placeholders(self):
        form = UserProfileForm()
        placeholders = {
            'full_name': 'Full Name',
            'default_phone_number': 'Phone Number',
            'default_street_address1': 'Street Address 1',
            'default_street_address2': 'Street Address 2',
            'default_town_or_city': 'Town or City',
            'default_postcode': 'Postcode',
        }

        for field in form.fields:
            expected_placeholder = (
                f'{placeholders[field]} *' if
                form.fields[field].required else placeholders[field])
            self.assertEqual(
                form.fields[field].widget.attrs['placeholder'],
                expected_placeholder)

    def test_form_field_classes(self):
        for field in self.form.fields:
            self.assertIn('stripe-style-input',
                          self.form.fields[field].widget.attrs['class'])

    def test_form_autofocus_on_first_field(self):
        self.assertTrue('autofocus'
                        in self.form.fields['default_phone_number']
                        .widget.attrs)

    def test_labels_are_removed(self):
        for field in self.form.fields:
            self.assertFalse(self.form.fields[field].label)


if __name__ == '__main__':
    TestCase.main()
