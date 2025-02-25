from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Category, Barrel


class ProductViewsTest(TestCase):
    def setUp(self):
        # Create a superuser for testing
        self.superuser = User.objects.create_superuser(
            username='superuser', password='password'
        )

        # Create a category for testing
        self.category = Category.objects.create(
            name='Barrels', friendly_name='Barrels'
        )

        # Create a product for testing
        self.product = Barrel.objects.create(
            name='Test Barrel',
            description='A great test barrel.',
            price=29.99,
            sku='TESTBARREL123',
            category=self.category,
            barrel_shape='Standard'
        )

    def test_all_products_view(self):
        response = self.client.get(reverse('products'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/all_products.html')
        self.assertContains(response, 'Test Barrel')

    def test_product_details_view(self):
        response = self.client.get(reverse('product_details',
                                           args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_details.html')
        self.assertContains(response, 'Test Barrel')

    def test_add_product_view(self):
        self.client.login(username='superuser', password='password')
        response = self.client.post(reverse('add_product'), {
            'name': 'New Barrel',
            'description': 'A new test barrel.',
            'price': 39.99,
            'sku': 'NEWBARREL123',
            'category': self.category.id,
            'barrel_shape': 'Tapered',
        })

        # If not a redirect, check for form errors
        if response.status_code != 302:
            # Print response content
            print("Response content:", response.content)
            # Print form errors if available
            print("Form errors:", response.context.get('form').errors)

        self.assertEqual(response.status_code, 302)  # Expect a redirect
        self.assertRedirects(response,
                             reverse('product_details',
                                     args=[Barrel.objects.last().id]))
        self.assertEqual(Barrel.objects.count(), 2)  # Ensure addition

    def test_edit_product_view(self):
        self.client.login(username='superuser', password='password')
        response = self.client.post(reverse('edit_product',
                                            args=[self.product.id]), {
            'name': 'Updated Barrel',
            'description': 'An updated test barrel.',
            'price': 29.99,
            'sku': 'TESTBARREL123',
            'category': self.category.id,
            'barrel_shape': 'Tapered',
        })

        # If not a redirect, check for form errors
        if response.status_code != 302:
            # Print the response content
            print("Response content:", response.content)
            # Print form errors if available
            print("Form errors:", response.context.get('form').errors)

        self.assertEqual(response.status_code, 302)  # Expect a redirect
        self.assertRedirects(response, reverse('product_details',
                                               args=[self.product.id]))
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Updated Barrel')

    def test_delete_product_view(self):
        self.client.login(username='superuser', password='password')
        response = self.client.post(reverse('delete_product',
                                            args=[self.product.id]))
        self.assertEqual(response.status_code, 302)  # Expect a redirect
        self.assertRedirects(response, reverse('products'))
        # Ensure the product was deleted
        self.assertEqual(Barrel.objects.count(), 0)

    def test_add_product_view_redirects_non_superuser(self):
        user = User.objects.create_user(username='normaluser',  # noqa
                                        password='password')
        self.client.login(username='normaluser', password='password')
        response = self.client.get(reverse('add_product'))
        self.assertRedirects(response, reverse('home'))

    def test_edit_product_view_redirects_non_superuser(self):
        user = User.objects.create_user(username='normaluser',  # noqa
                                        password='password')
        self.client.login(username='normaluser', password='password')
        response = self.client.get(reverse('edit_product',
                                           args=[self.product.id]))
        self.assertRedirects(response, reverse('home'))

    def test_delete_product_view_redirects_non_superuser(self):
        user = User.objects.create_user(username='normaluser',  # noqa
                                        password='password')
        self.client.login(username='normaluser', password='password')
        response = self.client.post(reverse('delete_product',
                                            args=[self.product.id]))
        self.assertRedirects(response, reverse('home'))
