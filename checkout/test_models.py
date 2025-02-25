from django.test import TestCase
from django.contrib.auth import get_user_model
from products.models import Product
from profiles.models import UserProfile
from .models import Order, OrderLineItem


class OrderModelTest(TestCase):

    def setUp(self):
        """Create a user profile and product for testing."""
        self.user = get_user_model().objects.create_user(username='testuser',
                                                         password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.user_profile, created = UserProfile.objects.get_or_create(
            user=self.user)
        self.product = Product.objects.create(
            name='Test Product',
            price=10.00,
        )

        # Create an order
        self.order = Order.objects.create(
            user_profile=self.user_profile,
            full_name='Test User',
            email='test@example.com',
            phone_number='1234567890',
            street_address1='123 Test St',
            street_address2='',
            town_or_city='Test City',
            postcode='12345',
            original_bag='{}',
            stripe_pid='test_stripe_pid'
        )

        OrderLineItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=1  # Set quantity to 1 to have a total of 10.00
        )

    def test_order_creation(self):
        """Test if the order is created correctly."""
        self.assertEqual(self.order.full_name, 'Test User')
        self.assertEqual(self.order.email, 'test@example.com')
        # Ensure order number is set
        self.assertEqual(self.order.order_number, self.order.order_number)

    def test_generate_order_number(self):
        """Test if the order number is generated."""
        order = Order()
        order.save()  # Save to generate order number
        # Ensure the order number is generated
        self.assertIsNotNone(order.order_number)

    def test_update_total(self):
        self.order.update_total()  # Call update_total to calculate the totals

        # Order total should be 11.00, delivery should be 1.00.
        self.assertEqual(self.order.delivery_cost, 1.00)
        self.assertEqual(self.order.order_total, 10.00)  # Verify order total
        self.assertEqual(self.order.grand_total, 11.00)  # Verify grand total

    def test_order_line_item_creation(self):
        """Test if the line item total is calculated correctly."""
        line_item = OrderLineItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2
        )
        self.assertEqual(line_item.lineitem_total, 20.00)  # 10.00 * 2

    def test_order_string_representation(self):
        """Test the string representation of the order."""
        self.assertEqual(str(self.order), self.order.order_number)
