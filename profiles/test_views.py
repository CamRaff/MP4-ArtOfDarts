from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from .models import UserProfile
from checkout.models import Order


class ProfileViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser',
                                             password='testpassword')
        self.profile = UserProfile.objects.get(user=self.user)
        self.client.login(username='testuser', password='testpassword')

    def test_profile_view_get(self):
        """
        Test that the profile page loads successfully for a logged-in user.
        """
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile.html')
        self.assertIn('form', response.context)
        self.assertIn('orders', response.context)

    def test_profile_view_post_valid(self):
        """ Test that the profile form updates correctly with valid data. """
        response = self.client.post(reverse('profile'), {
            'full_name': 'John Doe',
        }, follow=True)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.full_name, 'John Doe')
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn('Profile updated successfully', messages)

    def test_profile_view_post_invalid(self):
        """
        Test that an invalid form submission does not update the profile.
        """
        response = self.client.post(reverse('profile'), {
            'full_name': 'A' * 100,  # Exceeds max_length
        }, follow=True)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn('Update failed. Please ensure the form is valid.',
                      messages)


class OrderHistoryViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser',
                                             password='testpassword')
        self.profile = UserProfile.objects.get(user=self.user)
        self.order = Order.objects.create(order_number='12345',
                                          user_profile=self.profile)
        self.client.login(username='testuser', password='testpassword')

    def test_order_history_view(self):
        """Test that order history loads correctly for a valid order."""
        response = self.client.get(reverse('order_history', args=['12345']))

        # Check that the page loads successfully
        self.assertEqual(response.status_code, 200)

        # Check that the correct template is used
        self.assertTemplateUsed(response, 'checkout/checkout_success.html')

        # Check that the correct order is passed to the template
        self.assertEqual(response.context['order'], self.order)

        # Retrieve messages from the response
        messages = [m.message for m in get_messages(response.wsgi_request)]

        # Ensure the expected message is present
        expected_message = (
            "This is a past confirmation for order number 12345. "
            "A confirmation email was sent on the order date."
        )
        self.assertIn(expected_message, messages)
