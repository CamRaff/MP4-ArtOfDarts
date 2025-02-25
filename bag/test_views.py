from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from products.models import Barrel, Stem, Flight
from profiles.models import UserProfile


class BagViewsTest(TestCase):

    def setUp(self):
        """Create a user profile and product for testing."""
        self.user = get_user_model().objects.create_user(username='testuser',
                                                         password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.user_profile, created = UserProfile.objects.get_or_create(
            user=self.user)

        # Create product instances
        self.barrel_product = Barrel.objects.create(
            name='Test Barrel',
            price=10.00,
            barrel_shape='Straight'
        )
        self.stem_product = Stem.objects.create(
            name='Test Stem',
            price=5.00,
            stem_length='Short'
        )
        self.flight_product = Flight.objects.create(
            name='Test Flight',
            price=2.00,
            flight_shape='Standard'
        )

    def test_view_bag(self):
        """Test the view_bag view renders the bag contents page."""
        response = self.client.get(reverse('view_bag'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bag/bag.html')

    def test_add_to_bag(self):
        """Test adding a product to the shopping bag."""
        response = self.client.post(reverse('add_to_bag',
                                            args=[self.barrel_product.pk]), {
            'quantity': 2,
            'redirect_url': reverse('view_bag')
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.session['bag']
                         [str(self.barrel_product.pk)], 2)

    def test_adjust_bag(self):
        """Test adjusting the quantity of a product in the shopping bag."""
        self.client.post(reverse('add_to_bag',
                                 args=[self.barrel_product.pk]), {
            'quantity': 2,
            'redirect_url': reverse('view_bag')
        })
        response = self.client.post(reverse('adjust_bag',
                                            args=[self.barrel_product.pk]), {
            'quantity': 1
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.session['bag']
                         [str(self.barrel_product.pk)], 1)

    def test_remove_from_bag(self):
        """Test removing a product from the shopping bag."""
        self.client.post(reverse('add_to_bag',
                                 args=[self.barrel_product.pk]), {
            'quantity': 2,
            'redirect_url': reverse('view_bag')
        })
        response = self.client.post(reverse('remove_from_bag',
                                            args=[self.barrel_product.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(str(self.barrel_product.pk),
                         self.client.session['bag'])

    def test_product_type_in_bag(self):
        """Test if product types are correctly identified in the bag."""
        self.client.post(reverse('add_to_bag',
                                 args=[self.barrel_product.pk]), {
            'quantity': 1,
            'redirect_url': reverse('view_bag')
        })
        response = self.client.get(reverse('view_bag'))
        self.assertContains(response, 'Straight Barrel')

        self.client.post(reverse('add_to_bag', args=[self.stem_product.pk]), {
            'quantity': 1,
            'redirect_url': reverse('view_bag')
        })
        response = self.client.get(reverse('view_bag'))
        self.assertContains(response, 'Short Stem')

        self.client.post(reverse('add_to_bag',
                                 args=[self.flight_product.pk]), {
            'quantity': 1,
            'redirect_url': reverse('view_bag')
        })
        response = self.client.get(reverse('view_bag'))
        self.assertContains(response, 'Standard Flight')
