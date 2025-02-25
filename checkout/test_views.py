from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch
from django.contrib.auth import get_user_model
from .models import Order
from products.models import Product
from profiles.models import UserProfile


class CheckoutViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.cache_checkout_data_url = reverse('cache_checkout_data')
        self.user = get_user_model().objects.create_user(username='testuser',
                                                         password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.user_profile, created = UserProfile.objects.get_or_create(
            user=self.user)
        self.product = Product.objects.create(
            name='Test Product',
            price=10.00,
        )

    @patch("checkout.views.stripe.PaymentIntent.modify")  # Mock Stripe
    def test_cache_checkout_data(self, mock_modify):
        """Test caching checkout data in PaymentIntent metadata"""
        mock_modify.return_value = None  # Simulate a successful API response

        # Ensure the session contains a bag
        session = self.client.session
        session["bag"] = {"item_id": 1, "quantity": 2}
        session.save()

        response = self.client.post(
            self.cache_checkout_data_url,
            {"client_secret": "pi_123456789_secret_test", "save_info": "true"},
        )

        mock_modify.assert_called_once_with(
            "pi_123456789",
            metadata={
                "bag": '{"item_id": 1, "quantity": 2}',
                "save_info": "true",
                "username": "testuser",
            },
        )
        self.assertEqual(response.status_code, 200)

    def test_checkout_view_with_empty_bag(self):
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 302)  # Should redirect
        self.assertRedirects(response, reverse('products'))

    def test_checkout_view_with_valid_data(self):
        self.client.session['bag'] = {self.product.id: 1}
        response = self.client.post(reverse('checkout'), {
            'full_name': 'Test User',
            'email': 'test@example.com',
            'phone_number': '1234567890',
            'street_address1': '123 Test St',
            'street_address2': '',
            'town_or_city': 'Test City',
            'postcode': '12345',
            'client_secret': 'test_secret_123456',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('checkout_success',
                                               args=[Order.objects.first()
                                                     .order_number]))

    def test_checkout_success_view(self):
        self.client.session['bag'] = {self.product.id: 1}
        order_response = self.client.post(reverse('checkout'), {  # noqa
            'full_name': 'Test User',
            'email': 'test@example.com',
            'phone_number': '1234567890',
            'street_address1': '123 Test St',
            'street_address2': '',
            'town_or_city': 'Test City',
            'postcode': '12345',
            'client_secret': 'test_secret_123456',
        })
        order_number = Order.objects.first().order_number

        response = self.client.get(reverse('checkout_success',
                                           args=[order_number]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,
                            'Your order has been successfully processed!')

    def test_checkout_success_view_without_user_profile(self):
        # Test case where the user profile does not exist
        self.client.logout()
        self.client.login(username='testuser', password='testpass')
        self.client.session['bag'] = {self.product.id: 1}
        response = self.client.post(reverse('checkout'), {
            'full_name': 'Test User',
            'email': 'test@example.com',
            'phone_number': '1234567890',
            'street_address1': '123 Test St',
            'street_address2': '',
            'town_or_city': 'Test City',
            'postcode': '12345',
            'client_secret': 'test_secret_123456',
        })
        order_number = Order.objects.first().order_number

        response = self.client.get(reverse('checkout_success',
                                           args=[order_number]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,
                            'Your order has been successfully processed!')
